from datetime import datetime, timedelta
import logging
import json
from geoserver.layer import Layer
from geoserver.resource import FeatureType, Coverage
from geoserver.store import coveragestore_from_index, datastore_from_index, \
    wmsstore_from_index, UnsavedDataStore, \
    UnsavedCoverageStore, UnsavedWmsStore
from geoserver.style import Style
from geoserver.support import prepare_upload_bundle, url, _decode_list, _decode_dict
from geoserver.layergroup import LayerGroup, UnsavedLayerGroup
from geoserver.workspace import workspace_from_index, Workspace
from os import unlink
import httplib2
from xml.etree.ElementTree import XML
from xml.parsers.expat import ExpatError

from urlparse import urlparse

logger = logging.getLogger("gsconfig.catalog")

class UploadError(Exception):
    pass

class ConflictingDataError(Exception):
    pass

class AmbiguousRequestError(Exception):
    pass

class FailedRequestError(Exception):
    pass

def _name(named):
    """Get the name out of an object.  This varies based on the type of the input:
       * the "name" of a string is itself
       * the "name" of None is itself
       * the "name" of an object with a property named name is that property -
         as long as it's a string
       * otherwise, we raise a ValueError
    """
    if isinstance(named, basestring) or named is None:
        return named
    elif hasattr(named, 'name') and isinstance(named.name, basestring):
        return named.name
    else:
        raise ValueError("Can't interpret %s as a name or a configuration object" % named)

