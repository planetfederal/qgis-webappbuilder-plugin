from geoserver.support import ResourceInfo, bbox, write_bbox, \
        write_string, xml_property, url

def _maybe_text(n):
    if n is None:
        return None
    else:
        return n.text

def _layer_list(node, element):
    if node is not None:
        return [_maybe_text(n.find("name")) for n in node.findall(element)]
        
def _style_list(node):
    if node is not None:
        return [_maybe_text(n.find("name")) for n in node.findall("style")]

def _write_layers(builder, layers, parent, element, attributes):
    builder.start(parent, dict())
    for l in layers:
        builder.start(element, attributes or dict())
        if l is not None:
            builder.start("name", dict())
            builder.data(l)
            builder.end("name")
        builder.end(element)
    builder.end(parent)

def _write_styles(builder, styles):
    builder.start("styles", dict())
    for s in styles:
        builder.start("style", dict())
        if s is not None:
            builder.start("name", dict())
            builder.data(s)
            builder.end("name")
        builder.end("style")
    builder.end("styles")

class LayerGroup(ResourceInfo):
    """
    Represents a layer group in geoserver 
    """

    resource_type = "layerGroup"
    save_method = "PUT"

    def __init__(self, catalog, name):
        super(LayerGroup, self).__init__()

        assert isinstance(name, basestring)

        self.catalog = catalog
        self.name = name

        # the XML format changed in 2.3.x - the element listing all the layers
        # and the entries themselves have changed
        if self.catalog.gsversion() == "2.2.x":
            parent, element, attributes = "layers", "layer", None
        else:
            parent, element, attributes = "publishables", "published", {'type':'layer'}
        self._layer_parent = parent
        self._layer_element = element
        self._layer_attributes = attributes
        self.writers = dict(
            name = write_string("name"),
            styles = _write_styles,
            layers = lambda b,l: _write_layers(b, l, parent, element, attributes),
            bounds = write_bbox("bounds")
        )

    @property
    def href(self):
        return url(self.catalog.service_url, ["layergroups", self.name + ".xml"])

    styles = xml_property("styles", _style_list)
    bounds = xml_property("bounds", bbox)

    def _layers_getter(self):
        if "layers" in self.dirty:
            return self.dirty["layers"]
        else:
            if self.dom is None:
                self.fetch()
            node = self.dom.find(self._layer_parent)
            return _layer_list(node, self._layer_element) if node is not None else None

    def _layers_setter(self, value):
        self.dirty["layers"] = value

    def _layers_delete(self):
        self.dirty["layers"] = None
    
    layers =  property(_layers_getter, _layers_setter, _layers_delete)

    def __str__(self):
        return "<LayerGroup %s>" % self.name

    __repr__ = __str__

class UnsavedLayerGroup(LayerGroup):
    save_method = "POST"
    def __init__(self, catalog, name, layers, styles, bounds):
        super(UnsavedLayerGroup, self).__init__(catalog, name)
        bounds = bounds if bounds is not None else ("-180","180","-90","90","EPSG:4326")
        self.dirty.update(name = name, layers = layers, styles = styles, bounds = bounds)

    @property
    def href(self):
        return "%s/layergroups?name=%s" % (self.catalog.service_url, self.name)
