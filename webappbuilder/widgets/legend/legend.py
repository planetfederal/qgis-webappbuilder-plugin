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
        self.writeLegendFiles(appdef, app, folder)
        app.controls.append("<div id='legend'><QGISLegend map={map} legendBasePath='./resources/legend/' legendData={legendData} /></div>")

    def description(self):
        return "Legend"

    def writeLegendFiles(self, appdef, app, folder):
        layers = appdef["Layers"]
        legend = {}
        legendFolder = os.path.join(folder, "resources", "legend")
        if not QDir(legendFolder).exists():
            QDir().mkpath(legendFolder)
        for ilayer, applayer in enumerate(layers):
            if applayer.showInControls:
                layer = applayer.layer
                symbols = self.getLegendSymbols(layer, ilayer, legendFolder)
                if symbols:
                    legend[layer.id()] = symbols

        app.variables.append("var legendData = %s;" % json.dumps(legend))

    def getLegendSymbols(self, layer, ilayer, legendFolder):
        size = 20
        qsize = QSize(size, size)
        symbols = []
        def appendSymbol(title, href):
            symbols.append({'title': title, 'href':href})
        if layer.type() == layer.VectorLayer:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                    img = renderer.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_0.png" % (ilayer))
                    img.save(symbolPath)
                    appendSymbol("",  os.path.basename(symbolPath))
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                for isymbol, cat in enumerate(renderer.categories()):
                    img = cat.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_%i.png" % (ilayer, isymbol))
                    img.save(symbolPath)
                    appendSymbol(cat.label(), os.path.basename(symbolPath))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                for isymbol, ran in enumerate(renderer.ranges()):
                    img = ran.symbol().asImage(qsize)
                    symbolPath = os.path.join(legendFolder, "%i_%i.png" % (ilayer, isymbol))
                    img.save(symbolPath)
                    appendSymbol("%s-%s" % (ran.lowerValue(), ran.upperValue()), os.path.basename(symbolPath))
        elif layer.providerType() == "wms":
            source = layer.source()
            layerName = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
            url = re.search(r"url=(.*?)\?", source).groups(0)[0]
            styles = re.search(r"styles=(.*?)(?:&|$)", source).groups(0)[0]
            fullUrl = ("%s?LAYER=%s&STYLES=%s&REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=%i&HEIGHT=%i"
                       % (url, layerName, styles, size, size))
            response = requests.get(fullUrl, stream=True)
            symbolPath = os.path.join(legendFolder, "%i_0.png" % ilayer)
            with open(symbolPath, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            del response
            appendSymbol("", os.path.basename(symbolPath))
        return symbols