from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import METHOD_WMS

class AttributesTable(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('<li><a onclick="showAttributesTable()" href="#"><i class="glyphicon glyphicon-list-alt"></i>Attributes table</a></li>')
        app.panels.append('<div class="attributes-table"><a href="#" id="attributes-table-closer" class="attributes-table-closer">Close</a></div>')
        self.addScript("attributestable.js", folder, app)

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