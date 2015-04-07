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

baseLayersJs  = {
    "Stamen watercolor": "new ol.layer.Tile({type: 'base', title: 'Stamen watercolor', source: new ol.source.Stamen({layer: 'watercolor'})})",
    "Stamen toner": "new ol.layer.Tile({type: 'base', title: 'Stamen toner', source: new ol.source.Stamen({layer: 'toner'})})",
    "OSM": "new ol.layer.Tile({type: 'base', title: 'OSM', source: new ol.source.OSM()})",
    "MapQuest roads": "new ol.layer.Tile({type: 'base', title: 'MapQuest roads', source: new ol.source.MapQuest({layer: 'osm'})})",
    "MapQuest aerial": "new ol.layer.Tile({type: 'base', title: 'MapQuest aerial', source: new ol.source.MapQuest({layer: 'sat'})})"
}

baseLayerGroup = "var baseLayer = new ol.layer.Group({'title': 'Base maps',layers: [%s]});"

def writeOL(appdef, folder, writeLayersData, progress):
    progress.setText("Creating local files (3/3)")
    progress.setProgress(0)
    dst = os.path.join(folder, "resources")
    if not os.path.exists(dst):
        shutil.copytree(os.path.join(os.path.dirname(__file__), "resources", "base"), dst)
    layers = appdef["Layers"]
    if writeLayersData:
        exportLayers(layers, folder, progress)
    exportStyles(layers, folder, appdef["Settings"])
    writeLayersAndGroups(appdef, folder)
    geojsonVars ="\n".join(['<script src="layers/%s"></script>' % (safeName(layer.layer.name()) + ".js")
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])
    styleVars =  "\n".join(['<script src="styles/%s_style.js"></script>' % (safeName(layer.layer.name()))
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])
    popupLayers = "popupLayers = [%s];" % ",".join(['%s' % str(layer.popup)
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])
    controls = []
    widgets = appdef["Widgets"]
    if "Scale bar" in widgets:
        controls.append("new ol.control.ScaleLine(%s)" % json.dumps(widgets["Scale bar"]["Params"]))
    if "Layers list" in widgets:
        controls.append("new ol.control.LayerSwitcher(%s)" % json.dumps(widgets["Layers list"]["Params"]))
    if "Chart tool" in widgets:
        controls.append("new ol.control.ChartTool()")
    if "Attributes table" in widgets:
        controls.append("new ol.control.AttributesTable()")
    if "Overview map" in widgets:
        collapsed = str(widgets["Overview map"]["Params"]["collapsed"]).lower()
        controls.append("new ol.control.OverviewMap({collapsed: %s})" % collapsed)
    if "Mouse position" in widgets:
        coord = str(widgets["Mouse position"]["Params"]["coordinateFormat"])
        s = json.dumps(widgets["Mouse position"]["Params"])
        print s
        print coord
        s = s.replace('"%s"' % coord, coord)
        controls.append("new ol.control.MousePosition(%s)" % s)
    if "Zoom to extent" in widgets:
        controls.append("new ol.control.ZoomToExtent()")
    if "Zoom slider" in widgets:
        controls.append("new ol.control.ZoomSlider()")
    if "North arrow" in widgets:
        controls.append("new ol.control.Rotate({autoHide: false})")
    if "Full screen" in widgets:
        controls.append("new ol.control.FullScreen()")
    if "Zoom controls" in widgets:
        controls.append("new ol.control.Zoom(%s)" % json.dumps(widgets["Zoom controls"]["Params"]))
    if "Attribution" in widgets:
        controls.append("new ol.control.Attribution()")
    if "Text panel" in widgets:
        params = widgets["Text panel"]["Params"]
        textPanel = '<div class="inmap-panel">%s</div>' % params["HTML content"]
    else:
        textPanel = ""
    if "3D view" in widgets:
        cesium = '''var ol3d = new olcs.OLCesium({map: map});
                    var scene = ol3d.getCesiumScene();
                    var terrainProvider = new Cesium.CesiumTerrainProvider({
                        url : '//cesiumjs.org/stk-terrain/tilesets/world/tiles'
                    });
                    scene.terrainProvider = terrainProvider;
                    map.addControl(new CesiumControl(ol3d))'''
        cesiumImport = '''<script src="./resources/cesium/Cesium.js"></script>
                        <script src="./resources/ol3cesium.js"></script>'''
        dst = os.path.join(folder, "resources", "cesium")
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(os.path.dirname(__file__), "resources", "cesium"), dst)
    else:
        cesium = ""
        cesiumImport = ""

    mapbounds = bounds(appdef["Settings"]["Extent"] == "Canvas extent", layers)
    mapextent = "extent: %s," % mapbounds if appdef["Settings"]["Restrict to extent"] else ""
    maxZoom = int(appdef["Settings"]["Max zoom level"])
    minZoom = int(appdef["Settings"]["Min zoom level"])
    onHover = str(appdef["Settings"]["Show popups on hover"]).lower()
    highlight = str(appdef["Settings"]["Highlight features on hover"]).lower()
    view = "%s maxZoom: %d, minZoom: %d" % (mapextent, maxZoom, minZoom)
    footer = ('<div id="footer">%s</div>' % appdef["Settings"]["Footer text"]
                if "Footer text" in appdef["Settings"] else "")
    header = ('<div id="header">%s</div>' % appdef["Settings"]["Header text"]
                if "Header text" in appdef["Settings"] else "")
    values = {"@TITLE@": appdef["Settings"]["Title"],
              "@FOOTER@": footer,
              "@HEADER@": header,
                "@STYLEVARS@": styleVars,
                "@GEOJSONVARS@": geojsonVars,
                "@CESIUMIMPORT@": cesiumImport,
                "@TEXTPANEL@": textPanel}
    indexFilepath = os.path.join(folder, "index.html")
    template = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(indexFilepath, "w") as f:
        f.write(replaceInTemplate(template, values))
    values = {"@BOUNDS@": mapbounds,
                "@CONTROLS@": ",\n".join(controls),
                "@POPUPLAYERS@": popupLayers,
                "@VIEW@": view,
                "@ONHOVER@": onHover,
                "@DOHIGHLIGHT@": highlight,
                "@CESIUM@": cesium}
    indexJsFilepath = os.path.join(folder, "index.js")
    template = os.path.join(os.path.dirname(__file__), "templates", "index.js")
    with open(indexJsFilepath, "w") as f:
        f.write(replaceInTemplate(template, values))
    widgetsCssFilepath = os.path.join(folder, "widgets.css")
    with open(widgetsCssFilepath, "w") as f:
        f.write(widgetsCss["General"])
        for w in widgets:
            f.write(widgets[w]["Css"])
    baseCssFilepath = os.path.join(folder, "index.css")
    with open(baseCssFilepath, "w") as f:
        for css in baseCss:
            f.write(baseCss.get(css, ""))
        f.write(_contentCss(appdef))
    return indexFilepath


