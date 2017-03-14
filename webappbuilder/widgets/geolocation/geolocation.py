from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geolocation(WebAppWidget):
    
    levels = ["Current zoom"]
    levels.extend((str(s) for s in range(1,25)))
    _parameters = {"zoom": ("Current zoom", tuple(levels))}
    
    def write(self, appdef, folder, app, progress):
        try:
            zoom = "zoom: %i" % int(self._parameters["zoom"])
        except:
            zoom =""
        app.panels.append('''React.createElement("div", {id:'geolocation-control'},
                                    React.createElement(Geolocation, {map:map%s})
                                  )''' % zoom)
        self.addReactComponent(app, "Geolocation")
        
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geolocation.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "geolocation.png")

    def description(self):
        return "Geolocation"
