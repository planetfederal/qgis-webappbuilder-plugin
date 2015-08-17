from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class AddLayer(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('<li><a onclick="addLayerFromFile()" href="#"><i class="glyphicon glyphicon-open"></i>Add layer</a></li>')
        self.addScript("addlayer.js", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "add-layer.png"))

    def description(self):
        return "Add layer"