def _contentCss(appdef):
    try:
        footerCss = appdef["Settings"]["Footer css"]
        footerHeight = int(re.findall(u"height:.*?(\d+).*?;", footerCss)[0])
    except Exception, e:
        footerHeight = 0
    try:
        headerCss = appdef["Settings"]["Header css"]
        headerHeight = int(re.findall(u"height:.*?(\d+).*?;", headerCss)[0])
    except Exception, e:
        headerHeight = 0
    print headerHeight, footerHeight
    css = '''#content {
        width: 100%%;
        height: calc(100%% - %ipx);
        position:fixed;
        bottom: %ipx;
    }''' % (footerHeight + headerHeight, footerHeight)
    return css

def writeLayersAndGroups(appdef, folder):
    baseLayers = appdef["Base layers"]
    print baseLayers
    layers = appdef["Layers"]
    deploy = appdef["Deploy"]
    groups = appdef["Groups"]
    baseLayer = baseLayerGroup % ",".join([baseLayersJs[b] for b in baseLayers])
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

    groupList = ["baseLayer"]
    usedGroups = []
    noGroupList = []
    for appLayer in layers:
        layer = appLayer.layer
        if layer.id() in groupedLayers:
            groupName = groupedLayers[layer.id()]
            if groupName not in usedGroups:
                groupList.append("group_" + safeName(groupName))
                usedGroups.append(groupName)
        else:
            noGroupList.append("lyr_" + safeName(layer.name()))

    layersList = "var layersList = [%s];" % ",".join([layer for layer in (groupList + noGroupList)])
    singleLayersList = "var singleLayersList = [%s];" % ",".join(["lyr_%s" % safeName(layer.layer.name()) for layer in layers])

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



def replaceInTemplate(template, values):
    path = os.path.join(os.path.dirname(__file__), "templates", template)
    with open(path) as f:
        lines = f.readlines()
    s = "".join(lines)
    for name,value in values.iteritems():
        s = s.replace(name, value)
    return s

def bounds(useCanvas, layers):
    print useCanvas
    if useCanvas:
        canvas = iface.mapCanvas()
        canvasCrs = canvas.mapRenderer().destinationCrs()
        transform = QgsCoordinateTransform(canvasCrs, QgsCoordinateReferenceSystem("EPSG:3857"))
        try:
            extent = transform.transform(canvas.extent())
        except QgsCsException:
            print "error"
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
    if typeName is None:
        typeName = ""
    else:
        typeName = typeName + ":"
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
                    strategy: ol.loadingstrategy.createTile(new ol.tilegrid.XYZ({maxZoom: 19})),
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
        minResolution = "\nminResolution:%s,\n" % str(layer.minimumScale())
        maxResolution = "maxResolution:%s,\n" % str(layer.maximumScale())
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
                    distance: 40,
                        source: new ol.source.GeoJSON({object: geojson_%(n)s})
                });
                var lyr_%(n)s = new ol.layer.Vector({
                    source: cluster_%(n)s, %(min)s %(max)s
                    style: style_%(n)s,
                    title: "%(name)s"
                });''' %
                {"name": layer.name(), "n":layerName, "min": minResolution,
                 "max": maxResolution, "dist": applayer.clusterDistance})
            else:
                return ('''var lyr_%(n)s = new ol.layer.Vector({
                    source: new ol.source.GeoJSON({object: geojson_%(n)s}),%(min)s %(max)s
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
            size = layer.customProperty("labeling/fontSize")
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

        path = os.path.join(stylesFolder, safeName(layer.name()) + "_style.js")

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
            color =  getRGBAColor(props["color"], alpha)
            style = "image: %s" % getCircle(color)
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

def getCircle(color):
    return ("new ol.style.Circle({radius: 3, stroke: %s, fill: %s})" %
                (getStrokeStyle("'rgba(0,0,0,255)'", False, "0.5"), getFillStyle(color)))

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

