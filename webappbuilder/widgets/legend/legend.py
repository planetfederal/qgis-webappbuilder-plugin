from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from PyQt4.Qt import QDir, QSize
from qgis.core import *
import json
import re
import requests
import shutil

class Legend(WebAppWidget):

    _parameters = {"showExpandedOnStartup": False, "expandOnHover": True}

    def write(self, appdef, folder, app, progress):
        self.addCss("legend.css", folder, app)
        app.scripts.append('<script src="./legend/legend.js"></script>')
        self.addScript("legend.js", folder, app)
        self.writeLegendFiles(appdef, folder)
        app.controls.append("new ol.control.Legend(%s)" % json.dumps(self._parameters))

    def description(self):
        return "Legend"

    def writeLegendFiles(self, appdef, folder):
        layers = appdef["Layers"]
        legend = {}
        legendFolder = os.path.join(folder, "legend")
        if not QDir(legendFolder).exists():
            QDir().mkpath(legendFolder)
        for ilayer, applayer in enumerate(layers):
            if applayer.showInControls:
                layer = applayer.layer
                symbols = self.getLegendSymbols(layer, ilayer, legendFolder)
                if symbols:
                    legend[layer.name()] = symbols

        with open(os.path.join(legendFolder, "legend.js"), "w") as f:
            f.write("var legendData = %s;" % json.dumps(legend))

    def getLegendSymbols(self, layer, ilayer, legendFolder):
        size = 20
        qsize = QSize(size, size)
        symbols = []
        if layer.type() == layer.VectorLayer:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                    img = renderer.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_0.png" % (ilayer))
                    img.save(symbolPath)
                    symbols.append(("", os.path.basename(symbolPath)))
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                for isymbol, cat in enumerate(renderer.categories()):
                    img = cat.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_%i.png" % (ilayer, isymbol))
                    img.save(symbolPath)
                    symbols.append((cat.label(), os.path.basename(symbolPath)))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                for isymbol, ran in renderer.ranges():
                    img = ran.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_%i.png" % (ilayer, isymbol))
                    img.save(symbolPath)
                    symbols.append(("%s-%s" % (ran.lowerValue(), ran.upperValue()), os.path.basename(symbolPath)))
        elif layer.providerType() == "wms":
            source = layer.source()
            layerName = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
            url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0]
            styles = re.search(r"styles=(.*?)(?:&|$)", source).groups(0)[0]
            fullUrl = ("%s?LAYER=%s&STYLES=%s&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=%i&HEIGHT=%i"
                       % (url, layerName, styles, size, size))
            response = requests.get(fullUrl, stream=True)
            symbolPath = os.path.join(legendFolder, "%i_0.png" % ilayer)
            with open(symbolPath, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            del response
            symbols.append(("", os.path.basename(symbolPath)))
        return symbols