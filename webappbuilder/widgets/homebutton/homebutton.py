from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class HomeButton(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.controls.append("<div id='home-button' className='ol-unselectable ol-control'><HomeButton map={map} /></div>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "home.png"))

    def description(self):
        return "Home"