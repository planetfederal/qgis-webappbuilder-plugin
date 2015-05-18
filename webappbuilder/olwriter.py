import codecs
import os
import re
import math
import shutil
from qgis.core import *
from qgis.utils import iface
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from utils import *
from settings import *
import json
from bs4 import BeautifulSoup as bs
import importlib
from math import floor


dragBoxConditions = {"Not enabled": "ol.events.condition.never",
                     "Using Alt key": "ol.events.condition.altKeyOnly",
                     "Using Shift key": "ol.events.condition.shiftKeyOnly",
                     "Without using additional key": "ol.events.condition.noModifierKeys"}

def writeOL(appdef, folder, writeLayersData, progress):
    progress.setText("Creating local files (3/3)")
    progress.setProgress(0)
    dst = os.path.join(folder, "resources")
    resourcesFolder = os.path.join(os.path.dirname(__file__), "resources")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(resourcesFolder, dst)
    layers = appdef["Layers"]
    if writeLayersData:
        exportLayers(layers, folder, progress, appdef["Settings"]["Precision for GeoJSON export"])
    exportStyles(layers, folder, appdef["Settings"])
    writeLayersAndGroups(appdef, folder)
    popupLayers = "popupLayers = [%s];" % ",".join(["'%s'" % layer.popup for layer in layers])
    controls = []
    widgets = appdef["Widgets"]
    if "Scale bar" in widgets:
        controls.append("new ol.control.ScaleLine(%s)" % json.dumps(widgets["Scale bar"]))
    if "Layers list" in widgets:
        controls.append("new ol.control.LayerSwitcher(%s)" % json.dumps(widgets["Layers list"]))
    if "Geolocation" in widgets:
        controls.append("new ol.control.Geolocation()")
    if "Overview map" in widgets:
        collapsed = str(widgets["Overview map"]["collapsed"]).lower()
        controls.append("new ol.control.OverviewMap({collapsed: %s})" % collapsed)
    if "Mouse position" in widgets:
        coord = str(widgets["Mouse position"]["coordinateFormat"])
        s = json.dumps(widgets["Mouse position"])
        s = s.replace('"%s"' % coord, coord)
        controls.append("new ol.control.MousePosition(%s)" % s)
    if "Home button" in widgets:
        controls.append("new ol.control.HomeButton()")
    if "Zoom slider" in widgets:
        controls.append("new ol.control.ZoomSlider()")
    if "North arrow" in widgets:
        controls.append("new ol.control.Rotate({autoHide: false})")
    if "Full screen" in widgets:
        controls.append("new ol.control.FullScreen()")
    if "Zoom controls" in widgets:
        controls.append("new ol.control.Zoom(%s)" % json.dumps(widgets["Zoom controls"]))
    if "Attribution" in widgets:
        controls.append("new ol.control.Attribution()")
    if "3D view" in widgets:
        cesium = '''var ol3d = new olcs.OLCesium({map: map});
                    var scene = ol3d.getCesiumScene();
                    var terrainProvider = new Cesium.CesiumTerrainProvider({
                        url : '//cesiumjs.org/stk-terrain/tilesets/world/tiles'
                    });
                    scene.terrainProvider = terrainProvider;
                    map.addControl(new ol.control.CesiumControl(ol3d))'''
    else:
        cesium = ""

    mapbounds = bounds(appdef["Settings"]["Extent"] == "Canvas extent", layers)
    mapextent = "extent: %s" % mapbounds if appdef["Settings"]["Restrict to extent"] else "center:[0,0],zoom:7"
    maxZoom = int(appdef["Settings"]["Max zoom level"])
    minZoom = int(appdef["Settings"]["Min zoom level"])
    onHover = str(appdef["Settings"]["Show popups on hover"]).lower()
    highlight = str(appdef["Settings"]["Highlight features on hover"]).lower()
    highlightedFeaturesStyle = appdef["Settings"]["Style for highlighted features"]
    selectedFeaturesStyle = appdef["Settings"]["Style for selected features"]
    view = "%s, maxZoom: %d, minZoom: %d" % (mapextent, maxZoom, minZoom)
    values = {"@BOUNDS@": mapbounds,
                "@CONTROLS@": ",\n".join(controls),
                "@POPUPLAYERS@": popupLayers,
                "@VIEW@": view,
                "@ONHOVER@": onHover,
                "@DOHIGHLIGHT@": highlight,
                "@CESIUM@": cesium,
                "@HIGHLIGHTSTYLE@": highlightedFeaturesStyle,
                "@SELECTIONSTYLE@": selectedFeaturesStyle}
    indexJsFilepath = os.path.join(folder, "index.js")
    template = os.path.join(os.path.dirname(__file__), "templates", "index.js")
    with open(indexJsFilepath, "w") as f:
        f.write(replaceInTemplate(template, values))

    writeCss(appdef, folder)
    indexFilepath = writeWebApp(appdef, folder)
    return indexFilepath

