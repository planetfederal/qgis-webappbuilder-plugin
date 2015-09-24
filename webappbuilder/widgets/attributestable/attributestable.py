from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import METHOD_WMS

class AttributesTable(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append('<UI.Tab eventKey={2} title="Attributes table"><div id="attributes-table-tab"><FeatureTable layer={selectedLayer} map={map} /></div></UI.Tab>')


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "attribute-table.png"))

    def description(self):
        return "Attributes table"

    def checkProblems(self, appdef, problems):
        layers = appdef["Layers"]
        nonVectorLayers = 0
        for applayer in layers:
            layer = applayer.layer
            if layer.type() != layer.VectorLayer or applayer.method == METHOD_WMS:
                nonVectorLayers += 1

        if nonVectorLayers == len(layers):
            problems.append("Attributes table control has been added, but there are no suitable "
                            "layers to in the web app to be used with it. "
                            "Local vector layers or WFS layers are needed")