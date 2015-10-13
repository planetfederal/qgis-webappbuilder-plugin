from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ThreeDView(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append("<div id='globe-button' className='ol-unselectable ol-control'><Globe map={map} /></div>")


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "3d-view.png"))

    def description(self):
        return "3D view"