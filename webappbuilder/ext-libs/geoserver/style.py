from geoserver.support import ResourceInfo, url, xml_property

class Style(ResourceInfo):
    def __init__(self, catalog, name, workspace=None):
        super(Style, self).__init__()
        assert isinstance(name, basestring)

        self.catalog = catalog
        self.workspace = workspace
        self.name = name
        self._sld_dom = None

    @property
    def fqn(self):
        return self.name if not self.workspace else '%s:%s' % (self.workspace, self.name)

    @property
    def href(self):
        return self._build_href('.xml')

    def body_href(self):
        return self._build_href('.sld')

    @property
    def create_href(self):
        return self._build_href('.xml', True)

    def _build_href(self, extension, create=False):
        path_parts = ["styles"]
        query = {}
        if not create:
            path_parts.append(self.name + extension)
        else:
            query['name'] = self.name
        if self.workspace is not None:
            path_parts = ["workspaces", getattr(self.workspace, 'name', self.workspace)] + path_parts
        return url(self.catalog.service_url, path_parts, query)

    filename = xml_property("filename")

    def _get_sld_dom(self):
        if self._sld_dom is None:
            self._sld_dom = self.catalog.get_xml(self.body_href())
        return self._sld_dom

    @property
    def sld_title(self):
        user_style = self._get_sld_dom().find("{http://www.opengis.net/sld}NamedLayer/{http://www.opengis.net/sld}UserStyle")
        title_node = user_style.find("{http://www.opengis.net/sld}Title")
        return title_node.text if title_node is not None else None

    @property
    def sld_name(self):
        user_style = self._get_sld_dom().find("{http://www.opengis.net/sld}NamedLayer/{http://www.opengis.net/sld}UserStyle")
        name_node = user_style.find("{http://www.opengis.net/sld}Name")
        return name_node.text if name_node is not None else None

    @property
    def sld_body(self):
        content = self.catalog.http.request(self.body_href())[1]
        return content

    def update_body(self, body):
        headers = { "Content-Type": "application/vnd.ogc.sld+xml" }
        self.catalog.http.request(
            self.body_href(), "PUT", body, headers)
