from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    order = 1

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        self.addReactComponent(app, "Geocoding")
        self.addReactComponent(app, "GeocodingResults")
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append("<UI.Tab eventKey={%i} title='Geocoding'><div id='geocoding-tab'><Geocoding />" % idx
                          + "</div><div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} />"
                          + "</div></UI.Tab>" )
            app.tabsjs.append('''React.createElement(UI.Tab,{eventKey:%i, title:"Geocoding"},
                                    React.createElement("div", {id:"geocoding-tab"},
                                        React.createElement(Geocoding, {})
                                    ),
                                    React.createElement("div", {id:"geocoding-results"},
                                        React.createElement(GeocodingResults, {map:map})
                                    )
                                )''' % idx)
        else:
            app.mappanels.append("<div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} /></div>")
            app.mappanelsjs.append('''React.createElement("div", {id:'geocoding-results', className:'geocoding-results'},
                                    React.createElement(GeocodingResults, {map:map})
                                  )''')
            app.tools.append(" <ul id='geocoding' className='pull-right'><Geocoding /></ul>")
            app.toolsjs.append('''React.createElement("ul", {id:'geocoding', className:'pull-right'},
                                    React.createElement(Geocoding, {})
                                  )''')
        self.copyToResources("marker.png", folder)


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def description(self):
        return "Geocoding"