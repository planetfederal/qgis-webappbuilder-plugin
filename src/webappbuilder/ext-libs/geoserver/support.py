import logging
from xml.etree.ElementTree import TreeBuilder, tostring
from tempfile import mkstemp
import urllib
import urlparse
from zipfile import ZipFile
import os

logger = logging.getLogger("gsconfig.support")

FORCE_DECLARED = "FORCE_DECLARED"
## The projection handling policy for layers that should use coordinates
## directly while reporting the configured projection to clients.  This should be
## used when projection information is missing from the underlying datastore.


FORCE_NATIVE = "FORCE_NATIVE"
## The projection handling policy for layers that should use the projection
## information from the underlying storage mechanism directly, and ignore the
## projection setting.

REPROJECT = "REPROJECT"
## The projection handling policy for layers that should use the projection
## information from the underlying storage mechanism to reproject to the
## configured projection.

def url(base, seg, query=None):
    """
    Create a URL from a list of path segments and an optional dict of query
    parameters.
    """

    def clean_segment(segment):
        """
        Cleans the segment and encodes to UTF-8 if the segment is unicode.
        """
        segment = segment.strip('/')
        if isinstance(segment, unicode):
            segment = segment.encode('utf-8')
        return segment

    seg = (urllib.quote(clean_segment(s)) for s in seg)
    if query is None or len(query) == 0:
        query_string = ''
    else:
        query_string = "?" + urllib.urlencode(query)
    path = '/'.join(seg) + query_string
    adjusted_base = base.rstrip('/') + '/'
    return urlparse.urljoin(adjusted_base, path)

def xml_property(path, converter = lambda x: x.text, default=None):
    def getter(self):
        if path in self.dirty:
            return self.dirty[path]
        else:
            if self.dom is None:
                self.fetch()
            node = self.dom.find(path)
            return converter(self.dom.find(path)) if node is not None else default

    def setter(self, value):
        self.dirty[path] = value

    def delete(self):
        self.dirty[path] = None

    return property(getter, setter, delete)

def bbox(node):
    if node is not None: 
        minx = node.find("minx")
        maxx = node.find("maxx")
        miny = node.find("miny")
        maxy = node.find("maxy")
        crs  = node.find("crs")
        crs  = crs.text if crs is not None else None

        if (None not in [minx, maxx, miny, maxy]):
            return (minx.text, maxx.text, miny.text, maxy.text, crs)
        else: 
            return None
    else:
        return None

def string_list(node):
    if node is not None:
        return [n.text for n in node.findall("string")]

def attribute_list(node):
    if node is not None:
        return [n.text for n in node.findall("attribute/name")]

def key_value_pairs(node):
    if node is not None:
        return dict((entry.attrib['key'], entry.text) for entry in node.findall("entry"))

def write_string(name):
    def write(builder, value):
        builder.start(name, dict())
        if (value is not None):
            builder.data(value)
        builder.end(name)
    return write

def write_bool(name):
    def write(builder, b):
        builder.start(name, dict())
        builder.data("true" if b and b != "false" else "false")
        builder.end(name)
    return write

def write_bbox(name):
    def write(builder, b):
        builder.start(name, dict())
        bbox_xml(builder, b)
        builder.end(name)
    return write

def write_string_list(name):
    def write(builder, words):
        builder.start(name, dict())
        words = [w for w in words if len(w) > 0]
        for w in words:
            builder.start("string", dict())
            builder.data(w)
            builder.end("string")
        builder.end(name)
    return write

def write_dict(name):
    def write(builder, pairs):
        builder.start(name, dict())
        for k, v in pairs.iteritems():
            builder.start("entry", dict(key=k))
            builder.data(v)
            builder.end("entry")
        builder.end(name)
    return write

def write_metadata(name):
    def write(builder, metadata):
        builder.start(name, dict())
        for k, v in metadata.iteritems():
            builder.start("entry", dict(key=k))
            if k in ['time', 'elevation'] or k.startswith('custom_dimension'):
                dimension_info(builder, v)
            elif k == 'DynamicDefaultValues':
                dynamic_default_values_info(builder, v)
            else:
                builder.data(v)
            builder.end("entry")
        builder.end(name)
    return write

