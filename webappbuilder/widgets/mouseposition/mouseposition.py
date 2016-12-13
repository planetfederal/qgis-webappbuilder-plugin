from __future__ import print_function
import os
import json
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class MousePosition(WebAppWidget):

    _parameters = {"projection": "EPSG:4326",
                   "coordinateFormat": ("Lat/Lon", ("Lat/Lon", "MGRS")),
                   "undefinedHTML": "&nbsp;"}

    def write(self, appdef, folder, app, progress):
        projection = self._parameters["projection"]
        epsg = projection.split(":")[-1]
        if epsg not in ["3857", "4326"]:
            app.scripts.append('<script src="./resources/js/proj4.js"></script>')
            app.scripts.append('<script src="http://epsg.io/%s.js"></script>' % epsg)
        coord = self._parameters["coordinateFormat"][0]
        params = self._parameters.copy()
        del params["coordinateFormat"]
        if coord == 'MGRS':
            app.scripts.append('<script src="./resources/js/mgrs.js"></script>')
            fmt  = "function(coordinate) {return mgrs.forward(coordinate);}"
        else:
            fmt = "ol.coordinate.createStringXY(4)"
        s = json.dumps(params)
        print(s)
        s = s[:-1] + ', "coordinateFormat": {}'.format(fmt) + s[-1]
        print(s)
        s = s.replace('"%s"' % fmt, fmt)
        app.ol3controls.append("new ol.control.MousePosition(%s)" % s)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "mouse-position.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "mouse-position.png")

    def description(self):
        return "Mouse position"
