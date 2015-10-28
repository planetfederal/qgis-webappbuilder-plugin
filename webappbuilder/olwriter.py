from utils import *
import urlparse
from qgis.core import *
import traceback
from string import digits
import math

def _getWfsLayer(url, title, layerName, typeName, min, max, clusterDistance,
                 geometryType, layerCrs, viewCrs, layerOpacity, isSelectable,
                 timeInfo, layerId, popup):
    wfsSource =  ('''var geojsonFormat_%(layerName)s = new ol.format.GeoJSON();
                    var wfsSource_%(layerName)s = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        url: function(extent, resolution, projection) {
                            return '%(url)s?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=%(typeName)s&outputFormat=application/json&' +
                                '&srsname=%(layerCrs)s&bbox=' + extent.join(',') + ',%(viewCrs)s';
                        },
                        strategy: ol.loadingstrategy.tile(new ol.tilegrid.createXYZ({maxZoom: 19})),
                    });''' %
                    {"url": url, "layerName":layerName, "typeName": typeName,
                     "layerCrs": layerCrs, "viewCrs": viewCrs})

    if clusterDistance > 0 and geometryType== QGis.Point:
        vectorLayer = ('''var cluster_%(layerName)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: wfsSource_%(layerName)s,
                });
                var lyr_%(layerName)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: cluster_%(layerName)s, %(min)s %(max)s
                    style: style_%(layerName)s,
                    selectionStyle: selectionStyle_%(layerName)s,
                    title: %(title)s,
                    id: "%(id)s",
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s,
                    popupInfo: "%(popup)s"
                });''' %
                {"opacity": layerOpacity, "title": title, "layerName":layerName,
                 "min": min,"max": max, "dist": str(clusterDistance),
                 "selectable": str(isSelectable).lower(), "timeInfo": timeInfo,
                 "id": layerId, "popup": popup})
    else:
        vectorLayer = ('''var lyr_%(layerName)s = new ol.layer.Vector({
                            opacity: %(opacity)s,
                            source: wfsSource_%(layerName)s, %(min)s %(max)s
                            style: style_%(layerName)s,
                            selectionStyle: selectionStyle_%(layerName)s,
                            title: %(title)s,
                            id: "%(id)s",
                            filters: [],
                            timeInfo: %(timeInfo)s,
                            isSelectable: %(selectable)s,
                            popupInfo: "%(popup)s"
                        });''' %
                        {"opacity": layerOpacity, "title": title, "layerName":layerName,
                         "min": min, "max": max, "selectable": str(isSelectable).lower(),
                         "timeInfo": timeInfo, "id": layerId, "popup": popup})
    return wfsSource + vectorLayer



