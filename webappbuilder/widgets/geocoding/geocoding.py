from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    order = 1

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append("<UI.Tab eventKey={%i} title='Geocoding'><div id='geocoding-tab'><Geocoding />" % idx
                          + "</div><div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} />"
                          + "</div></UI.Tab>" )
        else:
            app.mappanels.append("<div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} /></div>")
            app.tools.append(" <div id='geocoding' className='pull-right'><Geocoding /></div>")
        self.copyToResources("marker.png", folder)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def description(self):
        return "Geocoding"