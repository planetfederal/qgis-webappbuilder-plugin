from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geolocation(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.controls.append("<div id='geolocation-control' className='ol-unselectable ol-control'><Geolocation map={map} /></div>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geolocation.png"))

    def description(self):
        return "Geolocation"