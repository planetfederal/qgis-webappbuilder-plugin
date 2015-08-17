from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class NorthArrow(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.controls.append("new ol.control.Rotate({autoHide: false})")
        self.addCss("northarrow.css", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "north-arrow.png"))

    def description(self):
        return "North"