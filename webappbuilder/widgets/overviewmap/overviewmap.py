from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from webappbuilder.utils import safeName

class OverviewMap(WebAppWidget):

    overviewPanelBaseLayers = []
    #TODO
    _parameters = {"Base layer": ("Use main map base layer", overviewPanelBaseLayers),
                    "Collapsed":True}

    def write(self, appdef, folder, app, progress):
        layers = appdef["Layers"]
        collapsed = str(self._parameters["Collapsed"]).lower()
        overviewLayers = ",".join(["lyr_%s" % safeName(layer.layer.name())
                        for layer in layers if layer.showInOverview])
        app.controls.append("new ol.control.OverviewMap({collapsed: %s, layers: [overviewMapBaseLayer, %s]})"
                        % (collapsed, overviewLayers))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "overview-map.png"))

    def description(self):
        return "Overview map"
