from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import shutil

class ThreeDView(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        cesiumFolder = os.path.join(folder, "resources", "Cesium")
        app.scripts.append('<script src="./resources/cesium/Cesium.js"></script>')
        src = os.path.join(os.path.dirname(__file__), "Cesium")
        dst = os.path.join(cesiumFolder)
        shutil.copytree(src, dst)
        app.panels.append("<div id='globe-button' className='ol-unselectable ol-control'><Globe map={map} /></div>")
        self.addReactComponent(app, "Globe")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "3d-view.png"))

    def description(self):
        return "3D view"