class ResourceInfo(object):
    def __init__(self):
        self.dom = None
        self.dirty = dict()

    def fetch(self):
        self.dom = self.catalog.get_xml(self.href)

    def clear(self):
        self.dirty = dict()

    def refresh(self):
        self.clear()
        self.fetch()

    def serialize(self, builder):
        # GeoServer will disable the resource if we omit the <enabled> tag,
        # so force it into the dirty dict before writing
        if hasattr(self, "enabled"):
            self.dirty['enabled'] = self.enabled

        if hasattr(self, "advertised"):
            self.dirty['advertised'] = self.advertised

        for k, writer in self.writers.items():
            if k in self.dirty:
                writer(builder, self.dirty[k])

    def message(self):
        builder = TreeBuilder()
        builder.start(self.resource_type, dict())
        self.serialize(builder)
        builder.end(self.resource_type)
        msg = tostring(builder.close())
        return msg
                
def prepare_upload_bundle(name, data):
    """GeoServer's REST API uses ZIP archives as containers for file formats such
    as Shapefile and WorldImage which include several 'boxcar' files alongside
    the main data.  In such archives, GeoServer assumes that all of the relevant
    files will have the same base name and appropriate extensions, and live in
    the root of the ZIP archive.  This method produces a zip file that matches
    these expectations, based on a basename, and a dict of extensions to paths or
    file-like objects. The client code is responsible for deleting the zip
    archive when it's done."""
    fd, path = mkstemp()
    zip_file = ZipFile(path, 'w')
    for ext, stream in data.iteritems():
        fname = "%s.%s" % (name, ext)
        if (isinstance(stream, basestring)):
            zip_file.write(stream, fname)
        else:
            zip_file.writestr(fname, stream.read())
    zip_file.close()
    os.close(fd)
    return path

def atom_link(node):
    if 'href' in node.attrib:
        return node.attrib['href']
    else:
        l = node.find("{http://www.w3.org/2005/Atom}link")
        return l.get('href')

def atom_link_xml(builder, href):
    builder.start("atom:link", {
        'rel': 'alternate',
        'href': href,
        'type': 'application/xml',
        'xmlns:atom': 'http://www.w3.org/2005/Atom'
    })
    builder.end("atom:link")

def bbox_xml(builder, box):
    minx, maxx, miny, maxy, crs = box
    builder.start("minx", dict())
    builder.data(minx)
    builder.end("minx")
    builder.start("maxx", dict())
    builder.data(maxx)
    builder.end("maxx")
    builder.start("miny", dict())
    builder.data(miny)
    builder.end("miny")
    builder.start("maxy", dict())
    builder.data(maxy)
    builder.end("maxy")
    if crs is not None:
        builder.start("crs", {"class": "projected"})
        builder.data(crs)
        builder.end("crs")

def dimension_info(builder, metadata):
    if isinstance(metadata, DimensionInfo):
        builder.start("dimensionInfo", dict())
        builder.start("enabled", dict())
        builder.data("true" if metadata.enabled else "false")
        builder.end("enabled")
        if metadata.presentation is not None:
            accepted = ['LIST', 'DISCRETE_INTERVAL', 'CONTINUOUS_INTERVAL']
            if metadata.presentation not in accepted:
                raise ValueError("metadata.presentation must be one of the following %s" % accepted)
            else:
                builder.start("presentation", dict())
                builder.data(metadata.presentation)
                builder.end("presentation")
        if metadata.attribute is not None:
            builder.start("attribute", dict())
            builder.data(metadata.attribute)
            builder.end("attribute")
        if metadata.end_attribute is not None:
            builder.start("endAttribute", dict())
            builder.data(metadata.end_attribute)
            builder.end("endAttribute")
        if metadata.resolution is not None:
            builder.start("resolution", dict())
            builder.data(str(metadata.resolution_millis()))
            builder.end("resolution")
        if metadata.units is not None:
            builder.start("units", dict())
            builder.data(metadata.units)
            builder.end("units")
        if metadata.unitSymbol is not None:
            builder.start("unitSymbol", dict())
            builder.data(metadata.unitSymbol)
            builder.end("unitSymbol")
        if metadata.strategy is not None:
            builder.start("defaultValue", dict())
            builder.start("strategy", dict())
            builder.data(metadata.strategy)
            builder.end("strategy")
            builder.end("defaultValue")
            
        builder.end("dimensionInfo")

