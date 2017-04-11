# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from utils import *
import urlparse
from qgis.core import *
import traceback
from string import digits
import math
import codecs
import uuid
import json
from webappbuilder.exp2js import compile_to_file

exportedStyles = 0

def _getWfsLayer(url, title, layer, typeName, min, max, clusterDistance,
                 layerCrs, viewCrs, layerOpacity, isSelectable,
                 timeInfo, popup, jsonp, useStrategy):

    layerName = safeName(layer.name())
    layerId = layer.id()
    geometryType = layer.wkbType()
    if useStrategy:
        strategy = "strategy: ol.loadingstrategy.tile(new ol.tilegrid.createXYZ({maxZoom: 19}))"
        bbox = "&bbox=' + extent.join(',') + ',%s" % viewCrs
    else:
        bbox = ""
        strategy = ""
    if jsonp:
        wfsSource =  ('''window.wfsCallback_%(layerName)s = function(jsonData) {
                        wfsSource_%(layerName)s.addFeatures(wfsSource_%(layerName)s.getFormat().readFeatures(jsonData, {featureProjection: "%(viewCrs)s", dataProjection: "%(layerCrs)s"}));
                    };
                    var wfsSource_%(layerName)s = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        loader: function(extent, resolution, projection) {
                            var script = document.createElement('script');
                            script.src = '%(url)s?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=%(typeName)s&outputFormat=text/javascript&format_options=callback:wfsCallback_%(layerName)s' +
                                '&srsname=%(layerCrs)s%(bbox)s';
                            document.head.appendChild(script);
                        },
                        %(strategy)s
                    });
                    ''' %
                    {"url": url, "layerName":layerName, "typeName": typeName,
                     "layerCrs": layerCrs, "viewCrs": viewCrs, "strategy": strategy, "bbox": bbox})
    else:
        wfsSource =  ('''var wfsSource_%(layerName)s = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        loader: function(extent, resolution, projection) {
                          var url = '%(url)s?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=%(typeName)s&outputFormat=application/json&' +
                                '&srsname=%(layerCrs)s%(bbox)s';
                          var xmlhttp = new XMLHttpRequest();
                          xmlhttp.onreadystatechange = function() {
                            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                              var features = wfsSource_%(layerName)s.getFormat().readFeatures(xmlhttp.responseText, {featureProjection: projection, dataProjection: "%(layerCrs)s"});
                              wfsSource_%(layerName)s.addFeatures(features);
                            }
                          };
                          xmlhttp.open('GET', url, true);
                          xmlhttp.send();
                        },
                        %(strategy)s
                    });''' %
                    {"url": url, "layerName":layerName, "typeName": typeName,
                     "layerCrs": layerCrs, "strategy": strategy, "bbox": bbox})

    GEOM_TYPE_NAME = {
        QGis.WKBPoint: 'Point',
        QGis.WKBLineString: 'LineString',
        QGis.WKBPolygon: 'Polygon',
        QGis.WKBMultiPoint: 'MultiPoint',
        QGis.WKBMultiLineString: 'MultiLineString',
        QGis.WKBMultiPolygon: 'MultiPolygon',
    }

    featurePrefix = ("'%s'" % typeName.split(":")[0]) if ":" in typeName else "undefined"
    wfst = str(bool(layer.capabilitiesString())).lower()
    wfsInfo = '''{featureNS: '%(ns)s',
                    featureType: '%(featureType)s',
                    geometryType: '%(geomType)s',
                    geometryName: '%(geomName)s',
                    featurePrefix: %(featurePrefix)s,
                    url: '%(url)s'
                  },
                  isWFST:%(wfst)s,''' % {"geomType": GEOM_TYPE_NAME[geometryType],
                          "url": url, "geomName": "the_geom",
                          "featureType": typeName.split(":")[-1], "ns": "",
                          "featurePrefix": featurePrefix,
                          "wfst": wfst #TODO: fill NS
                          }

    if clusterDistance > 0 and geometryType== QGis.WKBPoint:
        vectorLayer = ('''var cluster_%(layerName)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: wfsSource_%(layerName)s
                });
                var lyr_%(layerName)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: cluster_%(layerName)s, %(min)s %(max)s
                    style: style_%(layerName)s,
                    selectedStyle: selectionStyle_%(layerName)s,
                    title: %(title)s,
                    id: "%(id)s",
                    wfsInfo: %(wfsInfo)s
                    filters: [],
                    timeInfo: %(timeInfo)s,
                    isSelectable: %(selectable)s,
                    popupInfo: "%(popup)s"
                });''' %
                {"opacity": layerOpacity, "title": title, "layerName":layerName,
                 "min": min,"max": max, "dist": str(clusterDistance),
                 "selectable": str(isSelectable).lower(), "timeInfo": timeInfo,
                 "id": layerId, "popup": popup, "wfsInfo": wfsInfo})
    else:
        vectorLayer = ('''var lyr_%(layerName)s = new ol.layer.Vector({
                            opacity: %(opacity)s,
                            source: wfsSource_%(layerName)s, %(min)s %(max)s
                            style: style_%(layerName)s,
                            selectedStyle: selectionStyle_%(layerName)s,
                            title: %(title)s,
                            id: "%(id)s",
                            wfsInfo: %(wfsInfo)s
                            filters: [],
                            timeInfo: %(timeInfo)s,
                            isSelectable: %(selectable)s,
                            popupInfo: "%(popup)s"
                        });''' %
                        {"opacity": layerOpacity, "title": title, "layerName":layerName,
                         "min": min, "max": max, "selectable": str(isSelectable).lower(),
                         "timeInfo": timeInfo, "id": layerId, "popup": popup, "wfsInfo": wfsInfo})
    return wfsSource + vectorLayer



