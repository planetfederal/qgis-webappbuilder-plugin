from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json

class ZoomControls(WebAppWidget):

    _parameters = {"duration": 250, "zoomInLabel": "+", "zoomOutLabel": "-",
                    "zoomInTipLabel": "Zoom in", "zoomOutTipLabel": "Zoom out", "delta": 1.2}

    def write(self, appdef, folder, app, progress):
        app.controls.append("new ol.control.Zoom(%s)" % json.dumps(self._parameters))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "zoom-controls.png"))

    def description(self):
        return "Zoom controls"