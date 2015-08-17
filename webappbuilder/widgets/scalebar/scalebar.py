from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json

class ScaleBar(WebAppWidget):

    _parameters = {"minWidth": 64,
                   "units": ("metric", ("metric", "degrees", "imperial", "nautical", "us"))
                  }

    def write(self, appdef, folder, app, progress):
        app.controls.append("new ol.control.ScaleLine(%s)" % json.dumps(self._parameters))
        self.addCss("scalebar.css", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "scale-bar.png"))

    def description(self):
        return "Scalebar"