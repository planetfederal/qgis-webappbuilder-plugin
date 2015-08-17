from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ZoomSlider(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.controls.append("new ol.control.ZoomSlider()")
        self.addCss("zoomslider.css", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "zoom-slider.png"))

    def description(self):
        return "Zoom slider"