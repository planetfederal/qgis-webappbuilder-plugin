from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append("<UI.Tab eventKey={1} title='Geocoding'><div id='geocoding-tab'><Geocoding /></div><div id='geocoding-results' className='geocoding-results'><GeocodingResults map={map} /></div></UI.Tab>")
        self.copyToResources("marker.png", folder)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def description(self):
        return "Geocoding"