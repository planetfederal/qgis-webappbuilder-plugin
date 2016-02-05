from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geolocation(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append("<div id='geolocation-control' className='ol-unselectable ol-control'><Geolocation map={map} /></div>")
        app.panelsjs.append('''React.createElement("div", {id:'geolocation-control', className:'ol-unselectable ol-control'},
                                    React.createElement(Geolocation, {map:map})
                                  )''')
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geolocation.png"))

    def description(self):
        return "Geolocation"