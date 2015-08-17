from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geolocation(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.controls.append("new ol.control.Geolocation()")
        self.addScript("geolocation.js", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geolocation.png"))

    def description(self):
        return "Geolocation"