from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geolocation(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement("div", {id:'geolocation-control'},
                                    React.createElement(Geolocation, {map:map})
                                  )''')
        self.addReactComponent(app, "Geolocation")
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geolocation.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "geolocation.png")

    def description(self):
        return "Geolocation"
