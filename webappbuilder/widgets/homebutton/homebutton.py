from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class HomeButton(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("homebutton.js", folder, app)
        app.controls.append("new ol.control.HomeButton()")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "home.png"))

    def description(self):
        return "Home"