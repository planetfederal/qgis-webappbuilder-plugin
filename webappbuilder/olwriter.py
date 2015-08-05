from utils import *
import urlparse
from qgis.core import *
import codecs
import shutil
import traceback
from string import digits
import math

def _getWfsLayer(url, title, layerName, typeName, min, max, clusterDistance,
                 geometryType, layerCrs, viewCrs, layerOpacity, isSelectable, timeInfo):
    wfsSource =  ('''geojsonFormat_%(layerName)s = new ol.format.GeoJSON();
                    var wfsSource_%(layerName)s = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        loader: function(extent, resolution, projection) {
                            var url = '%(url)s?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=%(typeName)s&outputFormat=text/javascript&format_options=callback:loadFeatures_%(layerName)s' +
                                '&srsname=%(layerCrs)s&bbox=' + extent.join(',') + ',%(viewCrs)s';
                            $.ajax({
                                url: url,
                                dataType: 'jsonp'
                            });
                        },
                        strategy: ol.loadingstrategy.tile(new ol.tilegrid.createXYZ({maxZoom: 19})),
                    });
                    var loadFeatures_%(layerName)s = function(response) {
                        wfsSource_%(layerName)s.addFeatures(
                                geojsonFormat_%(layerName)s.readFeatures(response,
                                    {dataProjection: '%(layerCrs)s', featureProjection: '%(viewCrs)s'}));
                    };

                    ''' %
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
                    title: %(title)s,
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s
                });''' %
                {"opacity": layerOpacity, "title": title, "layerName":layerName,
                 "min": min,"max": max, "dist": str(clusterDistance),
                 "selectable": str(isSelectable).lower(), "timeInfo": timeInfo})
    else:
        vectorLayer = ('''var lyr_%(layerName)s = new ol.layer.Vector({
                            opacity: %(opacity)s,
                            source: wfsSource_%(layerName)s, %(min)s %(max)s
                            style: style_%(layerName)s,
                            title: %(title)s,
                            filters: [],
                            timeInfo: %(timeInfo)s,
                            isSelectable: %(selectable)s
                        });''' %
                        {"opacity": layerOpacity, "title": title, "layerName":layerName,
                         "min": min, "max": max, "selectable": str(isSelectable).lower(),
                         "timeInfo": timeInfo})
    return wfsSource + vectorLayer



def layerToJavascript(applayer, settings, deploy, title):
    viewCrs = settings["App view CRS"]
    scaleVisibility = settings["Use layer scale dependent visibility"]
    useViewCrs = settings["Use view CRS for WFS connections"]
    workspace = safeName(settings["Title"])
    layer = applayer.layer
    timeInfo = ('["%s","%s"]' % (unicode(applayer.timeInfo[0]), unicode(applayer.timeInfo[1]))
                            if applayer.timeInfo is not None else "null")
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
                                applayer.allowSelection, timeInfo)
        elif applayer.method == METHOD_FILE:
            if applayer.clusterDistance > 0 and layer.geometryType() == QGis.Point:
                return ('''var cluster_%(n)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_%(n)s)}),
                });
                var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: cluster_%(n)s, %(min)s %(max)s
                    style: style_%(n)s,
                    title: %(name)s,
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution, "dist": str(applayer.clusterDistance),
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo})
            else:
                return ('''var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_%(n)s)}),
                    %(min)s %(max)s
                    style: style_%(n)s,
                    title: %(name)s,
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution,
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo})
        elif applayer.method == METHOD_WFS or applayer.method == METHOD_WFS_POSTGIS:
                url = deploy["GeoServer url"] + "/wfs"
                typeName = ":".join([safeName(settings["Title"]), layerName])
                return _getWfsLayer(url, title, layerName, typeName, minResolution,
                            maxResolution, applayer.clusterDistance, layer.geometryType(),
                            layerCrs, viewCrs, layerOpacity, applayer.allowSelection,
                            timeInfo)
        else:
            source = layer.source()
            layers = layer.name()
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        opacity: %(opacity)s,
                        %(min)s %(max)s
                        timeInfo: %(timeInfo)s,
                        filters: [],
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true"},
                        })),
                        title: %(name)s
                      });''' % {"opacity": layerOpacity, "layers": layerName,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "timeInfo": timeInfo}
    elif layer.type() == layer.RasterLayer:
        layerOpacity = layer.renderer().opacity()
        if layer.providerType().lower() == "wms":
            source = layer.source()
            layers = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
            url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0]
            styles = re.search(r"styles=(.*?)(?:&|$)", source).groups(0)[0]
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        opacity: %(opacity)s,
                        timeInfo: %(timeInfo)s,
                        %(min)s %(max)s
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true", "STYLES": "%(styles)s"},
                        })),
                        title: %(name)s
                      });''' % {"opacity": layerOpacity, "layers": layers,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "styles": styles, "timeInfo": timeInfo}
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
                                      "crs": viewCrs, "timeInfo": timeInfo}
        else:
            url = "%s/%s/wms" % (deploy["GeoServer url"], workspace)
            return '''var lyr_%(n)s = new ol.layer.Tile({
                        opacity: %(opacity)s,
                        %(min)s %(max)s
                        timeInfo: %(timeInfo)s,
                        source: new ol.source.TileWMS(({
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s", "TILED": "true"},
                        })),
                        title: %(name)s
                      });''' % {"opacity": layerOpacity, "layers": layerName,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "timeInfo": timeInfo}

def exportStyles(layers, folder, settings, addTimeInfo):
    stylesFolder = os.path.join(folder, "styles")
    QDir().mkpath(stylesFolder)
    for appLayer in layers:
        cannotWriteStyle = False
        layer = appLayer.layer
        if layer.type() != layer.VectorLayer or appLayer.method in [METHOD_WMS, METHOD_WMS_POSTGIS]:
            continue
        defs = ""
        try:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                symbol = renderer.symbol()
                style = "var style = " + getSymbolAsStyle(symbol, stylesFolder)
                value = 'var value = ""'
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
                style = '''var style = categories_%s[value]'''  % (safeName(layer.name()))
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
                                var numSelected = 0;
                                var numVisible = 0;
                                for (var i = 0; i < size; i++) {
                                    if (features[i].hide != true) {
                                        numVisible++;
                                        if (selected && selected.indexOf(features[i]) != -1) {
                                            numSelected++;
                                        }
                                    }
                                }
                                if (numVisible === 0) {
                                    return null;
                                }
                                if (numVisible != 1) {
                                    var color = numSelected == 0 ? '#3399CC' : '#FFCC00'
                                    var style = numSelected == 0 ? clusterStyleCache_popp[numVisible] : selectedClusterStyleCache_popp[numVisible];
                                    if (!style) {
                                        style = [new ol.style.Style({
                                            image: new ol.style.Circle({
                                                radius: 10,
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
                                                })
                                            })
                                        })];
                                        if (numSelected == 0) {
                                            clusterStyleCache_popp[numVisible] = style;
                                        } else {
                                            selectedClusterStyleCache_popp[numVisible] = style;
                                        }
                                    }
                                    return style;
                                }
                            }
                            feature = feature.get('features')[0]
                            ''' % {"name": safeName(layer.name())}
            else:
                cluster = ""

            filters = '''if (feature.hide === true){
                return null;
            }
            '''
            timeInfo = getTimeBasedStyleCondition(appLayer) if addTimeInfo else ""
            labels = getLabeling(layer)
            style = '''function(feature, resolution){
                        %(cluster)s
                        %(filters)s
                        %(time)s
                        %(value)s
                        %(style)s;
                        %(selectionStyle)s;
                        allStyles = [];
                        %(labels)s
                        var selected = lyr_%(layerName)s.selectedFeatures;
                        if (selected && selected.indexOf(feature) != -1){
                            allStyles.push.apply(allStyles, selectionStyle);
                        }
                        else{
                            allStyles.push.apply(allStyles, style);
                        }
                        return allStyles;
                    }''' % {"style": style,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster, "selectionStyle": selectionStyle,
                            "time": timeInfo, "filters": filters, "labels":labels}
        except Exception, e:
            traceback.print_exc()
            cannotWriteStyle = True

        path = os.path.join(stylesFolder, safeName(layer.name()) + ".js")

        with codecs.open(path, "w","utf-8") as f:
            if cannotWriteStyle:
                f.write('''var default_fill = new ol.style.Fill({
                   color: 'rgba(255,255,255,0.4)'
                 });
                 var default_stroke = new ol.style.Stroke({
                   color: '#3399CC',
                   width: 1.25
                 });
                 var style_%s = [
                   new ol.style.Style({
                     image: new ol.style.Circle({
                       fill: default_fill,
                       stroke: default_stroke,
                       radius: 5
                     }),
                     fill: default_fill,
                     stroke: default_stroke
                   })
                 ];''' % safeName(layer.name()))
            else:
                f.write('''%(defs)s
                        var textStyleCache_%(name)s={}
                        var clusterStyleCache_%(name)s={}
                        var selectedClusterStyleCache_%(name)s={}
                        var style_%(name)s = %(style)s;''' %
                    {"defs":defs, "name":safeName(layer.name()), "style":style})

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
                  rotation: %(rotation)s,
                  offsetX: %(offsetX)s,
                  offsetY: %(offsetY)s %(halo)s
                });
            textStyleCache_%(layerName)s[key] = new ol.style.Style({"text": text});
        }
        allStyles.push(textStyleCache_%(layerName)s[key]);
        ''' % {"halo": halo, "offsetX": offsetX, "offsetY": offsetY, "rotation": rotation,
                "size": size, "color": color, "label": labelText, "resolution": resolution,
                "layerName": safeName(layer.name())}

    return s

def getTimeBasedStyleCondition(applayer):

    if applayer.timeInfo is None:
        return ""
    elif isinstance(applayer.timeInfo[0], basestring):
        return '''
                minFeatureTime = Date.parse(feature.get("%s"))
                if (isNaN(minFeatureTime) ||currentTimelineTime < minFeatureTime){
                    return null;
                }
                maxFeatureTime = Date.parse(feature.get("%s"))
                if (isNaN(maxFeatureTime) || currentTimelineTime > maxFeatureTime){
                    return null;
                }


        ''' % (applayer.timeInfo[0], applayer.timeInfo[1])
    else:
        return '''
            try{
                if (currentTimelineTime < %i){
                    return null;
                }
                if (currentTimelineTime > %i){
                    return null;
                }
            }
            catch (e){}
        ''' % (applayer.timeInfo[0], applayer.timeInfo[1])


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
                color = getRGBAColor(props["color"], alpha)
            with open(sl.path()) as f:
                svg = "".join(f.readlines())
            svg = re.sub(r'\"param\(outline\).*?\"', color, svg)
            svg = re.sub(r'\"param\(fill\).*?\"', color, svg)
            filename, ext = os.path.splitext(os.path.basename(sl.path()))
            filename = filename + ''.join(c for c in color if c in digits) + ext
            path = os.path.join(stylesFolder, filename)
            with open(path, "w") as f:
                f.write(svg)
            style = "image: %s" % getIcon(path, sl.size(), sl.angle())
        elif isinstance(sl, QgsSimpleLineSymbolLayerV2):
            # Check for old version
            if color is None:
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
            if props["style"] == "no":
                fillAlpha = 0
            else:
                fillAlpha = alpha
            if color is None:
                fillColor =  getRGBAColor(props["color"], fillAlpha)
                # for old version
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
            })''' % {"s": size, "path": "styles/" + os.path.basename(path),
                     "rad": math.radians(rotation)}

def getStrokeStyle(color, dashed, width):
    width  = float(width) * SIZE_FACTOR
    dash = "[3]" if dashed else "null"
    return "new ol.style.Stroke({color: %s, lineDash: %s, width: %d})" % (color, dash, width)

def getFillStyle(color):
    return "new ol.style.Fill({color: %s})" % color

