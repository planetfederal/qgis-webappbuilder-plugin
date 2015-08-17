from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class ThreeDView(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("cesium-control.js", folder, app)
        self.addScript("Cesium.js", folder, app)
        self.addScript("ol3cesium.js", folder, app)
        self.copyToResources("exports.js", folder)
        self.copyToResources("ol3cesium.js.map", folder)
        app.postmap.append('''var ol3d = new olcs.OLCesium({map: map});
                    var scene = ol3d.getCesiumScene();
                    var terrainProvider = new Cesium.CesiumTerrainProvider({
                        url : '//cesiumjs.org/stk-terrain/tilesets/world/tiles'
                    });
                    scene.terrainProvider = terrainProvider;
                    map.addControl(new ol.control.CesiumControl(ol3d))''')


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "3d-view.png"))

    def description(self):
        return "3D view"