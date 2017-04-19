from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ZoomToLatLon(WebAppWidget):

    order = 1

    def write(self, appdef, folder, app, progress):
        self.addReactComponent(app, "ZoomToLatLon")
        app.tools.append('''React.createElement(ZoomToLatLon, {map:map})''')


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "zoomtolatlon.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "zoomtolatlon.png")

    def description(self):
        return "Zoom to lat/lon"
