import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class Geocoding(WebAppWidget):

    order = 1

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        self.addReactComponent(app, "Geocoding")
        self.addReactComponent(app, "GeocodingResults")
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(Tab,{value:%i, label:"Geocoding"},
                                    React.createElement("div", {id:"geocoding-tab"},
                                        React.createElement(Geocoding, {})
                                    ),
                                    React.createElement("div", {id:"geocoding-results"},
                                        React.createElement(GeocodingResults, {map:map})
                                    )
                                )''' % idx)
        else:
            app.mappanels.append('''React.createElement("div", {id:'geocoding-results', className:'geocoding-results-panel'},
                                    React.createElement(GeocodingResults, {map:map})
                                  )''')
            app.tools.append('''React.createElement("div", {id:'geocoding', className:'pull-right'},
                                        React.createElement(Geocoding, {}))''')
        self.copyToResources("marker.png", folder)


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "geocoding.png")

    def description(self):
        return "Geocoding"