def layerToJavascript(applayer, settings, deploy, title):
    viewCrs = settings["App view CRS"]
    scaleVisibility = settings["Use layer scale dependent visibility"]
    useViewCrs = settings["Use view CRS for WFS connections"]
    workspace = safeName(settings["Title"])
    layer = applayer.layer
    try:
        timeInfo = ('{start:%s,end:%s}' % (int(applayer.timeInfo[0]), int(applayer.timeInfo[1]))
                            if applayer.timeInfo is not None else "null")
    except:
        timeInfo = '{start:"%s",end:"%s"}' % (unicode(applayer.timeInfo[0]), unicode(applayer.timeInfo[1]))
    title = '"%s"' % unicode(title) if title is not None else "null"
    if useViewCrs:
        layerCrs = viewCrs
    else:
        layerCrs = layer.crs().authid()
    if scaleVisibility and layer.hasScaleBasedVisibility():
        scaleToResolution = 3571.42
        minResolution = "\nminResolution:%s,\n" % str(layer.minimumScale() / scaleToResolution)
        maxResolution = "maxResolution:%s,\n" % str(layer.maximumScale() / scaleToResolution)
    else:
        minResolution = ""
        maxResolution = ""
    layerClass = "ol.layer.Image" if applayer.singleTile else "ol.layer.Tile"
    sourceClass = "ol.source.ImageWMS" if applayer.singleTile else "ol.source.TileWMS"
    tiled = "" if applayer.singleTile else ', "TILED": "true"'
    popup = applayer.popup.replace('\n', ' ').replace('\r', '').replace('"',"'")
    layerName = safeName(layer.name())
    if layer.type() == layer.VectorLayer:
        layerOpacity = 1 - (layer.layerTransparency() / 100.0)
        if layer.providerType().lower() == "wfs":
            url = layer.source().split("?")[0]
            parsed = urlparse.urlparse(layer.source())
            typeName = ",".join(urlparse.parse_qs(parsed.query)['TYPENAME'])
            return _getWfsLayer(url, title, layerName, typeName,
                                minResolution, maxResolution, applayer.clusterDistance,
                                layer.geometryType(), layerCrs, viewCrs, layerOpacity,
                                applayer.allowSelection, timeInfo, layer.id(), popup)
        elif applayer.method == METHOD_FILE:
            if applayer.clusterDistance > 0 and layer.geometryType() == QGis.Point:
                return ('''var cluster_%(n)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        url: './data/lyr_%(n)s.json'
                    }),
                });
                var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: cluster_%(n)s, %(min)s %(max)s
                    style: style_%(n)s,
                    selectionStyle: selectionStyle_%(n)s,
                    title: %(name)s,
                    id: "%(id)s",
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s,
                    popupInfo: "%(popup)s"
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution, "dist": str(applayer.clusterDistance),
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup})
            else:
                return ('''var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        url: './data/lyr_%(n)s.json'
                    }),
                    %(min)s %(max)s
                    style: style_%(n)s,
                    title: %(name)s,
                    id: "%(id)s",
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s,
                    popupInfo: "%(popup)s"
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution,
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup})
        elif applayer.method == METHOD_WFS or applayer.method == METHOD_WFS_POSTGIS:
                url = deploy["GeoServer url"] + "/wfs"
                typeName = ":".join([safeName(settings["Title"]), layerName])
                return _getWfsLayer(url, title, layerName, typeName, minResolution,
                            maxResolution, applayer.clusterDistance, layer.geometryType(),
                            layerCrs, viewCrs, layerOpacity, applayer.allowSelection,
                            timeInfo, layer.id(), popup)
        else:
            source = layer.source()
            layers = layer.name()
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = new %(layerClass)s({
                        opacity: %(opacity)s,
                        %(min)s %(max)s
                        timeInfo: %(timeInfo)s,
                        filters: [],
                        source: new %(sourceClass)s(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s" %(tiled)s},
                        })),
                        title: %(name)s,
                        id: "%(id)s"
                      });''' % {"opacity": layerOpacity, "layers": layerName,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "timeInfo": timeInfo, "id": layer.id(),
                                "layerClass": layerClass, "sourceClass": sourceClass,
                                "tiled": tiled}
    elif layer.type() == layer.RasterLayer:
        layerOpacity = layer.renderer().opacity()
        if layer.providerType().lower() == "wms":
            source = layer.source()
            layers = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
            url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0]
            styles = re.search(r"styles=(.*?)(?:&|$)", source).groups(0)[0]
            return '''var lyr_%(n)s = new %(layerClass)s({
                        opacity: %(opacity)s,
                        timeInfo: %(timeInfo)s,
                        %(min)s %(max)s
                        source: new %(sourceClass)s(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s" %(tiled)s, "STYLES": "%(styles)s"},
                        })),
                        title: %(name)s,
                        id: "%(id)s",
                        popupInfo: "%(popup)s"
                      });''' % {"opacity": layerOpacity, "layers": layers,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "styles": styles, "timeInfo": timeInfo,
                                "id": layer.id(), "layerClass": layerClass,
                                "sourceClass": sourceClass, "tiled": tiled,
                                "popup": popup}
        elif applayer.method == METHOD_FILE:
            if layer.providerType().lower() == "gdal":
                provider = layer.dataProvider()
                transform = QgsCoordinateTransform(provider.crs(), QgsCoordinateReferenceSystem(viewCrs))
                extent = transform.transform(provider.extent())
                sExtent = "[%f, %f, %f, %f]" % (extent.xMinimum(), extent.yMinimum(),
                                        extent.xMaximum(), extent.yMaximum())
                return '''var lyr_%(n)s = new ol.layer.Image({
                                opacity: %(opacity)s,
                                %(min)s %(max)s
                                title: %(name)s,
                                id: "%(id)s",
                                timeInfo: %(timeInfo)s,
                                source: new ol.source.ImageStatic({
                                   url: "./layers/%(n)s.jpg",
                                    projection: "%(crs)s",
                                    alwaysInRange: true,
                                    imageSize: [%(col)d, %(row)d],
                                    imageExtent: %(extent)s
                                })
                            });''' % {"opacity": layerOpacity, "n": layerName,
                                      "extent": sExtent, "col": provider.xSize(),
                                      "min": minResolution, "max": maxResolution,
                                      "name": title, "row": provider.ySize(),
                                      "crs": viewCrs, "timeInfo": timeInfo,"id": layer.id()}
        else:
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = %(layerClass)s({
                        opacity: %(opacity)s,
                        %(min)s %(max)s
                        timeInfo: %(timeInfo)s,
                        source: new %(sourceClass)s(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s" %(tiled)s},
                        })),
                        title: %(name)s,
                        id: "%(id)s"
                      });''' % {"opacity": layerOpacity, "layers": layerName,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "timeInfo": timeInfo, "id": layer.id(),
                                "layerClass": layerClass, "sourceClass": sourceClass,
                                "tiled": tiled}

