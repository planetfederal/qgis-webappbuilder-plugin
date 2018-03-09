from webappbuilder.webbappwidget import WebAppWidget
import os
from qgis.PyQt.QtGui import QIcon
import json

class ScaleBar(WebAppWidget):

    _parameters = {"minWidth": 64,
                   "units": ("metric", ("metric", "degrees", "imperial", "nautical", "us"))
                  }

    def write(self, appdef, folder, app, progress):
        params = {"minWidth": self._parameters["minWidth"],
                  "units": self._parameters["units"][0]}
        app.ol3controls.append("new ol.control.ScaleLine(%s)" % json.dumps(params))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "scale-bar.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "scale-bar.png")

    def description(self):
        return "Scalebar"