class DimensionInfo(object):

    _lookup = (
        ('seconds', 1),
        ('minutes', 60),
        ('hours', 3600),
        ('days', 86400),
        ('months', 2628000000), # this is the number geoserver computes for 1 month
        ('years', 31536000000)
    )

    def __init__(self, name, enabled, presentation, resolution, units, unitSymbol, strategy=None, attribute=None, end_attribute=None):
        self.name = name
        self.enabled = enabled
        self.attribute = attribute
        self.end_attribute = end_attribute
        self.presentation = presentation
        self.resolution = resolution
        self.units = units
        self.unitSymbol = unitSymbol
        self.strategy = strategy

    def _multipier(self, name):
        name = name.lower()
        found = [ i[1] for i in self._lookup if i[0] == name ]
        if not found: raise ValueError('invalid multipler: %s' % name)
        return found[0] if found else None
    
    def resolution_millis(self):
        '''if set, get the value of resolution in milliseconds'''
        if self.resolution is None or not isinstance(self.resolution, basestring):
                return self.resolution
        val, mult = self.resolution.split(' ')
        return int(float(val) * self._multipier(mult) * 1000)

    def resolution_str(self):
        '''if set, get the value of resolution as "<n> <period>s", for example: "8 seconds"'''
        if self.resolution is None or isinstance(self.resolution, basestring):
            return self.resolution
        seconds = self.resolution / 1000.
        biggest = self._lookup[0]
        for entry in self._lookup:
            if seconds < entry[1]: break
            biggest = entry
        val = seconds / biggest[1]
        if val == int(val):
            val = int(val)
        return '%s %s' % (val, biggest[0])


def md_dimension_info(name, node):
    """Extract metadata Dimension Info from an xml node"""
    child_text = lambda child_name: getattr(node.find(child_name), 'text', None)
    resolution = child_text('resolution')
    return DimensionInfo(
        name, 
        child_text('enabled') == 'true',
        child_text('presentation'),
        int(resolution) if resolution else None,
        child_text('units'),
        child_text('unitSymbol'),
        child_text('strategy'),
        child_text('attribute'),
        child_text('endAttribute'),
    )

def dynamic_default_values_info(builder, metadata):
    if isinstance(metadata, DynamicDefaultValues):
        builder.start("DynamicDefaultValues", dict())
        
        if metadata.configurations is not None:
            builder.start("configurations", dict())
            for c in metadata.configurations:
                builder.start("configuration", dict())
                if c.dimension is not None:
                    builder.start("dimension", dict())
                    builder.data(c.dimension)
                    builder.end("dimension")
                if c.policy is not None:
                    builder.start("policy", dict())
                    builder.data(c.policy)
                    builder.end("policy")
                if c.defaultValueExpression is not None:
                    builder.start("defaultValueExpression", dict())
                    builder.data(c.defaultValueExpression)
                    builder.end("defaultValueExpression")
                builder.end("configuration")
            builder.end("configurations")
        builder.end("DynamicDefaultValues")
        
class DynamicDefaultValuesConfiguration(object):
    def __init__(self, dimension, policy, defaultValueExpression):
        self.dimension = dimension
        self.policy = policy
        self.defaultValueExpression = defaultValueExpression

class DynamicDefaultValues(object):
    def __init__(self, name, configurations):
        self.name = name
        self.configurations = configurations

def md_dynamic_default_values_info(name, node):
    """Extract metadata Dynamic Default Values from an xml node"""
    configurations = node.find("configurations")
    if configurations is not None:
        configurations = []
        for n in node.findall("configuration"):
            dimension = n.find("dimension")
            dimension = dimension.text if dimension is not None else None
            policy = n.find("policy")
            policy = policy.text if policy is not None else None
            defaultValueExpression = n.find("defaultValueExpression")
            defaultValueExpression = defaultValueExpression.text if defaultValueExpression is not None else None
            
            configurations.append(DynamicDefaultValuesConfiguration(dimension, policy, defaultValueExpression))
            
    return DynamicDefaultValues(name, configurations)

def md_entry(node):
    """Extract metadata entries from an xml node"""
    key = None
    value = None
    if 'key' in node.attrib:
        key = node.attrib['key']
    else:
        key = None

    if key in ['time', 'elevation'] or key.startswith('custom_dimension'):
        value = md_dimension_info(key, node.find("dimensionInfo"))
    elif key == 'DynamicDefaultValues':
        value = md_dynamic_default_values_info(key, node.find("DynamicDefaultValues"))
    else:
        value = node.text
        
    if None in [key, value]:
        return None
    else:
        return (key, value)

def metadata(node):
    if node is not None:
        return dict(md_entry(n) for n in node.findall("entry"))

def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv

def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv
