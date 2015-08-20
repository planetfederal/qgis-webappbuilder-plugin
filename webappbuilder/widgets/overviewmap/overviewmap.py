from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import safeName
from webappbuilder.settings import *
from webappbuilder.settings import baseLayers

class OverviewMap(WebAppWidget):

    def __init__(self):
        overviewPanelBaseLayers = ["Use main map base layer"]
        overviewPanelBaseLayers.extend(baseLayers.keys())
        self._parameters = {"Base layer": ("Use main map base layer", overviewPanelBaseLayers),
                    "Collapsed":True}
        self.defaultParameters = self._parameters.copy()

    def write(self, appdef, folder, app, progress):
        layers = appdef["Layers"]
        collapsed = str(self._parameters["Collapsed"]).lower()
        overviewLayers = ",".join(["lyr_%s" % safeName(layer.layer.name())
                        for layer in layers if layer.showInOverview])
        app.controls.append("new ol.control.OverviewMap({collapsed: %s, layers: [overviewMapBaseLayer, %s]})"
                        % (collapsed, overviewLayers))
        self.addCss("overviewmap.css", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "overview-map.png"))

    def description(self):
        return "Overview map"