def exportStyles(layers, folder, settings, addTimeInfo, app, progress):
    stylesFolder = os.path.join(folder, "data", "styles")
    QDir().mkpath(stylesFolder)
    progress.setText("Writing layer styles")
    progress.setProgress(0)
    for ilayer, appLayer in enumerate(layers):
        cannotWriteStyle = False
        layer = appLayer.layer
        if layer.type() != layer.VectorLayer or appLayer.method in [METHOD_WMS, METHOD_WMS_POSTGIS]:
            continue
        defs = ""
        try:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                symbol = renderer.symbol()
                style = "var style = %s;" % getSymbolAsStyle(symbol, stylesFolder)
                value = 'var value = "";'
                selectionStyle = "var selectionStyle = " + getSymbolAsStyle(symbol,
                                    stylesFolder, '"rgba(255, 204, 0, 1)"')
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                defs += "var categories_%s = {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(), stylesFolder)))
                defs +=  ",\n".join(cats) + "};"
                defs += "var categoriesSelected_%s = {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(),
                                stylesFolder, '"rgba(255, 204, 0, 1)"')))
                defs +=  ",\n".join(cats) + "};"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = categories_%s[value];'''  % (safeName(layer.name()))
                selectionStyle = '''var selectionStyle = categoriesSelected_%s[value]'''  % (safeName(layer.name()))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                varName = "ranges_" + safeName(layer.name())
                defs += "var %s = [" % varName
                ranges = []
                for ran in renderer.ranges():
                    symbolstyle = getSymbolAsStyle(ran.symbol(), stylesFolder)
                    selectedSymbolStyle = getSymbolAsStyle(ran.symbol(), stylesFolder, '"rgba(255, 204, 0, 1)"')
                    ranges.append('[%f, %f, %s, %s]' % (ran.lowerValue(), ran.upperValue(),
                                                         symbolstyle, selectedSymbolStyle))
                defs += ",\n".join(ranges) + "];"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = %(v)s[0][2];
                            var selectionStyle = %(v)s[0][3];
                            for (i = 0; i < %(v)s.length; i++){
                                var range = %(v)s[i];
                                if (value > range[0] && value<=range[1]){
                                    style = range[2];
                                    selectionStyle = range[3];
                                }
                            }
                            ''' % {"v": varName}
            else:
                cannotWriteStyle = True

            if (appLayer.clusterDistance > 0 and layer.type() == layer.VectorLayer
                                        and layer.geometryType() == QGis.Point):
                cluster = '''var size = feature.get('features').length;
                            if (size != 1){
                                var features = feature.get('features');
                                var numVisible = 0;
                                for (var i = 0; i < size; i++) {
                                    if (features[i].hide != true) {
                                        numVisible++;
                                    }
                                }
                                if (numVisible === 0) {
                                    return null;
                                }
                                if (numVisible != 1) {
                                    var color = '%(clusterColor)s'
                                    var style = clusterStyleCache_%(name)s[numVisible]
                                    if (!style) {
                                        style = [new ol.style.Style({
                                            image: new ol.style.Circle({
                                                radius: 14,
                                                stroke: new ol.style.Stroke({
                                                    color: '#fff'
                                                }),
                                                fill: new ol.style.Fill({
                                                    color: color
                                                })
                                            }),
                                            text: new ol.style.Text({
                                                text: numVisible.toString(),
                                                fill: new ol.style.Fill({
                                                    color: '#fff'
                                                }),
                                                stroke: new ol.style.Stroke({
                                                  color: 'rgba(0, 0, 0, 0.6)',
                                                  width: 3
                                                })
                                            })
                                        })];
                                        clusterStyleCache_%(name)s[numVisible] = style;
                                    }
                                    return style;
                                }
                            }
                            feature = feature.get('features')[0];
                            ''' % {"name": safeName(layer.name()), "clusterColor": appLayer.clusterColor}
            else:
                cluster = ""

            filters = '''if (feature.hide === true){
                return null;
            }
            '''
            labels = getLabeling(layer)
            style = '''function(feature, resolution){
                        %(cluster)s
                        %(filters)s
                        %(value)s
                        %(style)s;
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": style,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                             "filters": filters, "labels":labels}
            selectionStyle = '''function(feature, resolution){
                        %(cluster)s
                        %(filters)s
                        %(value)s
                        %(style)s;
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": selectionStyle,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                             "filters": filters, "labels":labels}
        except Exception, e:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.WARNING)
            cannotWriteStyle = True

        if cannotWriteStyle:
            app.variables.append('''
             var style_%(s)s = [
               new ol.style.Style({
                 image: new ol.style.Circle({
                   fill: defaulFill,
                   stroke: defaultStroke,
                   radius: 5
                 }),
                 fill: defaulFill,
                 stroke: defaultStroke
               })
             ];
              var selectionStyle_%(s)s = [
               new ol.style.Style({
                 image: new ol.style.Circle({
                   fill: defaultSelectionFill,
                   stroke: defaultSelectionStroke,
                   radius: 5
                 }),
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
               })
             ];''' % {"s": safeName(layer.name())})
        else:
            app.variables.append('''%(defs)s
                    var textStyleCache_%(name)s={}
                    var clusterStyleCache_%(name)s={}
                    var style_%(name)s = %(style)s;
                    var selectionStyle_%(name)s = %(selectionStyle)s;''' %
                {"defs":defs, "name":safeName(layer.name()), "style":style,
                 "selectionStyle": selectionStyle})
        progress.setProgress(int(ilayer*100.0/len(layers)))