def layerToJavascript(applayer, settings, title, forPreview):
    viewCrs = settings["App view CRS"]
    jsonp = settings["Use JSONP for WFS connections"]
    useStrategy = not applayer.singleTile
    scaleVisibility = settings["Use layer scale dependent visibility"]
    useViewCrs = settings["Use view CRS for WFS connections"]
    workspace = safeName(settings["Title"])
    layer = applayer.layer

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
        try:
            timeInfo = ('{start:%s,end:%s}' % (int(applayer.timeInfo[0]), int(applayer.timeInfo[1]))
                                if applayer.timeInfo is not None else "null")
        except:
            timeInfo = '{start:"%s",end:"%s"}' % (unicode(applayer.timeInfo[0]), unicode(applayer.timeInfo[1]))

        layerOpacity = 1 - (layer.layerTransparency() / 100.0)
        if layer.providerType().lower() == "wfs":
            datasourceUri = QgsDataSourceURI(layer.source())
            url = datasourceUri.param("url") or layer.source().split("?")[0]
            typeName = datasourceUri.param("typename")
            if not bool(typeName):
                parsed = urlparse.urlparse(layer.source())
                typeName = ",".join(urlparse.parse_qs(parsed.query)['TYPENAME'])
            return _getWfsLayer(url, title, layer, typeName,
                                minResolution, maxResolution, applayer.clusterDistance,
                                layerCrs, viewCrs, layerOpacity,
                                applayer.allowSelection, timeInfo, popup, jsonp, useStrategy)
        else:
            if forPreview:
                source = ""
            else:
                source = '''{
                            format: new ol.format.GeoJSON(),
                            url: './data/lyr_%s.json'
                            }''' % layerName
            if applayer.clusterDistance > 0 and layer.geometryType() == QGis.Point:
                js =  ('''var cluster_%(n)s = new ol.source.Cluster({
                    distance: %(dist)s,
                    source: new ol.source.Vector(%(source)s),
                });
                var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: cluster_%(n)s, %(min)s %(max)s
                    style: style_%(n)s,
                    selectedStyle: selectionStyle_%(n)s,
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
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup,
                 "source": source})
            elif isinstance(layer.rendererV2(), QgsHeatmapRenderer):
                renderer = layer.rendererV2()
                hmRadius = renderer.radius()
                colorRamp = renderer.colorRamp()
                hmStart = colorRamp.color1().name()
                hmEnd = colorRamp.color2().name()
                hmRamp = "['" + hmStart + "', "
                hmStops = colorRamp.stops()
                for stop in hmStops:
                    hmRamp += "'" + stop.color.name() + "', "
                hmRamp += "'" + hmEnd + "']"
                hmWeight = renderer.weightExpression()
                hmWeightId = layer.fieldNameIndex(hmWeight)
                hmWeightMax = layer.maximumValue(hmWeightId)
                if hmWeight != "":
                    weight = '''weight: function(feature){
                            var weightField = '%(hmWeight)s';
                            var featureWeight = feature.get(weightField);
                            var maxWeight = %(hmWeightMax)d;
                            var calibratedWeight = featureWeight/maxWeight;
                            return calibratedWeight;
                        },''' % {"hmWeight": hmWeight, "hmWeightMax": hmWeightMax}
                else:
                    weight = ""
                js = '''var lyr_%(n)s = new ol.layer.Heatmap({
                    source: new ol.source.Vector(%(source)s),
                    %(min)s %(max)s
                    radius: %(hmRadius)d * 2,
                    gradient: %(hmRamp)s,
                    blur: 15,
                    shadow: 250,
                    %(weight)s
                    title: "%(n)s"
                    });''' %  {"n": layerName, "source": source,
                             "min": minResolution, "max": maxResolution,
                             "hmRadius": hmRadius, "hmRamp": hmRamp,
                             "weight": weight}
            else:
                js= ('''var lyr_%(n)s = new ol.layer.Vector({
                    opacity: %(opacity)s,
                    source: new ol.source.Vector(%(source)s),
                    %(min)s %(max)s
                    style: style_%(n)s,
                    selectedStyle: selectionStyle_%(n)s,
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
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup,
                 "source": source})

            if forPreview:
                clusterSource = ".getSource()" if applayer.clusterDistance > 0 and layer.geometryType() == QGis.Point else ""
                js += '''\n%(n)s_geojson_callback = function(geojson) {
                              lyr_%(n)s.getSource()%(cs)s.addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };''' % {"n": layerName, "cs": clusterSource}
            return js

    elif layer.type() == layer.RasterLayer:
        timeInfo = applayer.timeInfo if applayer.timeInfo is not None else "null"
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
                          crossOrigin: 'anonymous',
                          url: "%(url)s",
                          params: {"LAYERS": "%(layers)s" %(tiled)s, "STYLES": "%(styles)s"},
                        })),
                        title: %(name)s,
                        id: "%(id)s",
                        popupInfo: "%(popup)s",
                        projection: "%(crs)s"
                      });''' % {"opacity": layerOpacity, "layers": layers,
                                "url": url, "n": layerName, "name": title,
                                "min": minResolution, "max": maxResolution,
                                "styles": styles, "timeInfo": timeInfo,
                                "id": layer.id(), "layerClass": layerClass,
                                "sourceClass": sourceClass, "tiled": tiled,
                                "popup": popup, "crs": layer.crs().authid()}
        else:
            if layer.providerType().lower() == "gdal":
                provider = layer.dataProvider()
                transform = QgsCoordinateTransform(provider.crs(), QgsCoordinateReferenceSystem(viewCrs))
                extent = transform.transform(provider.extent())
                sExtent = "[%f, %f, %f, %f]" % (extent.xMinimum(), extent.yMinimum(),
                                        extent.xMaximum(), extent.yMaximum())

                nodata = [0, 0, 0]
                return '''var src_%(n)s = new ol.source.ImageStatic({
                                url: "./data/%(n)s.png",
                                projection: "%(crs)s",
                                alwaysInRange: true,
                                imageSize: [%(col)d, %(row)d],
                                imageExtent: %(extent)s
                          });

                          var raster_%(n)s = new ol.source.Raster({
                                sources: [src_%(n)s],
                                operation: function(pixels, data) {
                                    var pixel = pixels[0];
                                    if (pixel[0] === %(ndR)d && pixel[1] === %(ndG)d && pixel[2] === %(ndB)d) {
                                        pixel[3] = 0;
                                    }
                                    return pixel;
                                  }
                          });

                          var lyr_%(n)s = new ol.layer.Image({
                                opacity: %(opacity)s,
                                %(min)s %(max)s
                                title: %(name)s,
                                id: "%(id)s",
                                timeInfo: %(timeInfo)s,
                                source: raster_%(n)s
                            });''' % {"opacity": layerOpacity, "n": layerName,
                                      "extent": sExtent, "col": provider.xSize(),
                                      "min": minResolution, "max": maxResolution,
                                      "name": title, "row": provider.ySize(),
                                      "crs": viewCrs, "timeInfo": timeInfo,
                                      "id": layer.id(), "ndR": nodata[0],
                                      "ndG": nodata[1], "ndB": nodata[2]}

def exportStyles(layers, folder, settings, addTimeInfo, app, progress):
    SELECTION_YELLOW = '"rgba(255, 204, 0, 1)"'
    global exportedStyles
    exportedStyles = 0
    stylesFolder = os.path.join(folder, "data", "styles")
    QDir().mkpath(stylesFolder)
    progress.setText("Writing layer styles")
    progress.setProgress(0)
    qgisLayers = [lay.layer for lay in layers]
    #mapbox = mapboxgl.toMapbox(qgisLayers, stylesFolder)

    for ilayer, appLayer in enumerate(layers):
        cannotWriteStyle = False
        layer = appLayer.layer
        if layer.type() != layer.VectorLayer:
            continue
        defs = ""#var mapboxStyle = %s;\n" % json.dumps(mapbox, indent=4, sort_keys=True)
        try:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                symbol = renderer.symbol()
                style = "var style = %s;" % getSymbolAsStyle(symbol, stylesFolder, layer, app.variables)
                value = 'var value = "";'
                selectionStyle = "var style = " + getSymbolAsStyle(symbol,
                                    stylesFolder, layer, app.variables, SELECTION_YELLOW)
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                defs += "var categories_%s = function(){ return {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(), stylesFolder, layer, app.variables)))
                defs +=  ",\n".join(cats) + "};};"
                defs += "var categoriesSelected_%s = {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(),
                                stylesFolder, layer, app.variables, SELECTION_YELLOW)))
                defs +=  ",\n".join(cats) + "};"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = categories_%s()[value];'''  % (safeName(layer.name()))
                selectionStyle = '''var style = categoriesSelected_%s[value]'''  % (safeName(layer.name()))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                varName = "ranges_" + safeName(layer.name())
                defs += "var %s = function(){ return [" % varName
                ranges = []
                for ran in renderer.ranges():
                    symbolstyle = getSymbolAsStyle(ran.symbol(), stylesFolder, layer, app.variables)
                    selectedSymbolStyle = getSymbolAsStyle(ran.symbol(), stylesFolder, layer, app.variables, SELECTION_YELLOW)
                    ranges.append('[%f, %f,\n %s, %s]' % (ran.lowerValue(), ran.upperValue(),
                                                         symbolstyle, selectedSymbolStyle))
                defs += ",\n".join(ranges) + "];};"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = %(v)s()[0][2];
                            var ranges = %(v)s();
                            for (var i = 0, ii = ranges.length; i < ii; i++){
                                var range = ranges[i];
                                if (value > range[0] && value<=range[1]){
                                    style = range[2];
                                    break;
                                }
                            }
                            ''' % {"v": varName}

                selectionStyle = '''var style = %(v)s[0][3];
                            for (var i = 0; i < %(v)s.length; i++){
                                var range = %(v)s[i];
                                if (value > range[0] && value<=range[1]){
                                    style = range[3];
                                    break;
                                }
                            }
                            ''' % {"v": varName}

            elif isinstance(renderer, QgsRuleBasedRendererV2):
                template = """
                        function rules_%s(feature, value) {
                            var context = {
                                feature: feature,
                                variables: {}
                            };
                            // Start of if blocks and style check logic
                            %s
                            else {
                                return %s;
                            }
                        }
                        var style = rules_%s(feature, value);
                        """
                elsejs = "[]"
                selectionElsejs = "[]"
                js = ""
                selectionJs = ""
                root_rule = renderer.rootRule()
                rules = root_rule.children()
                expFile = os.path.join(folder, "resources", "js",
                                       "qgis2web_expressions.js")
                ifelse = "if"
                for count, rule in enumerate(rules):
                    styleCode = getSymbolAsStyle(rule.symbol(), stylesFolder, layer, app.variables)
                    selectionStyleCode = getSymbolAsStyle(rule.symbol(), stylesFolder, layer, app.variables, SELECTION_YELLOW)
                    name = "".join((safeName(layer.name()), "rule", unicode(count)))
                    exp = rule.filterExpression()
                    if rule.isElse():
                        elsejs = styleCode
                        selectionElsejs = selectionStyleCode
                        continue
                    name = compile_to_file(exp, name, "OpenLayers3", expFile)
                    js += """
                    %s (%s(context)) {
                      return %s;
                    }
                    """ % (ifelse, name, styleCode)
                    js = js.strip()
                    selectionJs += """
                    %s (%s(context)) {
                      return %s;
                    }
                    """ % (ifelse, name, selectionStyleCode)
                    selectionJs = selectionJs.strip()
                    ifelse = "else if"
                value = ("var value = '';")
                style = template % (safeName(layer.name()), js, elsejs, safeName(layer.name()))
                selectionStyle = template % (safeName(layer.name()), selectionJs, selectionElsejs, safeName(layer.name()))
            else:
                cannotWriteStyle = True

            if (appLayer.clusterDistance > 0 and layer.type() == layer.VectorLayer
                                        and layer.geometryType() == QGis.Point):
                cluster = '''var features = feature.get('features');
                            var size = 0;
                            for (var i = 0, ii = features.length; i < ii; ++i) {
                              if (features[i].selected) {
                                return null;
                              }
                              if (features[i].hide !== true) {
                                size++;
                              }
                            }
                            if (size === 0) {
                              return null;
                            }
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

            labels = getLabeling(layer, folder, app)
            style = '''function(feature, resolution){
                        var context = {
                            feature: feature,
                            variables: {}
                        };
                        %(cluster)s
                        %(value)s
                        %(style)s
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": style,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                            "labels":labels}
            selectionStyle = '''function(feature, resolution){
                        var context = {
                            feature: feature,
                            variables: {}
                        };
                        %(value)s
                        %(style)s
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": selectionStyle,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                             "labels":labels}
        except Exception, e:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.WARNING)
            cannotWriteStyle = True

        if cannotWriteStyle:
            app.variables.append('''
             var style_%(s)s = [
               new ol.style.Style({
                 image: new ol.style.Circle({
                   fill: defaultFill,
                   stroke: defaultStroke,
                   radius: 5
                 }),
                 fill: defaultFill,
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

def getLabeling(layer, folder, app):
    if str(layer.customProperty("labeling/enabled")).lower() != "true":
        return ""

    labelField = layer.customProperty("labeling/fieldName")
    if unicode(layer.customProperty(
            "labeling/isExpression")).lower() == "true":
        exprFilename = os.path.join(folder, "resources", "js", "qgis2web_expressions.js")
        name = compile_to_file(labelField, "label_%s" % safeName(layer.name()),
                               "OpenLayers3", exprFilename)
        js = "%s(context)" % (name)
        js = js.strip()
        labelText = js
        app.scripts.append('<script src="./resources/js/qgis2web_expressions.js"></script>')
    else:
        labelText = 'feature.get("%s")' % labelField.replace('"', '\\"')

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

    palyr = QgsPalLayerSettings()
    palyr.readFromLayer(layer)
    sv = palyr.scaleVisibility
    if str(layer.customProperty("labeling/scaleVisibility")).lower() == "true":
        min = float(palyr.scaleMin)
        max = float(palyr.scaleMax)
        min = 1 / ((1 / min) * 39.37 * 90.7)
        max = 1 / ((1 / max) * 39.37 * 90.7)
        labelRes = " && resolution > %(min)d " % {"min": min}
        labelRes += "&& resolution < %(max)d" % {"max": max}
    else:
        labelRes = ""

    s = '''
        if (%(label)s !== null%(labelRes)s) {
            var labelText = String(%(label)s);
        } else {
            var labelText = ""
        }
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
                "size": size, "color": color, "label": labelText, "labelRes": labelRes,
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


def getSymbolAsStyle(symbol, stylesFolder, layer, variables, color = None):
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
            with codecs.open(sl.path(), encoding="utf-8") as f:
                svg = "".join(f.readlines())
            svg = re.sub(r'\"param\(outline\).*?\"', svgColor, svg)
            svg = re.sub(r'\"param\(fill\).*?\"', svgColor, svg)
            filename, ext = os.path.splitext(os.path.basename(sl.path()))
            filename = filename + ''.join(c for c in svgColor if c in digits) + ext
            path = os.path.join(stylesFolder, filename)
            with codecs.open(path, "w", "utf-8") as f:
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
        elif isinstance(sl, QgsGradientFillSymbolLayerV2):
            style = ('''fill: new ol.style.Fill({
                            color: function() {
                               var canvas = document.createElement('canvas');
                               var context = canvas.getContext('2d');
                               var grad = context.createLinearGradient(0,0,1000,0);
                               grad.addColorStop(0, %s);
                               grad.addColorStop(1, %s);
                               return grad;
                            }()
                     })''' %  (getRGBAColor(props["color"], alpha),
                                 getRGBAColor(props["gradient_color2"], alpha)))

        elif isinstance(sl, QgsPointPatternFillSymbolLayer):
            if color is None:
                global exportedStyles
                exportedStyles += 1
                qsize = QSize(int(math.floor(float(props["distance_x"]))), int(math.floor(float(props["distance_y"]))))
                img = sl.subSymbol().asImage(qsize)
                symbolPath = os.path.join(stylesFolder, "pattern%i.png" % exportedStyles)
                img.save(symbolPath)
                variables.append('''var patternFill_%(p)i = new ol.style.Fill({});
                    var patternImg_%(p)i = new Image();
                    patternImg_%(p)i.src = './data/styles/pattern%(p)i.png';
                    patternImg_%(p)i.onload = function(){
                      var canvas = document.createElement('canvas');
                      var context = canvas.getContext('2d');
                      var pattern = context.createPattern(patternImg_%(p)i, 'repeat');
                      patternFill_%(p)i = new ol.style.Fill({
                            color: pattern
                          });
                      lyr_%(layer)s.changed()
                    };''' % ({"layer": safeName(layer.name()), "p": exportedStyles}))
                style = 'fill: patternFill_%i' % exportedStyles
            else:'''
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 '''
        elif isinstance(sl, QgsSVGFillSymbolLayer):
            if color is None:
                global exportedStyles
                exportedStyles += 1
                def qcolorToRgba(c):
                    return ",".join([str(c.red()), str(c.green()), str(c.blue()), str(c.alpha())])
                if color is None:
                    fillColor = getRGBAColor(qcolorToRgba(sl.svgFillColor()), alpha)
                else:
                    fillColor = color
                borderColor = getRGBAColor(qcolorToRgba(sl.svgOutlineColor()), alpha)
                with codecs.open(sl.svgFilePath(), encoding="utf-8") as f:
                    svg = "".join(f.readlines())
                svg = re.sub(r'\"param\(outline\).*?\"', borderColor, svg)
                svg = re.sub(r'\"param\(fill\).*?\"', fillColor, svg)
                width = props["width"]
                svg = re.sub(r'width=\".*?px\"', r'width="%spx"' % str(width), svg)
                svg = re.sub(r'height=\".*?px\"', r'height="%spx"' % str(width), svg)
                filename = "patternFill_%s.svg" % exportedStyles
                path = os.path.join(stylesFolder, filename)
                with codecs.open(path, "w", "utf-8") as f:
                    f.write(svg)

                variables.append('''var patternFill_%(p)s = new ol.style.Fill({});
                        var patternImg_%(p)i = new Image();
                        patternImg_%(p)i.src = './data/styles/%(filename)s';
                        patternImg_%(p)i.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_%(p)i, 'repeat');
                          patternFill_%(p)i = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_%(layer)s.changed()
                        };''' % ({"layer": safeName(layer.name()), "p": exportedStyles,
                                  "filename": filename}))
                style = 'fill: patternFill_%i' % exportedStyles
            else:
                style = '''
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 '''
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