def writeCss(appdef, folder):
    cssFilepath = os.path.join(folder, "webapp.css")
    with open(cssFilepath, "w") as f:
        f.write(appdef["Settings"]["Theme"]["Css"])


def writeWebApp(appdef, folder):
    theme = appdef["Settings"]["Theme"]["Name"]
    try:
        module = importlib.import_module('webappbuilder.themes.%s.%s' % (theme, theme))
    except ImportError:
        return _writeWebApp(appdef, folder)
    if hasattr(module, 'writeWebApp'):
        func = getattr(module, 'writeWebApp')
        return func(appdef, folder)
    else:
        return _writeWebApp(appdef, folder)

def _writeWebApp(appdef, folder):
    layers = appdef["Layers"]
    widgets = appdef["Widgets"]
    theme = appdef["Settings"]["Theme"]["Name"]
    tools = []
    panels = []
    mappanels = []
    imports = []
    importsAfter = []
    if "Geocoding" in widgets:
        tools.append('''<div class="navbar-form navbar-right">
                          <div class="input-group">
                              <input type="text" onkeypress="searchBoxKeyPressed(event);" id="geocoding-search" class="form-control" placeholder="Search placename..."/>
                              <div class="input-group-btn">
                                  <button class="btn btn-default" "onclick="searchAddress()"><span>&nbsp;</span><i class="glyphicon glyphicon-search"></i></button>
                              </div>
                          </div>
                        </div>''');
        mappanels.append('<div id="geocoding-results" class="geocoding-results"></div>')
    if "Links" in widgets:
        links = widgets["Links"]["links"]
        for name, url in links.iteritems():
            tools.append('<li><a href="%s">%s</a></li>' % (url, name))
    if "Selection tools" in widgets:
        params = widgets["Selection tools"]
        selectTools = []
        if params["Select single feature"]:
            selectTools.append(["selectSingleFeature()", "Select single feature"])
        if params["Select by polygon"]:
            selectTools.append(["selectByPolygon()", "Select by polygon"])
        if params["Select by point and radius"]:
            selectTools.append(["selectByPointAndRadius()", "Select by point and radius"])
        if params["Select by rectangle"]:
            selectTools.append(["selectByRectangle()", "Select by rectangle"])
        if selectTools:
            li = "\n".join(['<li><a onclick="%s" href="#">%s</a></li>' % (sel[0], sel[1]) for sel in selectTools])
            tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            Selection <span class="caret"><span></a>
                            <ul class="dropdown-menu">
                              %s
                            </ul>
                          </li>''' % li)

    if "Query" in widgets:
        imports.append('''<script src="./resources/filtrex.js"></script>''')
        tools.append('<li><a onclick="showQueryPanel()" href="#"><i class="glyphicon glyphicon-filter"></i>Query</a></li>')
        mappanels.append('''<div class="query-panel" id="query-panel">
                                <form class="form-horizontal">
                                    <div style="margin-bottom: 25px" class="input-group">
                                        <span class="input-group-addon">Layer</span>
                                        <select id="query-layer" class="form-control"></select>
                                    </div>
                                    <div style="margin-bottom: 25px" class="input-group">
                                        <span class="input-group-addon">Filter </span>
                                        <input id="query-expression" type="text" class="form-control" placeholder="Type expression...">
                                    </div>
                                   <div style="margin-top:10px" class="form-group">
                                        <div class="col-sm-12 controls">
                                          <a id="btn-query-new" href="#" class="btn btn-primary">New selection</a>
                                          <a id="btn-query-add" href="#" class="btn btn-primary">Add to current selection</a>
                                          <a id="btn-query-in" href="#" class="btn btn-primary">Select in current selection</a>
                                          <a id="btn-close-query" href="#" class="btn btn-default">Close</a>
                                        </div>
                                    </div>
                                </form>
                            </div>''')
    if "Export as image" in widgets:
        tools.append('<li><a onclick="saveAsPng()" href="#" id="export-as-image"><i class="glyphicon glyphicon-camera"></i>Export as image</a></li>')
    if "Attributes table" in widgets:
        tools.append('<li><a onclick="showAttributesTable()" href="#"><i class="glyphicon glyphicon-list-alt"></i>Attributes table</a></li>')
        panels.append('<div class="attributes-table"><a href="#" id="attributes-table-closer" class="attributes-table-closer">Close</a></div>')
    if "Measure tool" in widgets:
        tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Measure <span class="caret"><span> </a>
                            <ul class="dropdown-menu">
                              <li><a onclick="measureTool('distance')" href="#">Distance</a></li>
                              <li><a onclick="measureTool('area')" href="#">Area</a></li>
                              <li><a onclick="measureTool(null)" href="#">Remove measurements</a></li>
                            </ul>
                          </li>''')
    if "Chart tool" in widgets:
        params = widgets["Chart tool"]
        li = "\n".join(["<li><a onclick=\"openChart('%s')\" href=\"#\">%s</a></li>" % (c,c) for c in params["charts"]])
        tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            <i class="glyphicon glyphicon-stats"></i> Charts <span class="caret"><span></a>
                            <ul class="dropdown-menu">
                              %s
                            </ul>
                          </li>''' % li)
        imports.append('''<script src="./resources/d3.min.js"></script>
                        <script src="./resources/c3.min.js"></script>
                        <link href="./resources/c3.min.css" rel="stylesheet" type="text/css"/>
                        <script src="./charts.js"></script>''')
        panels.append('''<div class="chart-panel" id="chart-panel">
                        <span class="chart-panel-info" id="chart-panel-info"></span>
                        <a href="#" id="chart-panel-closer" class="chart-panel-closer">Close</a>
                        <div id="chart"></div></div>''')
        chartsFilepath = os.path.join(folder, "charts.js")
        with open(chartsFilepath, "w") as f:
            f.write("var AGGREGATION_MIN = 0;")
            f.write("var AGGREGATION_MAX = 1;")
            f.write("var AGGREGATION_SUM = 2;")
            f.write("var AGGREGATION_AVG = 3;")
            f.write("var DISPLAY_MODE_FEATURE = 0;")
            f.write("var DISPLAY_MODE_CATEGORY = 1;")
            f.write("var DISPLAY_MODE_COUNT = 2;")
            f.write("var charts = " + json.dumps(params["charts"]))
    if "About panel" in widgets:
        params = widgets["About panel"]
        closer = ('<a class="closer-icon" id="closer-icon" onclick="toggleAboutPanel(false)">&times;</a>'
                 if params["isClosable"] else "")
        mappanels.append('''<div class="about-panel" id="about-panel">
                        %s
                        %s</div>''' % (closer, params["content"]))
        if params["showNavBarLink"]:
            tools.append('<li><a onclick="toggleAboutPanel(true)" href="#" id="about-panel-link">About</a></li>')
    if "Help" in widgets:
        tools.append('<li><a href="./help.html"><i class="glyphicon glyphicon-question-sign"></i>Help</a></li>')

    bookmarkEvents = ""
    if "Bookmarks" in widgets:
        params = widgets["Bookmarks"]
        bookmarks = params["bookmarks"]
        if bookmarks:
            importsAfter.append('<script src="./bookmarks.js"></script>')
            if params["format"] != SHOW_BOOKMARKS_IN_MENU:
                itemBase = '''<div class="item %s">
                              <div class="header-text hidden-xs">
                                  <div class="col-md-12 text-center">
                                      <h2>%s</h2>
                                      <p>%s</p>
                                  </div>
                              </div>
                            </div>'''
                bookmarkDivs = itemBase % ("active", params["introTitle"], params["introText"])
                bookmarkDivs += "\n".join([itemBase % ("", b[0], b[2]) for i,b in enumerate(bookmarks)])
                if params["showIndicators"]:
                    li = "\n".join(['<li data-target="#story-carousel" data-slide-to="%i"></li>' % (i+1) for i in xrange(len(bookmarks))])
                    indicators = '''<ol class="carousel-indicators">
                                        <li data-target="#story-carousel" data-slide-to="0" class="active"></li>
                                        %s
                                    </ol>''' % li
                else:
                    indicators = ""
                slide = "slide" if params["interval"] else ""
                interval = str(params["interval"] * 1000) if params["interval"] else "false"
                mappanels.append('''<div class="story-panel">
                      <div class="row">
                          <div id="story-carousel" class="carousel %s" data-interval="%s" data-ride="carousel">
                            %s
                            <div class="carousel-inner">
                                %s
                            </div>
                          </div>
                          <a class="left carousel-control" href="#story-carousel" data-slide="prev">
                              <span class="glyphicon glyphicon-chevron-left">&nbsp;</span>
                          </a>
                          <a class="right carousel-control" href="#story-carousel" data-slide="next">
                              <span class="glyphicon glyphicon-chevron-right">&nbsp;</span>
                          </a>
                      </div>
                    </div>
                    ''' % (slide, interval, indicators, bookmarkDivs))
                bookmarkEvents = '''\n$("#story-carousel").on('slide.bs.carousel', function(evt) {
                                          %sToBookmark($(evt.relatedTarget).index()-1)
                                    })''' % ["go", "pan", "fly"][params["format"]]
            else:
                li = "\n".join(["<li><a onclick=\"goToBookmarkByName('%s')\" href=\"#\">%s</a></li>" % (b[0],b[0]) for b in params["bookmarks"]])
                tools.append('''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Bookmarks <span class="caret"><span></a>
                    <ul class="dropdown-menu">
                      %s
                    </ul>
                  </li>''' % li)
            bookmarksFilepath = os.path.join(folder, "bookmarks.js")
            with open(bookmarksFilepath, "w") as f:
                bookmarksWithoutDescriptions = [b[:-1] for b in bookmarks]
                f.write("var bookmarks = " + json.dumps(bookmarksWithoutDescriptions))
                f.write(bookmarkEvents)

    imports.extend(['<script src="layers/lyr_%s.js"></script>' % (safeName(layer.layer.name()))
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])
    imports.extend(['<script src="styles/%s.js"></script>' % (safeName(layer.layer.name()))
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])

    if "Layers list" in widgets and widgets["Layers list"]["showOpacity"]:
        imports.append('<script src="./resources/bootstrap-slider.js"></script>')
        imports.append('<link href="./resources/slider.css" rel="stylesheet"/>')
    if "3D view" in widgets:
        imports.append('<script src="./resources/Cesium.js"></script>')
        imports.append('<script src="./resources/ol3cesium.js"></script>')
        dst = os.path.join(folder, "resources", "cesium")
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(os.path.dirname(__file__), "resources", "cesium"), dst)

    logoImg = appdef["Settings"]["Logo"].strip()
    if logoImg:
        logo = '<img class="pull-left" style="margin:5px;height:calc(100%%-10px);" src="logo.png"></img>'
        ext = os.path.splitext(logoImg)[1]
        shutil.copyfile(logoImg, os.path.join(folder, "logo" + ext))
    else:
        logo = ""
    values = {"@TITLE@": appdef["Settings"]["Title"],
              "@LOGO@": logo,
                "@IMPORTS@": "\n".join(imports),
                "@IMPORTSAFTER@": "\n".join(importsAfter),
                "@MAPPANELS@": "\n".join(mappanels),
                "@PANELS@": "\n".join(panels),
                "@TOOLBAR@": "\n".join(tools)}
    indexFilepath = os.path.join(folder, "index.html")
    template = os.path.join(os.path.dirname(__file__), "themes", theme, theme + ".html")
    html = replaceInTemplate(template, values)
    soup=bs(html)
    pretty=soup.prettify(formatter='html')
    with open(indexFilepath, "w") as f:
        f.write(pretty)
    return indexFilepath


def writeLayersAndGroups(appdef, folder):
    base = appdef["Base layers"]
    layers = appdef["Layers"]
    deploy = appdef["Deploy"]
    groups = appdef["Groups"]
    baseJs =[]
    for b in base:
        if b in baseLayers:
            baseJs.append(baseLayers[b])
        elif b in baseOverlays:
            baseJs.append(baseOverlays[b])
    baseLayer = "var baseLayer = new ol.layer.Group({'type': 'base', 'title': 'Base maps',layers: [%s]});" % ",".join(baseJs)
    layerVars = "\n".join([layerToJavascript(layer, appdef["Settings"], deploy) for layer in layers])
    groupVars = ""
    groupedLayers = {}
    for group, groupLayers in groups.iteritems():
        groupVars +=  ('''var %s = new ol.layer.Group({
                                layers: [%s],
                                title: "%s"});\n''' %
                ("group_" + safeName(group), ",".join(["lyr_" + safeName(layer.name()) for layer in groupLayers]),
                group))
        for layer in groupLayers:
            groupedLayers[layer.id()] = safeName(group)

    visibility = "\n".join(["lyr_%s.setVisible(%s);" % (safeName(layer.layer.name()), str(layer.visible).lower()) for layer in layers])

    layersList = ["baseLayer"] if base else []
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
    singleLayersList = "var singleLayersList = [%s];" % ",".join(["lyr_%s" % safeName(layer.layer.name()) for layer in layers])
    selectableLayersList = "var selectableLayersList = [%s];" % ",".join(
                            ["lyr_%s" % safeName(layer.layer.name()) for layer in layers if layer.allowSelection])

    path = os.path.join(folder, "layers")
    if not QDir(path).exists():
        QDir().mkpath(path)
    filename = os.path.join(path, "layers.js")
    with codecs.open(filename, "w","utf-8") as f:
        f.write(baseLayer + "\n")
        f.write(layerVars + "\n")
        f.write(groupVars + "\n")
        f.write(visibility + "\n")
        f.write(layersList + "\n")
        f.write(singleLayersList + "\n")
        f.write(selectableLayersList + "\n")




def bounds(useCanvas, layers):
    print useCanvas
    if useCanvas:
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapSettings().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, QgsCoordinateReferenceSystem("EPSG:3857"))
        try:
            extent = transform.transform(canvas.extent())
        except QgsCsException:
            extent = QgsRectangle(-20026376.39, -20048966.10, 20026376.39,20048966.10)
    else:
        extent = None
        for layer in layers:
            transform = QgsCoordinateTransform(layer.layer.crs(), QgsCoordinateReferenceSystem("EPSG:3857"))
            try:
                layerExtent = transform.transform(layer.layer.extent())
            except QgsCsException:
                layerExtent = QgsRectangle(-20026376.39, -20048966.10, 20026376.39,20048966.10)
            if extent is None:
                extent = layerExtent
            else:
                extent.combineExtentWith(layerExtent)
        extent = extent or QgsRectangle(0, 0, 0, 0)
    return "[%f, %f, %f, %f]" % (extent.xMinimum(), extent.yMinimum(),
                                extent.xMaximum(), extent.yMaximum())

def _getWfsLayer(url, title, layerName, typeName, min, max):
    return ('''var wfsSource_%(layerName)s = new ol.source.ServerVector({
                    format: new ol.format.GeoJSON(),
                    loader: function(extent, resolution, projection) {
                        var url = '%(url)s?service=WFS&version=1.1.0&request=GetFeature' +
                            '&typename=%(typeName)s&outputFormat=text/javascript&format_options=callback:loadFeatures_%(layerName)s' +
                            '&srsname=EPSG:3857&bbox=' + extent.join(',') + ',EPSG:3857';
                        $.ajax({
                            url: url,
                            dataType: 'jsonp'
                        });
                    },
                    strategy: ol.loadingstrategy.tile(new ol.tilegrid.XYZ({maxZoom: 19})),
                    projection: 'EPSG:3857'
                });

                var loadFeatures_%(layerName)s = function(response) {
                    wfsSource_%(layerName)s.addFeatures(wfsSource_%(layerName)s.readFeatures(response));
                };
                var lyr_%(layerName)s = new ol.layer.Vector({
                    source: wfsSource_%(layerName)s, %(min)s %(max)s
                    style: style_%(layerName)s,
                    title: "%(title)s"
                });''' %
                {"url": url, "title": title, "layerName":layerName, "min": min,
                 "max": max, "typeName": typeName})

def layerToJavascript(applayer, settings, deploy):
    #TODO: change scale to resolution
    scaleVisibility = settings["Use layer scale dependent visibility"]
    workspace = safeName(settings["Title"])
    layer = applayer.layer
    if scaleVisibility and layer.hasScaleBasedVisibility():
        scaleToResolution = 3571.42
        minResolution = "\nminResolution:%s,\n" % str(layer.minimumScale() / scaleToResolution)
        maxResolution = "maxResolution:%s,\n" % str(layer.maximumScale() / scaleToResolution)
    else:
        minResolution = ""
        maxResolution = ""
    layerName = safeName(layer.name())
    if layer.type() == layer.VectorLayer:
        if layer.providerType().lower() == "wfs":
            url = layer.source().split("?")[0]
            typeName = layer.name() #TODO
            return _getWfsLayer(url, layer.name(), layerName, typeName, minResolution, maxResolution)
        elif applayer.method == METHOD_FILE:
            if applayer.clusterDistance > 0 and layer.geometryType() == QGis.Point:
                return ('''var cluster_%(n)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_%(n)s)}),
                });
                var lyr_%(n)s = new ol.layer.Vector({
                    source: cluster_%(n)s, %(min)s %(max)s
                    style: style_%(n)s,
                    title: "%(name)s"
                });''' %
                {"name": layer.name(), "n":layerName, "min": minResolution,
                 "max": maxResolution, "dist": str(applayer.clusterDistance)})
            else:
                return ('''var lyr_%(n)s = new ol.layer.Vector({
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_%(n)s)}),
                    %(min)s %(max)s
                    style: style_%(n)s,
                    title: "%(name)s"
                });''' %
                {"name": layer.name(), "n":layerName, "min": minResolution,
                 "max": maxResolution})
        elif applayer.method == METHOD_WFS or applayer.method == METHOD_WFS_POSTGIS:
                #TODO:cluster
                url = deploy["GeoServer url"] + "/wfs"
                typeName = ":".join([safeName(settings["Title"]), layerName])
                return _getWfsLayer(url, layer.name(), layerName, typeName, minResolution, maxResolution)
        else:
            source = layer.source()
            layers = layer.name()
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true"},
                        })),
                        title: "%(name)s"
                      });''' % {"layers": layerName, "url": url, "n": layerName, "name": layer.name()}
    elif layer.type() == layer.RasterLayer:
        if layer.providerType().lower() == "wms":
            source = layer.source()
            layers = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
            url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0]
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true"},
                        })),
                        title: "%(name)s"
                      });''' % {"layers": layers, "url": url, "n": layerName, "name": layer.name()}
        elif applayer.method == METHOD_FILE:
            if layer.providerType().lower() == "gdal":
                provider = layer.dataProvider()
                transform = QgsCoordinateTransform(provider.crs(), QgsCoordinateReferenceSystem("EPSG:3857"))
                extent = transform.transform(provider.extent())
                sExtent = "[%f, %f, %f, %f]" % (extent.xMinimum(), extent.yMinimum(),
                                        extent.xMaximum(), extent.yMaximum())
                return '''var lyr_%(n)s = new ol.layer.Image({
                                opacity: 1,
                                title: "%(name)s",
                                source: new ol.source.ImageStatic({
                                   url: "./layers/%(n)s.jpg",
                                    projection: 'EPSG:3857',
                                    alwaysInRange: true,
                                    imageSize: [%(col)d, %(row)d],
                                    imageExtent: %(extent)s
                                })
                            });''' % {"n": layerName, "extent": sExtent, "col": provider.xSize(),
                                        "name": layer.name(), "row": provider.ySize()}
        else:
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true"},
                        })),
                        title: "%(name)s"
                      });''' % {"layers": layerName, "url": url, "n": layerName, "name": layer.name()}