def getLabeling(layer):
    if str(layer.customProperty("labeling/enabled")).lower() != "true":
        return ""

    labelField = layer.customProperty("labeling/fieldName")
    labelText = 'feature.get("%s")' % labelField

    try:
        size = str(float(layer.customProperty("labeling/fontSize")) * 2)
    except:
        size = 1

    if str(layer.customProperty("labeling/bufferDraw")).lower() == "true":
        rHalo = str(layer.customProperty("labeling/bufferColorR"))
        gHalo = str(layer.customProperty("labeling/bufferColorG"))
        bHalo = str(layer.customProperty("labeling/bufferColorB"))
        strokeWidth = str(float(layer.customProperty("labeling/bufferSize")) * SIZE_FACTOR)
        halo = ''',
                  stroke: new ol.style.Stroke({
                    color: "rgba(%s, %s, %s, 255)",
                    width: %s
                  })''' % (rHalo, gHalo, bHalo, strokeWidth)
    else:
        halo = ""

    r = layer.customProperty("labeling/textColorR")
    g = layer.customProperty("labeling/textColorG")
    b = layer.customProperty("labeling/textColorB")
    color = "rgba(%s, %s, %s, 255)" % (r,g,b)
    rotation = str(math.radians(-1 * float(layer.customProperty("labeling/angleOffset"))))
    offsetX = layer.customProperty("labeling/xOffset")
    offsetY = layer.customProperty("labeling/yOffset")
    textBaselines = ["bottom", "middle", "top"]
    textAligns = ["end", "center", "start"]
    quad = int(layer.customProperty("labeling/quadOffset"))
    textBaseline = textBaselines[quad / 3]
    textAlign = textAligns[quad % 3]

    if str(layer.customProperty("labeling/scaleVisibility")).lower() == "true":
        scaleToResolution = 3571.42
        minResolution = float(layer.customProperty("labeling/scaleMin")) / scaleToResolution
        maxResolution = float(layer.customProperty("labeling/scaleMax")) / scaleToResolution
        resolution = '''
            var minResolution = %(minResolution)s;
            var maxResolution = %(maxResolution)s;
            if (resolution > maxResolution || resolution < minResolution){
                labelText = "";
            } ''' % {"minResolution": minResolution, "maxResolution": maxResolution}
    else:
        resolution = ""

    s = '''
        var labelText = %(label)s;
        %(resolution)s
        var key = value + "_" + labelText;
        if (!textStyleCache_%(layerName)s[key]){
            var text = new ol.style.Text({
                  font: '%(size)spx Calibri,sans-serif',
                  text: labelText,
                  fill: new ol.style.Fill({
                    color: "%(color)s"
                  }),
                  textBaseline: "%(textBaseline)s",
                  textAlign: "%(textAlign)s",
                  rotation: %(rotation)s,
                  offsetX: %(offsetX)s,
                  offsetY: %(offsetY)s %(halo)s
                });
            textStyleCache_%(layerName)s[key] = new ol.style.Style({"text": text});
        }
        allStyles.push(textStyleCache_%(layerName)s[key]);
        ''' % {"halo": halo, "offsetX": offsetX, "offsetY": offsetY, "rotation": rotation,
                "size": size, "color": color, "label": labelText, "resolution": resolution,
                "layerName": safeName(layer.name()), "textAlign": textAlign,
                "textBaseline": textBaseline}

    return s


