from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import METHOD_WMS, safeName, METHOD_WMS_POSTGIS

class AttributesTable(WebAppWidget):

    zoomLevels = list((str(i) for i in xrange(1,33)))

    _parameters = {"Zoom level when zooming to point feature": ("16", zoomLevels)}

    order = 2

    def write(self, appdef, folder, app, progress):
        layerVar = ""
        layers = appdef["Layers"]
        for applayer in layers:
            layer = applayer.layer
            if layer.type() == layer.VectorLayer and applayer.method not in [METHOD_WMS, METHOD_WMS_POSTGIS]:
                layerVar = "lyr_" + safeName(layer.name())
                break
        self.addReactComponent(app, "FeatureTable")
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append(('<UI.Tab eventKey={%i} title="Attributes table"><div id="attributes-table-tab">'
                              + '<FeatureTable layer={%s} pointZoom={%s} resizeTo="tabs-panel" offset={[50, 60]} '
                              + 'map={map} /></div></UI.Tab>')
                              % (idx, layerVar, int(self._parameters["Zoom level when zooming to point feature"][0])))
        else:
            app.tools.append("<ul className='pull-right' id='toolbar-table'><BUTTON.DefaultButton "
                             "onClick={this._toggleTable.bind(this)} title='Attributes table'>"
                             "<ICON.Icon name='list-alt' /> Table</BUTTON.DefaultButton></ul>")
            app.panels.append("<div id='table-panel' className='attributes-table'><FeatureTable resizeTo='table-panel' layer={%s} map={map} /></div>"
                              % layerVar)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "attribute-table.png"))

    def description(self):
        return "Attributes table"

    def checkProblems(self, appdef, problems):
        layers = appdef["Layers"]
        nonVectorLayers = 0
        for applayer in layers:
            layer = applayer.layer
            if layer.type() != layer.VectorLayer or applayer.method in [METHOD_WMS, METHOD_WMS_POSTGIS]:
                nonVectorLayers += 1

        if nonVectorLayers == len(layers):
            problems.append("Attributes table control has been added, but there are no suitable "
                            "layers to in the web app to be used with it. "
                            "Local vector layers or WFS layers are needed")