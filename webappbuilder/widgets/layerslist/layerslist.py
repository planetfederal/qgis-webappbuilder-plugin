from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json

class LayersList(WebAppWidget):

    _parameters = {"tipLabel": "Layers",
                    "showOpacity": False,
                    "showZoomTo": False,
                    "showDownload": False,
                    "allowReordering": False,
                    "allowFiltering": True,
                    "expandOnHover": True}

    def write(self, appdef, folder, app, progress):
        self.addCss("layerslist.css", folder, app)
        app.controls.append("new ol.control.LayerSwitcher(%s)" % json.dumps(self._parameters))
        self.addScript("layerslist.js", folder, app)
        if self._parameters["showOpacity"]:
            self.addScript("bootstrap-slider.js", folder, app)
            self.addCss("slider.css", folder, app)
            app.scripts.append('<script src="./resources/bootstrap-slider.js"></script>')
        if self._parameters["allowFiltering"]:
            self.addScript("bootbox.min.js", folder, app)
            self.addScript("filtrex.js", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "layer-list.png"))

    def description(self):
        return "Layers list"