SIZE_FACTOR = 3.8

def getRGBAColor(color, alpha):
    try:
        r,g,b,a = color.split(",")
    except:
        color = color.lstrip('#')
        lv = len(color)
        r,g,b = tuple(str(int(color[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3))
        a = 255.0
    a = float(a) / 255.0
    return '"rgba(%s)"' % ",".join([r, g, b, str(alpha * a)])


def getSymbolAsStyle(symbol, stylesFolder, color = None):
    styles = []
    alpha = symbol.alpha()
    for i in xrange(symbol.symbolLayerCount()):
        sl = symbol.symbolLayer(i)
        props = sl.properties()
        if isinstance(sl, QgsSimpleMarkerSymbolLayerV2):
            style = "image: %s" % getShape(props, alpha, color)
        elif isinstance(sl, QgsSvgMarkerSymbolLayerV2):
            if color is None:
                svgColor = getRGBAColor(props["color"], alpha)
            else:
                svgColor = color
            with open(sl.path()) as f:
                svg = "".join(f.readlines())
            svg = re.sub(r'\"param\(outline\).*?\"', svgColor, svg)
            svg = re.sub(r'\"param\(fill\).*?\"', svgColor, svg)
            filename, ext = os.path.splitext(os.path.basename(sl.path()))
            filename = filename + ''.join(c for c in svgColor if c in digits) + ext
            path = os.path.join(stylesFolder, filename)
            with open(path, "w") as f:
                f.write(svg)
            style = "image: %s" % getIcon(path, sl.size(), sl.angle())
        elif isinstance(sl, QgsSimpleLineSymbolLayerV2):
            if color is None:
                if 'color' in props:
                    strokeColor = getRGBAColor(props["color"], alpha)
                else:
                    strokeColor = getRGBAColor(props["line_color"], alpha)
            else:
                strokeColor = color
            if 'width' in props:
                line_width = props["width"]
            else:
                line_width = props["line_width"]
            if 'penstyle' in props:
                line_style = props["penstyle"]
            else:
                line_style = props["line_style"]
            style = "stroke: %s" % (getStrokeStyle(strokeColor, line_style != "solid", line_width))
        elif isinstance(sl, QgsSimpleFillSymbolLayerV2):
            if props["style"] == "no":
                fillAlpha = 0
            else:
                fillAlpha = alpha
            if color is None:
                fillColor =  getRGBAColor(props["color"], fillAlpha)
                if 'color_border' in props:
                    borderColor =  getRGBAColor(props["color_border"], alpha)
                else:
                    borderColor =  getRGBAColor(props["outline_color"], alpha)
            else:
                borderColor = color
                fillColor = color
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

def getShape(props, alpha, color_):
    size = float(props["size"]) * SIZE_FACTOR / 2
    color =  color_ or getRGBAColor(props["color"], alpha)
    outlineColor = color_ or getRGBAColor(props["outline_color"], alpha)
    outlineWidth = float(props["outline_width"])
    shape = props["name"]
    if "star" in shape.lower():
        return getRegularShape(color, 5,  size, size / 2.0, outlineColor, outlineWidth)
    elif "triangle" in shape.lower():
        return getRegularShape(color, 3,  size, None, outlineColor, outlineWidth)
    elif "diamond" == shape.lower():
        return getRegularShape(color, 4,  size, None, outlineColor, outlineWidth)
    elif "pentagon" == shape.lower():
        return getRegularShape(color, 5,  size, None, outlineColor, outlineWidth)
    elif "rectangle" == shape.lower():
        return getRegularShape(color, 4,  size, None, outlineColor, outlineWidth, 3.14159 / 4.0)
    elif "cross" == shape.lower():
        return getRegularShape(color, 4,  size, 0, outlineColor, outlineWidth)
    elif "cross2" == shape.lower():
        return getRegularShape(color, 4,  size, 0, outlineColor, outlineWidth, 3.14159 / 4.0)
    else:
        return getCircle(color, size, outlineColor, outlineWidth)

def getCircle(color, size, outlineColor, outlineWidth):
    return ("new ol.style.Circle({radius: %s, stroke: %s, fill: %s})" %
                (str(size), getStrokeStyle(outlineColor, False, outlineWidth),
                 getFillStyle(color)))

def getRegularShape(color, points, radius1, radius2, outlineColor, outlineWidth, angle = 0):
    if radius2 is None:
        return ("new ol.style.RegularShape({points: %s, radius: %s, stroke: %s, fill: %s, angle: %s})" %
                (str(points), str(radius1),
                 getStrokeStyle(outlineColor, False, outlineWidth),
                 getFillStyle(color), str(angle)))
    else:
        return ("new ol.style.RegularShape({points: %s, radius1: %s, radius2: %s, stroke: %s, fill: %s, angle: %s})" %
                (str(points), str(radius1), str(radius2),
                 getStrokeStyle(outlineColor, False, outlineWidth),
                 getFillStyle(color), angle))

def getIcon(path, size, rotation):
    size  = float(size) * 0.005
    return '''new ol.style.Icon({
                  scale: %(s)f,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  src: "%(path)s",
                  rotation: %(rad)f
            })''' % {"s": size, "path": "./data/styles/" + os.path.basename(path),
                     "rad": math.radians(rotation)}

def getStrokeStyle(color, dashed, width):
    width  = float(width) * SIZE_FACTOR
    dash = "[6]" if dashed else "null"
    return "new ol.style.Stroke({color: %s, lineDash: %s, width: %d})" % (color, dash, width)

def getFillStyle(color):
    return "new ol.style.Fill({color: %s})" % color

