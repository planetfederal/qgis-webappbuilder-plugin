from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ExportAsImage(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('<li><a onclick="saveAsPng()" href="#" id="export-as-image"><i class="glyphicon glyphicon-camera"></i>Export as image</a></li>')
        self.addScript("savepng.js", folder, app)
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "export-as-image.png"))

    def description(self):
        return "Export image"