def exportStyles(layers, folder, settings):
    stylesFolder = os.path.join(folder, "styles")
    QDir().mkpath(stylesFolder)
    for appLayer in layers:
        layer = appLayer.layer
        if layer.type() != layer.VectorLayer or appLayer.method == METHOD_WMS:
            continue
        labelsEnabled = str(layer.customProperty("labeling/enabled")).lower() == "true"
        if labelsEnabled:
            labelField = layer.customProperty("labeling/fieldName")
            labelText = 'feature.get("%s")' % labelField
        else:
            labelText = '""'
        defs = ""
        try:
            renderer = layer.rendererV2()
            layerTransparency = layer.layerTransparency()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                symbol = renderer.symbol()
                style = "var style = " + getSymbolAsStyle(symbol, stylesFolder, layerTransparency)
                value = 'var value = ""'
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                defs += "var categories_%s = {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(), stylesFolder,layerTransparency)))
                defs +=  ",\n".join(cats) + "};"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = categories_%s[value]'''  % (safeName(layer.name()))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                varName = "ranges_" + safeName(layer.name())
                defs += "var %s = [" % varName
                ranges = []
                for ran in renderer.ranges():
                    symbolstyle = getSymbolAsStyle(ran.symbol(), stylesFolder,layerTransparency)
                    ranges.append('[%f, %f, %s]' % (ran.lowerValue(), ran.upperValue(), symbolstyle))
                defs += ",\n".join(ranges) + "];"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = %(v)s[0][2];
                            for (i = 0; i < %(v)s.length; i++){
                                var range = %(v)s[i];
                                if (value > range[0] && value<=range[1]){
                                    style =  range[2];
                                }
                            }
                            ''' % {"v": varName}
            try:
                size = str(float(layer.customProperty("labeling/fontSize")) * 2)
            except:
                size = 1
            r = layer.customProperty("labeling/textColorR")
            g = layer.customProperty("labeling/textColorG")
            b = layer.customProperty("labeling/textColorB")
            color = "rgba(%s, %s, %s, 255)" % (r,g,b)
            if appLayer.clusterDistance > 0 and layer.type() == layer.VectorLayer and layer.geometryType() == QGis.Point:
                cluster = '''var size = feature.get('features').length;
                            if (size != 1){
                                var style = clusterStyleCache_%(name)s[size];
                                if (!style) {
                                  style = [new ol.style.Style({
                                    image: new ol.style.Circle({
                                      radius: 10,
                                      stroke: new ol.style.Stroke({
                                        color: '#fff'
                                      }),
                                      fill: new ol.style.Fill({
                                        color: '#3399CC'
                                      })
                                    }),
                                    text: new ol.style.Text({
                                      text: size.toString(),
                                      fill: new ol.style.Fill({
                                        color: '#fff'
                                      })
                                    })
                                  })];
                                  clusterStyleCache_%(name)s[size] = style;
                                }
                                return style;
                            }''' % {"name": safeName(layer.name())}
            else:
                cluster = ""

            style = '''function(feature, resolution){
                        %(cluster)s
                        %(value)s
                        %(style)s;
                        var labelText = %(label)s;
                        var key = value + "_" + labelText

                        if (!%(cache)s[key]){
                            var text = new ol.style.Text({
                                  font: '%(size)spx Calibri,sans-serif',
                                  text: labelText,
                                  fill: new ol.style.Fill({
                                    color: "%(color)s"
                                  }),
                                });
                            %(cache)s[key] = new ol.style.Style({"text": text});
                        }
                        var allStyles = [%(cache)s[key]];
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": style, "label": labelText, "cache": "textStyleCache_" + safeName(layer.name()),
                            "size": size, "color": color, "value": value, "cluster": cluster}
        except Exception, e:
            print e
            style = "{}"

        path = os.path.join(stylesFolder, safeName(layer.name()) + ".js")

        with codecs.open(path, "w","utf-8") as f:
            f.write('''%(defs)s
                    var textStyleCache_%(name)s={}
                    var clusterStyleCache_%(name)s={}
                    var style_%(name)s = %(style)s;''' %
                {"defs":defs, "name":safeName(layer.name()), "style":style})


def getRGBAColor(color, alpha):
    r,g,b,_ = color.split(",")
    return '"rgba(%s)"' % ",".join([r, g, b, str(alpha)])


def getSymbolAsStyle(symbol, stylesFolder, layerTransparency):
    styles = []
    if layerTransparency == 0:
        alpha = symbol.alpha()
    else:
        alpha = layerTransparency/float(100)
    for i in xrange(symbol.symbolLayerCount()):
        sl = symbol.symbolLayer(i)
        props = sl.properties()
        if isinstance(sl, QgsSimpleMarkerSymbolLayerV2):
            size = floor(float(props["size"]) * 3)
            color =  getRGBAColor(props["color"], alpha)
            style = "image: %s" % getCircle(color, size)
        elif isinstance(sl, QgsSvgMarkerSymbolLayerV2):
            path = os.path.join(stylesFolder, os.path.basename(sl.path()))
            shutil.copy(sl.path(), path)
            style = "image: %s" % getIcon(path, sl.size())
        elif isinstance(sl, QgsSimpleLineSymbolLayerV2):
            # Check for old version
            if 'color' in props:
                color = getRGBAColor(props["color"], alpha)
            else:
                color = getRGBAColor(props["line_color"], alpha)
            if 'width' in props:
                line_width = props["width"]
            else:
                line_width = props["line_width"]
            if 'penstyle' in props:
                line_style = props["penstyle"]
            else:
                line_style = props["line_style"]
            style = "stroke: %s" % (getStrokeStyle(color, line_style != "solid", line_width))
        elif isinstance(sl, QgsSimpleFillSymbolLayerV2):
            fillColor =  getRGBAColor(props["color"], alpha)
            # for old version
            if 'color_border' in props:
                borderColor =  getRGBAColor(props["color_border"], alpha)
            else:
                borderColor =  getRGBAColor(props["outline_color"], alpha)
            if 'style_border' in props:
                borderStyle = props["style_border"]
            else:
                borderStyle = props["outline_style"]
            if 'width_border' in props:
                borderWidth = props["width_border"]
            else:
                borderWidth = props["outline_width"]
            style = ('''stroke: %s,
                        fill: %s''' %
                    (getStrokeStyle(borderColor, borderStyle != "solid", borderWidth),
                     getFillStyle(fillColor)))
        else:
            style = ""
        styles.append('''new ol.style.Style({
                            %s
                        })
                        ''' % style)
    return "[ %s]" % ",".join(styles)

def getCircle(color, size):
    return ("new ol.style.Circle({radius: %s, stroke: %s, fill: %s})" %
                (str(size), getStrokeStyle("'rgba(0,0,0,255)'", False, "0.5"),
                 getFillStyle(color)))

def getIcon(path, size):
    size  = float(size) * 0.005
    return '''new ol.style.Icon({
                  scale: %(s)f,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  src: "%(path)s"
            })''' % {"s": size, "path": "styles/" + os.path.basename(path)}

def getStrokeStyle(color, dashed, width):
    width  = math.floor(float(width) * 3.8)
    dash = "[3]" if dashed else "null"
    return "new ol.style.Stroke({color: %s, lineDash: %s, width: %d})" % (color, dash, width)

def getFillStyle(color):
    return "new ol.style.Fill({color: %s})" % color

