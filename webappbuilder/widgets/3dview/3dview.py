from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import shutil
from PyQt4.QtCore import QDir

class ThreeDView(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        cesiumFolder = os.path.join(folder, "resources", "cesium")
        app.scripts.append('<script src="./resources/cesium/Cesium.js"></script>')
        QDir().mkpath(cesiumFolder)
        src = os.path.join(os.path.dirname(__file__), "Cesium.js")
        dst = os.path.join(cesiumFolder, "Cesium.js")
        shutil.copy2(src, dst)
        src = os.path.join(os.path.dirname(__file__), "Assets")
        dst = os.path.join(cesiumFolder, "Assets")
        shutil.copytree(src, dst)
        app.panels.append("<div id='globe-button' className='ol-unselectable ol-control'><Globe map={map} /></div>")


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "3d-view.png"))

    def description(self):
        return "3D view"