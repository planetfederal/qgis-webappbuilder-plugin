import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class ZoomSlider(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement("div", {id:'zoom-slider'},
                                    React.createElement(ZoomSlider, {map:map})
                                  )''')
        self.addReactComponent(app, "ZoomSlider")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "zoom-slider.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "zoom-slider.png")

    def description(self):
        return "Zoom slider"
