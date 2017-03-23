from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ZoomControls(WebAppWidget):

    _parameters = {"duration": 250, "zoomInTipLabel": "Zoom in", "zoomOutTipLabel": "Zoom out", "delta": 1.2}

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement("div", {id:'zoom-buttons'},
                                    React.createElement(Zoom, {
                                    duration:%s,
                                    zoomInTipLabel: '%s',
                                    zoomOutTipLabel: '%s',
                                    delta: %s,
                                    map: map,
                                    tooltipPosition: 'bottom-right'})
                                  )''' % (self._parameters["duration"], self._parameters["zoomInTipLabel"],
                                          self._parameters["zoomOutTipLabel"], self._parameters["delta"]))
        self.addReactComponent(app, "Zoom")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "zoom-controls.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "zoom-controls.png")

    def description(self):
        return "Zoom controls"
