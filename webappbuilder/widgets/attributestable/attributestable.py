from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import METHOD_WMS, safeName, METHOD_WMS_POSTGIS

class AttributesTable(WebAppWidget):

    zoomLevels = list((str(i) for i in xrange(1,33)))

    _parameters = {"Zoom level when zooming to point feature": ("16", zoomLevels)}

    def write(self, appdef, folder, app, progress):
        layerVar = ""
        layers = appdef["Layers"]
        for applayer in layers:
            layer = applayer.layer
            if layer.type() == layer.VectorLayer and applayer.method not in [METHOD_WMS, METHOD_WMS_POSTGIS]:
                layerVar = "lyr_" + safeName(layer.name())
                break
        app.panels.append('<UI.Tab eventKey={2} title="Attributes table"><div id="attributes-table-tab">'
                          + '<FeatureTable layer={%s} pointZoom=%s map={map} /></div></UI.Tab>'
                          % (layerVar, str(self.parameters["Zoom level when zooming to point feature"])))


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