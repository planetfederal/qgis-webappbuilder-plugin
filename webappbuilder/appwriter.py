import codecs
import os
import shutil
from qgis.core import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from utils import *
from settings import *
from olwriter import exportStyles, layerToJavascript
from collections import OrderedDict


def writeWebApp(appdef, folder, writeLayersData, progress):
    progress.setText("Copying resources files")
    progress.setProgress(0)
    dst = os.path.join(folder, "webapp")
    resourcesFolder = os.path.join(os.path.dirname(__file__), "sdk")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(resourcesFolder, dst)
    layers = appdef["Layers"]
    if writeLayersData:
        exportLayers(layers, dst, progress,
                     appdef["Settings"]["Precision for GeoJSON export"],
                     appdef["Settings"]["App view CRS"])

    class App():
        controls = []
        tools = []
        panels = []
        variables = []
        scripts = []
    app = App()
    exportStyles(layers, dst, appdef["Settings"], "timeline" in appdef["Widgets"], app, progress)
    writeLayersAndGroups(appdef, dst, app, progress)

    widgets = appdef["Widgets"].values()
    for w in widgets:
        w.write(appdef, dst, app, progress)

    writeCss(appdef, dst)
    writeJsx(appdef, dst, app, progress)
    indexFilepath = writeHtml(appdef, dst, app, progress)
    return indexFilepath

def writeJsx(appdef, folder, app, progress):
    layers = appdef["Layers"]
    viewCrs = appdef["Settings"]["App view CRS"]
    mapbounds = bounds(appdef["Settings"]["Extent"] == "Canvas extent", layers, viewCrs)
    mapextent = "extent: %s" % mapbounds if appdef["Settings"]["Restrict to extent"] else "center:[0,0],zoom:7"
    maxZoom = int(appdef["Settings"]["Max zoom level"])
    minZoom = int(appdef["Settings"]["Min zoom level"])
    pointZoom = str(appdef["Settings"]["Zoom level when zooming to point feature"])
    popupEvent = "pointermove" if appdef["Settings"]["Show popups on hover"] else "singleclick"

    app.variables.append("var view = new ol.View({%s, maxZoom: %d, minZoom: %d, projection: '%s'});" % (mapextent, maxZoom, minZoom, viewCrs))
    app.variables.append("var originalExtent = %s;" % mapbounds)

    logoImg = appdef["Settings"]["Logo"].strip()
    if logoImg:
        logo = '<img class="pull-left" style="margin:5px;height:calc(100%%-10px);" src="logo.png"></img>'
        ext = os.path.splitext(logoImg)[1]
        shutil.copyfile(logoImg, os.path.join(folder, "logo" + ext))
    else:
        logo = ""

    values = {"@LOGO@": logo,
                "@CONTROLS@": ",\n".join(app.controls),
                #"@POPUPEVENT@": popupEvent,
                "@PANELS@": "\n".join(app.panels),
                "@TOOLBAR@": "\n".join(app.tools),
                "@VARIABLES@": "\n".join(app.variables)}
    jsxFilepath = os.path.join(folder, "app.jsx")
    template = os.path.join(os.path.dirname(__file__), "themes",
                            appdef["Settings"]["Theme"]["Name"], "app.jsx")
    with open(jsxFilepath, "w") as f:
        f.write(replaceInTemplate(template, values))
    processJsx(jsxFilepath, progress)


def processJsx(folder, progress):
    pass

def writeCss(appdef, folder):
    cssFilepath = os.path.join(folder, "app.css")
    with open(cssFilepath, "w") as f:
        f.write(appdef["Settings"]["Theme"]["Css"])


def writeHtml(appdef, folder, app, progress):
    layers = appdef["Layers"]
    theme = appdef["Settings"]["Theme"]["Name"]
    viewCrs = appdef["Settings"]["App view CRS"]

    refresh = []
    for applayer in layers:
        layer = applayer.layer
        if applayer.refreshInterval:
            refresh.append(
            '''map.once("postcompose", function(){
                    window.setInterval(function(){
                        lyr_%s.getSource().updateParams({'dummy': Math.random()});
                    }, %s);
                  }); ''' % (safeName(layer.name()), str(applayer.refreshInterval)))
        useViewCrs = appdef["Settings"]["Use view CRS for WFS connections"]
        if layer.providerType().lower() == "wfs":
            epsg = layer.crs().authid().split(":")[-1]
            if not useViewCrs and epsg not in ["3857", "4326"]:
                app.scripts.append('<script src="./resources/proj4.js"></script>')
                app.scripts.append('<script src="http://epsg.io/%s.js"></script>' % epsg)

    if refresh:
        app.scripts.append("<script>$(document).ready(function(){%s});</script>" % "\n".join(refresh))

    viewEpsg = viewCrs.split(":")[-1]
    if viewEpsg not in ["3857", "4326"]:
            app.scripts.append('<script src="./resources/proj4.js"></script>')
            app.scripts.append('<script src="http://epsg.io/%s.js"></script>' % viewEpsg)


    values = {"@TITLE@": appdef["Settings"]["Title"],
                "@SCRIPTS@": "\n".join(OrderedDict((item,None) for item in app.scripts).keys())
            }

    template = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    html = replaceInTemplate(template, values)

    indexFilepath = os.path.join(folder, "index.html")
    try:
        from bs4 import BeautifulSoup as bs
        soup=bs(html)
        pretty=soup.prettify(formatter='html')
    except:
        pretty = html
    with open(indexFilepath, "w") as f:
        f.write(pretty)
    return indexFilepath


