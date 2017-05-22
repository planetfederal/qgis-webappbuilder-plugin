from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    order = 1

    _parameters = {"maxResults": 5, "zoom": 10}

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        self.addReactComponent(app, "Geocoding")
        self.addReactComponent(app, "GeocodingResults")
        maxResults = int(self._parameters["maxResults"])
        zoom = int(self._parameters["zoom"])
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(Tab,{key:%i, value:%i, label:"Geocoding"},
                                    React.createElement("div", {id:"geocoding-tab"},
                                        React.createElement(Geocoding, {maxResults:%i})
                                    ),
                                    React.createElement("div", {id:"geocoding-results"},
                                        React.createElement(GeocodingResults, {map:map,
                                        zoom:%i})
                                    )
                                )''' % (idx, idx, maxResults, zoom))
        else:
            app.mappanels.append('''React.createElement("div", {id:'geocoding-results', className:'geocoding-results-panel'},
                                    React.createElement(GeocodingResults, {map:map, zoom:%i})
                                  )''' % zoom)
            app.tools.append('''React.createElement("div", {id:'geocoding'},
                                        React.createElement(Geocoding, {maxResults:%i}))''' % maxResults)
        self.copyToResources("marker.png", folder)


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "geocoding.png")

    def description(self):
        return "Geocoding"