class Catalog(object):
    """
    The GeoServer catalog represents all of the information in the GeoServer
    configuration.    This includes:
    - Stores of geospatial data
    - Resources, or individual coherent datasets within stores
    - Styles for resources
    - Layers, which combine styles with resources to create a visible map layer
    - LayerGroups, which alias one or more layers for convenience
    - Workspaces, which provide logical grouping of Stores
    - Maps, which provide a set of OWS services with a subset of the server's
        Layers
    - Namespaces, which provide unique identifiers for resources
    """

    def __init__(self, service_url, username="admin", password="geoserver", disable_ssl_certificate_validation=False):
        self.service_url = service_url
        if self.service_url.endswith("/"):
            self.service_url = self.service_url.strip("/")
        self.username = username
        self.password = password
        self.diable_ssl_cert_validation = disable_ssl_certificate_validation
        self.http = None
        self.setup_connection()

        self._cache = dict()
        self._version = None

    def __getstate__(self):
        '''http connection cannot be pickled'''
        state = dict(vars(self))
        state.pop('http', None)
        state['http'] = None
        return state

    def __setstate__(self, state):
        '''restore http connection upon unpickling'''
        self.__dict__.update(state)
        self.setup_connection()

    @property
    def gs_base_url(self):
        return self.service_url.rstrip("rest")

    def setup_connection(self):
        self.http = httplib2.Http(
            disable_ssl_certificate_validation=self.diable_ssl_cert_validation)
        self.http.add_credentials(self.username, self.password)
        netloc = urlparse(self.service_url).netloc
        self.http.authorizations.append(
            httplib2.BasicAuthentication(
                (self.username, self.password),
                netloc,
                self.service_url,
                {},
                None,
                None,
                self.http
            ))

    def about(self):
        '''return the about information as a formatted html'''
        about_url = self.service_url + "/about/version.html"
        response, content = self.http.request(about_url, "GET")
        if response.status == 200:
            return content
        raise FailedRequestError('Unable to determine version: %s' %
                                 (content or response.status))

    def gsversion(self):
        '''obtain the version or just 2.2.x if < 2.3.x
        Raises:
            FailedRequestError: If the request fails.
        '''
        if self._version: return self._version
        about_url = self.service_url + "/about/version.xml"
        response, content = self.http.request(about_url, "GET")
        version = None
        if response.status == 200:
            dom = XML(content)
            resources = dom.findall("resource")
            for resource in resources:
                if resource.attrib["name"] == "GeoServer":
                    try:
                        version = resource.find("Version").text
                        break
                    except:
                        pass

        #This will raise an exception if the catalog is not available
        #If the catalog is available but could not return version information,
        #it is an old version that does not support that
        if version is None:
            self.get_workspaces()
            # just to inform that version < 2.3.x
            version = "2.2.x"
        self._version = version
        return version

    def delete(self, config_object, purge=False, recurse=False):
        """
        send a delete request
        XXX [more here]
        """
        rest_url = config_object.href

        #params aren't supported fully in httplib2 yet, so:
        params = []

        # purge deletes the SLD from disk when a style is deleted
        if purge:
            params.append("purge=true")

        # recurse deletes the resource when a layer is deleted.
        if recurse:
            params.append("recurse=true")

        if params:
            rest_url = rest_url + "?" + "&".join(params)

        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        response, content = self.http.request(rest_url, "DELETE", headers=headers)
        self._cache.clear()

        if response.status == 200:
            return (response, content)
        else:
            raise FailedRequestError("Tried to make a DELETE request to %s but got a %d status code: \n%s" % (rest_url, response.status, content))

    def get_xml(self, rest_url):
        logger.debug("GET %s", rest_url)

        cached_response = self._cache.get(rest_url)

        def is_valid(cached_response):
            return cached_response is not None and datetime.now() - cached_response[0] < timedelta(seconds=5)

        def parse_or_raise(xml):
            try:
                return XML(xml)
            except (ExpatError, SyntaxError), e:
                msg = "GeoServer gave non-XML response for [GET %s]: %s"
                msg = msg % (rest_url, xml)
                raise Exception(msg, e)

        if is_valid(cached_response):
            raw_text = cached_response[1]
            return parse_or_raise(raw_text)
        else:
            response, content = self.http.request(rest_url)
            if response.status == 200:
                self._cache[rest_url] = (datetime.now(), content)
                return parse_or_raise(content)
            else:
                raise FailedRequestError("Tried to make a GET request to %s but got a %d status code: \n%s" % (rest_url, response.status, content))

    def reload(self):
        reload_url = url(self.service_url, ['reload'])
        response = self.http.request(reload_url, "POST")
        self._cache.clear()
        return response

    def reset(self):
        reload_url = url(self.service_url, ['reset'])
        response = self.http.request(reload_url, "POST")
        self._cache.clear()
        return response

    def save(self, obj):
        """
        saves an object to the REST service

        gets the object's REST location and the XML from the object,
        then POSTS the request.
        """
        rest_url = obj.href
        message = obj.message()

        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        logger.debug("%s %s", obj.save_method, obj.href)
        response = self.http.request(rest_url, obj.save_method, message, headers)
        headers, body = response
        self._cache.clear()
        if 400 <= int(headers['status']) < 600:
            raise FailedRequestError("Error code (%s) from GeoServer: %s" %
                (headers['status'], body))
        return response

    def get_store(self, name, workspace=None):

        # Make sure workspace is a workspace object and not a string.
        # If the workspace does not exist, continue as if no workspace had been defined.
        if isinstance(workspace, basestring):
            workspace = self.get_workspace(workspace)

        # Create a list with potential workspaces to look into
        # if a workspace is defined, it will contain only that workspace
        # if no workspace is defined, the list will contain all workspaces.
        workspaces = []

        if workspace is None:
            workspaces.extend(self.get_workspaces())
        else:
            workspaces.append(workspace)

        # Iterate over all workspaces to find the stores or store
        found_stores = {}
        for ws in workspaces:
            # Get all the store objects from geoserver
            raw_stores = self.get_stores(workspace=ws)
            # And put it in a dictionary where the keys are the name of the store,
            new_stores = dict(zip([s.name for s in raw_stores], raw_stores))
            # If the store is found, put it in a dict that also takes into account the
            # worspace.
            if name in new_stores:
                found_stores[ws.name + ':' + name] = new_stores[name]

        # There are 3 cases:
        #    a) No stores are found.
        #    b) Only one store is found.
        #    c) More than one is found.
        if len(found_stores) == 0:
            raise FailedRequestError("No store found named: " + name)
        elif len(found_stores) > 1:
            raise AmbiguousRequestError("Multiple stores found named '" + name + "': "+ found_stores.keys())
        else:
            return found_stores.values()[0]


    def get_stores(self, workspace=None):
        if workspace is not None:
            if isinstance(workspace, basestring):
                workspace = self.get_workspace(workspace)
            ds_list = self.get_xml(workspace.datastore_url)
            cs_list = self.get_xml(workspace.coveragestore_url)
            wms_list = self.get_xml(workspace.wmsstore_url)
            datastores = [datastore_from_index(self, workspace, n) for n in ds_list.findall("dataStore")]
            coveragestores = [coveragestore_from_index(self, workspace, n) for n in cs_list.findall("coverageStore")]
            wmsstores = [wmsstore_from_index(self, workspace, n) for n in wms_list.findall("wmsStore")]
            return datastores + coveragestores + wmsstores
        else:
            stores = []
            for ws in self.get_workspaces():
                a = self.get_stores(ws)
                stores.extend(a)
            return stores

    def create_datastore(self, name, workspace=None):
        if isinstance(workspace, basestring):
            workspace = self.get_workspace(workspace)
        elif workspace is None:
            workspace = self.get_default_workspace()
        return UnsavedDataStore(self, name, workspace)

    def create_coveragestore2(self, name, workspace = None):
        """
        Hm we already named the method that creates a coverage *resource*
        create_coveragestore... time for an API break?
        """
        if isinstance(workspace, basestring):
            workspace = self.get_workspace(workspace)
        elif workspace is None:
            workspace = self.get_default_workspace()
        return UnsavedCoverageStore(self, name, workspace)

    def create_wmsstore(self, name, workspace = None, user = None, password = None):
        if workspace is None:
            workspace = self.get_default_workspace()
        return UnsavedWmsStore(self, name, workspace, user, password)

    def create_wmslayer(self, workspace, store, name, nativeName=None):
        headers = {
            "Content-type": "text/xml",
            "Accept": "application/xml"
        }
        # if not provided, fallback to name - this is what geoserver will do
        # anyway but nativeName needs to be provided if name is invalid xml
        # as this will cause verification errors since geoserver 2.6.1
        if nativeName is None:
            nativeName = name

        wms_url = store.href.replace('.xml', '/wmslayers')
        data = "<wmsLayer><name>%s</name><nativeName>%s</nativeName></wmsLayer>" % (name, nativeName)
        headers, response = self.http.request(wms_url, "POST", data, headers)

        self._cache.clear()
        if headers.status < 200 or headers.status > 299: raise UploadError(response) 
        return self.get_resource(name, store=store, workspace=workspace)

    def add_data_to_store(self, store, name, data, workspace=None, overwrite = False, charset = None):
        if isinstance(store, basestring):
            store = self.get_store(store, workspace=workspace)
        if workspace is not None:
            workspace = _name(workspace)
            assert store.workspace.name == workspace, "Specified store (%s) is not in specified workspace (%s)!" % (store, workspace)
        else:
            workspace = store.workspace.name
        store = store.name

        if isinstance(data, dict):
            bundle = prepare_upload_bundle(name, data)
        else:
            bundle = data

        params = dict()
        if overwrite:
            params["update"] = "overwrite"
        if charset is not None:
            params["charset"] = charset

        headers = { 'Content-Type': 'application/zip', 'Accept': 'application/xml' }
        upload_url = url(self.service_url, 
            ["workspaces", workspace, "datastores", store, "file.shp"], params) 

        with open(bundle, "rb") as f:
            data = f.read()
            headers, response = self.http.request(upload_url, "PUT", data, headers)
            self._cache.clear()
            if headers.status != 201:
                raise UploadError(response)

    def create_featurestore(self, name, data, workspace=None, overwrite=False, charset=None):
        if not overwrite:
            try:
                store = self.get_store(name, workspace)
                msg = "There is already a store named " + name
                if workspace:
                    msg += " in " + str(workspace)
                raise ConflictingDataError(msg)
            except FailedRequestError:
                # we don't really expect that every layer name will be taken
                pass

        if workspace is None:
            workspace = self.get_default_workspace()
        workspace = _name(workspace)
        params = dict()
        if charset is not None:
            params['charset'] = charset
        ds_url = url(self.service_url,
            ["workspaces", workspace, "datastores", name, "file.shp"], params)

        # PUT /workspaces/<ws>/datastores/<ds>/file.shp
        headers = {
            "Content-type": "application/zip",
            "Accept": "application/xml"
        }
        if isinstance(data,dict):
            logger.debug('Data is NOT a zipfile')
            archive = prepare_upload_bundle(name, data)
        else:
            logger.debug('Data is a zipfile')
            archive = data
        message = open(archive, 'rb')
        try:
            # response = self.requests.post(ds_url, files={archive: open(archive, 'rb')})
            headers, response = self.http.request(ds_url, "PUT", message, headers)
            self._cache.clear()
            if headers.status != 201:
                raise UploadError(response)
        finally:
            message.close()
            unlink(archive)

    def create_imagemosaic(self, name, data, configure=None, workspace=None, overwrite=False, charset=None):
        if not overwrite:
            try:
                store = self.get_store(name, workspace)
                msg = "There is already a store named " + name
                if workspace:
                    msg += " in " + str(workspace)
                raise ConflictingDataError(msg)
            except FailedRequestError:
                # we don't really expect that every layer name will be taken
                pass

        if workspace is None:
            workspace = self.get_default_workspace()
        workspace = _name(workspace)
        params = dict()
        if charset is not None:
            params['charset'] = charset
        if configure is not None:
            params['configure'] = "none"
        cs_url = url(self.service_url,
            ["workspaces", workspace, "coveragestores", name, "file.imagemosaic"], params)

        # PUT /workspaces/<ws>/coveragestores/<name>/file.imagemosaic?configure=none
        headers = {
            "Content-type": "application/zip",
            "Accept": "application/xml"
        }
        if isinstance(data, basestring):
            message = open(data, 'rb')
        else:
            message = data
        try:
            headers, response = self.http.request(cs_url, "PUT", message, headers)
            self._cache.clear()
            if headers.status != 201:
                raise UploadError(response)
        finally:
            if hasattr(message, "close"):
                message.close()

    def create_coveragestore(self, name, data, workspace=None, overwrite=False):
        if not overwrite:
            try:
                store = self.get_store(name, workspace)
                msg = "There is already a store named " + name
                if workspace:
                    msg += " in " + str(workspace)
                raise ConflictingDataError(msg)
            except FailedRequestError:
                # we don't really expect that every layer name will be taken
                pass

        if workspace is None:
            workspace = self.get_default_workspace()
        headers = {
            "Content-type": "image/tiff",
            "Accept": "application/xml"
        }

        archive = None
        ext = "geotiff"

        if isinstance(data, dict):
            archive = prepare_upload_bundle(name, data)
            message = open(archive, 'rb')
            if "tfw" in data:
                # If application/archive was used, server crashes with a 500 error
                # read in many sites that application/zip will do the trick. Successfully tested
                headers['Content-type'] = 'application/zip'
                ext = "worldimage"
        elif isinstance(data, basestring):
            message = open(data, 'rb')
        else:
            message = data

        cs_url = url(self.service_url,
            ["workspaces", workspace.name, "coveragestores", name, "file." + ext])

        try:
            headers, response = self.http.request(cs_url, "PUT", message, headers)
            self._cache.clear()
            if headers.status != 201:
                raise UploadError(response)
        finally:
            if hasattr(message, "close"):
                message.close()
            if archive is not None:
                unlink(archive)

    def harvest_externalgranule(self, data, store):
        '''Harvest a granule into an existing imagemosaic'''
        params = dict()
        cs_url = url(self.service_url,
            ["workspaces", store.workspace.name, "coveragestores", store.name, "external.imagemosaic"], params)
        # POST /workspaces/<ws>/coveragestores/<name>/external.imagemosaic
        headers = {
            "Content-type": "text/plain",
            "Accept": "application/xml"
        }
        headers, response = self.http.request(cs_url, "POST", data, headers)
        self._cache.clear()
        if headers.status != 202:
            raise UploadError(response)

    def harvest_uploadgranule(self, data, store):
        '''Harvest a granule into an existing imagemosaic'''
        params = dict()
        cs_url = url(self.service_url,
            ["workspaces", store.workspace.name, "coveragestores", store.name, "file.imagemosaic"], params)
        # POST /workspaces/<ws>/coveragestores/<name>/file.imagemosaic
        headers = {
            "Content-type": "application/zip",
            "Accept": "application/xml"
        }
        message = open(data, 'rb')
        try:
            headers, response = self.http.request(cs_url, "POST", message, headers)
            self._cache.clear()
            if headers.status != 202:
                raise UploadError(response)
        finally:
            if hasattr(message, "close"):
                message.close()

    def mosaic_coverages(self, store):
        '''Print granules of an existing imagemosaic'''
        params = dict()
        cs_url = url(self.service_url,
            ["workspaces", store.workspace.name, "coveragestores", store.name, "coverages.json"], params)
        # GET /workspaces/<ws>/coveragestores/<name>/coverages.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        headers, response = self.http.request(cs_url, "GET", None, headers)
        self._cache.clear()
        coverages = json.loads(response, object_hook=_decode_dict)
        return coverages

    def mosaic_coverage_schema(self, coverage, store):
        '''Print granules of an existing imagemosaic'''
        params = dict()
        cs_url = url(self.service_url,
            ["workspaces", store.workspace.name, "coveragestores", store.name, "coverages", coverage, "index.json"], params)
        # GET /workspaces/<ws>/coveragestores/<name>/coverages/<coverage>/index.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        headers, response = self.http.request(cs_url, "GET", None, headers)
        self._cache.clear()
        schema = json.loads(response, object_hook=_decode_dict)
        return schema

    def mosaic_granules(self, coverage, store, filter=None):
        '''Print granules of an existing imagemosaic'''
        params = dict()
        if filter is not None:
            params['filter'] = filter        
        cs_url = url(self.service_url,
            ["workspaces", store.workspace.name, "coveragestores", store.name, "coverages", coverage, "index/granules.json"], params)
        # GET /workspaces/<ws>/coveragestores/<name>/coverages/<coverage>/index/granules.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }
        headers, response = self.http.request(cs_url, "GET", None, headers)
        self._cache.clear()
        granules = json.loads(response, object_hook=_decode_dict)
        return granules

    def publish_featuretype(self, name, store, native_crs, srs=None):
        '''Publish a featuretype from data in an existing store'''
        # @todo native_srs doesn't seem to get detected, even when in the DB
        # metadata (at least for postgis in geometry_columns) and then there
        # will be a misconfigured layer
        if native_crs is None: raise ValueError("must specify native_crs")
        srs = srs or native_crs
        feature_type = FeatureType(self, store.workspace, store, name)
        # because name is the in FeatureType base class, work around that
        # and hack in these others that don't have xml properties
        feature_type.dirty['name'] = name
        feature_type.dirty['srs'] = srs
        feature_type.dirty['nativeCRS'] = native_crs
        feature_type.enabled = True
        feature_type.title = name
        headers = {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }
        headers, response = self.http.request(store.resource_url, "POST", feature_type.message(), headers)
        feature_type.fetch()
        return feature_type

    def get_resource(self, name, store=None, workspace=None):
        if store is not None and workspace is not None:
            if isinstance(workspace, basestring):
                workspace = self.get_workspace(workspace)
            if isinstance(store, basestring):
                store = self.get_store(store, workspace)
            if store is not None:
                return store.get_resources(name)
        
        if store is not None:
            candidates = [s for s in self.get_resources(store) if s.name == name]
            if len(candidates) == 0:
                return None
            elif len(candidates) > 1:
                raise AmbiguousRequestError
            else:
                return candidates[0]

        if workspace is not None:
            for store in self.get_stores(workspace):
                resource = self.get_resource(name, store)
                if resource is not None:
                    return resource
            return None

        for ws in self.get_workspaces():
            resource = self.get_resource(name, workspace=ws)
            if resource is not None:
                return resource
        return None

    def get_resource_by_url(self, url):
        xml = self.get_xml(url)
        name = xml.find("name").text
        resource = None
        if xml.tag == 'featureType':
            resource = FeatureType
        elif xml.tag == 'coverage':
            resource = Coverage
        else:
            raise Exception('drat')
        return resource(self, None, None, name, href=url)

    def get_resources(self, store=None, workspace=None):
        if isinstance(workspace, basestring):
            workspace = self.get_workspace(workspace)
        if isinstance(store, basestring):
            store = self.get_store(store, workspace)
        if store is not None:
            return store.get_resources()
        if workspace is not None:
            resources = []
            for store in self.get_stores(workspace):
                resources.extend(self.get_resources(store))
            return resources
        resources = []
        for ws in self.get_workspaces():
            resources.extend(self.get_resources(workspace=ws))
        return resources

    def get_layer(self, name):
        try:
            lyr = Layer(self, name)
            lyr.fetch()
            return lyr
        except FailedRequestError:
            return None

    def get_layers(self, resource=None):
        if isinstance(resource, basestring):
            resource = self.get_resource(resource)
        layers_url = url(self.service_url, ["layers.xml"])
        description = self.get_xml(layers_url)
        lyrs = [Layer(self, l.find("name").text) for l in description.findall("layer")]
        if resource is not None:
            lyrs = [l for l in lyrs if l.resource.href == resource.href]
        # TODO: Filter by style
        return lyrs

    def get_layergroup(self, name=None):
        try: 
            group_url = url(self.service_url, ["layergroups", name + ".xml"])
            group = self.get_xml(group_url)
            return LayerGroup(self, group.find("name").text)
        except FailedRequestError:
            return None

    def get_layergroups(self):
        groups = self.get_xml("%s/layergroups.xml" % self.service_url)
        return [LayerGroup(self, g.find("name").text) for g in groups.findall("layerGroup")]

    def create_layergroup(self, name, layers = (), styles = (), bounds = None):
        if any(g.name == name for g in self.get_layergroups()):
            raise ConflictingDataError("LayerGroup named %s already exists!" % name)
        else:
            return UnsavedLayerGroup(self, name, layers, styles, bounds)

    def get_style(self, name, workspace=None):
        '''Find a Style in the catalog if one exists that matches the given name.
        If name is fully qualified in the form of `workspace:name` the workspace
        may be ommitted.

        :param name: name of the style to find
        :param workspace: optional workspace to search in
        '''
        style = None
        if ':' in name:
            workspace, name = name.split(':', 1)
        try:
            style = Style(self, name, _name(workspace))
            style.fetch()
        except FailedRequestError:
            style = None
        return style

    def get_style_by_url(self, style_workspace_url):
        try:
            dom = self.get_xml(style_workspace_url)
        except FailedRequestError:
            return None
        rest_parts = style_workspace_url.replace(self.service_url, '').split('/')
        # check for /workspaces/<ws>/styles/<stylename>
        workspace = None
        if 'workspaces' in rest_parts:
            workspace = rest_parts[rest_parts.index('workspaces') + 1]
        return Style(self, dom.find("name").text, workspace)

    def get_styles(self):
        styles_url = url(self.service_url, ["styles.xml"])
        description = self.get_xml(styles_url)
        return [Style(self, s.find('name').text) for s in description.findall("style")]

    def create_style(self, name, data, overwrite = False, workspace=None):
        style = self.get_style(name, workspace)
        if not overwrite and style is not None:
            raise ConflictingDataError("There is already a style named %s" % name)

        if not overwrite or style is None:
            headers = {
                "Content-type": "application/xml",
                "Accept": "application/xml"
            }
            xml = "<style><name>{0}</name><filename>{0}.sld</filename></style>".format(name)
            style = Style(self, name, workspace)
            headers, response = self.http.request(style.create_href, "POST", xml, headers)
            if headers.status < 200 or headers.status > 299: raise UploadError(response)

        headers = {
            "Content-type": "application/vnd.ogc.sld+xml",
            "Accept": "application/xml"
        }

        headers, response = self.http.request(style.body_href(), "PUT", data, headers)
        if headers.status < 200 or headers.status > 299: raise UploadError(response)

        self._cache.pop(style.href, None)
        self._cache.pop(style.body_href(), None)

    def create_workspace(self, name, uri):
        xml = ("<namespace>"
            "<prefix>{name}</prefix>"
            "<uri>{uri}</uri>"
            "</namespace>").format(name=name, uri=uri)
        headers = { "Content-Type": "application/xml" }
        workspace_url = self.service_url + "/namespaces/"

        headers, response = self.http.request(workspace_url, "POST", xml, headers)
        assert 200 <= headers.status < 300, "Tried to create workspace but got " + str(headers.status) + ": " + response
        self._cache.pop("%s/workspaces.xml" % self.service_url, None)
        return self.get_workspace(name)

    def get_workspaces(self):
        description = self.get_xml("%s/workspaces.xml" % self.service_url)
        return [workspace_from_index(self, node) for node in description.findall("workspace")]

    def get_workspace(self, name):
        candidates = [w for w in self.get_workspaces() if w.name == name]
        if len(candidates) == 0:
            return None
        elif len(candidates) > 1:
            raise AmbiguousRequestError()
        else:
            return candidates[0]

    def get_default_workspace(self):
        ws = Workspace(self, "default")
        # must fetch and resolve the 'real' workspace from the response
        ws.fetch()
        return workspace_from_index(self, ws.dom)

    def set_default_workspace(self, name):
        if hasattr(name, 'name'):
            name = name.name
        workspace = self.get_workspace(name)
        if workspace is not None:
            headers = { "Content-Type": "application/xml" }
            default_workspace_url = self.service_url + "/workspaces/default.xml"
            msg = "<workspace><name>%s</name></workspace>" % name
            headers, response = self.http.request(default_workspace_url, "PUT", msg, headers)
            assert 200 <= headers.status < 300, "Error setting default workspace: " + str(headers.status) + ": " + response
            self._cache.pop(default_workspace_url, None)
            self._cache.pop("%s/workspaces.xml" % self.service_url, None)
        else:
            raise FailedRequestError("no workspace named '%s'" % name)