def writeLayersAndGroups(appdef, folder, app, progress):
    base = appdef["Base layers"]
    layers = appdef["Layers"]
    deploy = appdef["Deploy"]
    groups = appdef["Groups"]
    widgets = appdef["Widgets"]
    baseJs =[]
    for b in base:
        if b in baseLayers:
            baseJs.append(baseLayers[b])
        elif b in baseOverlays:
            baseJs.append(baseOverlays[b])
    baseLayer = "var baseLayers = [%s];" % ",".join(baseJs)


    baseLayer += "var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});"

    if "overviewmap" in widgets:
        overviewMapBaseLayerName = widgets["overviewmap"].parameters()["Base layer"]
        if overviewMapBaseLayerName == "Use main map base layer":
            baseLayer += "var overviewMapBaseLayer = baseLayersGroup"
        else:
            baseLayer += "var overviewMapBaseLayer = %s;" % baseLayers[overviewMapBaseLayerName]

    layerVars = []
    progress.setText("Writing layer definitions")
    for i, layer in enumerate(layers):
        layerTitle = layer.layer.name() if layer.showInControls else None
        layerVars.append(layerToJavascript(layer, appdef["Settings"], deploy, layerTitle))
        progress.setProgress(int((i+1)*100.0/len(layers)))
    layerVars = "\n".join(layerVars)
    groupVars = ""
    groupedLayers = {}
    for group, groupDef in groups.iteritems():
        groupLayers = groupDef["layers"]
        groupVars +=  ('''var %s = new ol.layer.Group({
                                layers: [%s],
                                showContent: %s,
                                title: "%s"});\n''' %
                ("group_" + safeName(group), ",".join(["lyr_" + safeName(layer.name()) for layer in groupLayers]),
                str(groupDef["showContent"]).lower(), group))
        for layer in groupLayers:
            groupedLayers[layer.id()] = safeName(group)

    visibility = "\n".join(["lyr_%s.setVisible(%s);" % (safeName(layer.layer.name()),
                                                str(layer.visible).lower()) for layer in layers])

    layersList = []
    usedGroups = []
    for appLayer in layers:
        layer = appLayer.layer
        if layer.id() in groupedLayers:
            groupName = groupedLayers[layer.id()]
            if groupName not in usedGroups:
                layersList.append("group_" + safeName(groupName))
                usedGroups.append(groupName)
        else:
            layersList.append("lyr_" + safeName(layer.name()))

    layersList = "var layersList = [%s];" % ",".join([layer for layer in layersList])
    groupBaseLayers = appdef["Settings"]["Group base layers"]

    if base:
        if groupBaseLayers:
            layersList += "layersList.unshift(baseLayersGroup);"
        else:
            layersList += "Array.prototype.splice.apply(layersList, [0, 0].concat(baseLayers));"

    app.variables.append(baseLayer)
    app.variables.append(layerVars)
    app.variables.append(groupVars)
    app.variables.append(visibility)
    app.variables.append(layersList)


def bounds(useCanvas, layers, crsid):
    extent = None
    if useCanvas:
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, QgsCoordinateReferenceSystem(crsid))
        try:
            extent = transform.transform(canvas.extent())
        except:
            extent = None
    if extent is None:
        for layer in layers:
            transform = QgsCoordinateTransform(layer.layer.crs(), QgsCoordinateReferenceSystem(crsid))
            try:
                layerExtent = transform.transform(layer.layer.extent())
                if extent is None:
                    extent = layerExtent
                else:
                    extent.combineExtentWith(layerExtent)
            except QgsCsException:
                pass

    if extent is None:
        extent = QgsRectangle(-180, -90, 180, 90)
        transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("ESPG:4326"), QgsCoordinateReferenceSystem(crsid))
        extent = transform.transform(extent)

    return "[%f, %f, %f, %f]" % (extent.xMinimum(), extent.yMinimum(),
                                extent.xMaximum(), extent.yMaximum())

