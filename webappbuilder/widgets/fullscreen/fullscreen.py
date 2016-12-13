import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class FullScreen(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.ol3controls.append("new ol.control.FullScreen()")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "full-screen.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "full-screen.png")

    def description(self):
        return "Full screen"
