from webappbuilder.webbappwidget import WebAppWidget
import os
from qgis.PyQt.QtGui import QIcon

class ExportAsImage(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(ImageExport, {map:map})")
        self.addReactComponent(app, "ImageExport")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "export-as-image.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "export-as-image.png")

    def description(self):
        return "Export image"
