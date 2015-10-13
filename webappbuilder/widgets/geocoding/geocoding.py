from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    order = 1

    def write(self, appdef, folder, app, progress):
        idx = len(app.panels) + 1
        app.panels.append("<UI.Tab eventKey={%i} title='Geocoding'><div id='geocoding-tab'><Geocoding />" % idx
                          + "</div><div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} />"
                          + "</div></UI.Tab>" )
        self.copyToResources("marker.png", folder)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def description(self):
        return "Geocoding"