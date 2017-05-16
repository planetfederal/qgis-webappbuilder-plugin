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
from PyQt4.QtCore import QSize

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


def _geomType(geometryType):
    types = {QGis.Point: "Point", QGis.Line: "Line", QGis.Polygon: "Polygon"}
    return types.get(geometryType, "Point")

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
        geometryType = _geomType(layer.geometryType())
        attributes = [f.name() for f in layer.pendingFields()]
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
                    popupInfo: "%(popup)s",
                    attributes: %(attributes)s,
                    geometryType: "%(geometryType)s"
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution, "dist": str(applayer.clusterDistance),
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup,
                 "source": source, "attributes": json.dumps(attributes), "geometryType":geometryType})
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
                    popupInfo: "%(popup)s",
                    attributes: %(attributes)s,
                    geometryType: "%(geometryType)s"
                });''' %
                {"opacity": layerOpacity, "name": title, "n":layerName,
                 "min": minResolution, "max": maxResolution,
                 "selectable": str(applayer.allowSelection).lower(),
                 "timeInfo": timeInfo, "id": layer.id(), "popup": popup,
                 "source": source, "attributes": json.dumps(attributes),
                 "geometryType":geometryType})

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

def resolveParameterValue(v, folder, name, app):
    expFile = os.path.join(folder, "resources", "js", "qgis2web_expressions.js")
    try:
        v = float(v)
        return v
    except:
        qgis2web = '<script src="./resources/js/qgis2web_expressions.js"></script>'
        if qgis2web not in app.scripts:
            app.scripts.append(qgis2web)
        name = name + ''.join(i for i in str(uuid.uuid4()) if i.isdigit())
        name = compile_to_file(v, name, "OpenLayers3", expFile)
        return "%s(context)" % name

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
        context = '''var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_%s'
        };''' % safeName(layer.name())
        try:
            renderer = layer.rendererV2()
            if isinstance(renderer, QgsSingleSymbolRendererV2):
                symbol = renderer.symbol()
                style = "var style = %s;" % getSymbolAsStyle(symbol, folder, layer, app)
                value = 'var value = "";'
                selectionStyle = "var style = " + getSymbolAsStyle(symbol,
                                    folder, layer, app, SELECTION_YELLOW)
            elif isinstance(renderer, QgsCategorizedSymbolRendererV2):
                defs += "var categories_%s = function(){ return {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(), folder, layer, app)))
                defs +=  ",\n".join(cats) + "};};"
                defs += "var categoriesSelected_%s = {" % safeName(layer.name())
                cats = []
                for cat in renderer.categories():
                    cats.append('"%s": %s' % (cat.value(), getSymbolAsStyle(cat.symbol(),
                                folder, layer, app, SELECTION_YELLOW)))
                defs +=  ",\n".join(cats) + "};"
                value = 'var value = feature.get("%s");' %  renderer.classAttribute()
                style = '''var style = categories_%s()[value];'''  % (safeName(layer.name()))
                selectionStyle = '''var style = categoriesSelected_%s[value]'''  % (safeName(layer.name()))
            elif isinstance(renderer, QgsGraduatedSymbolRendererV2):
                varName = "ranges_" + safeName(layer.name())
                defs += "var %s = function(){ return [" % varName
                ranges = []
                for ran in renderer.ranges():
                    symbolstyle = getSymbolAsStyle(ran.symbol(), folder, layer, app)
                    selectedSymbolStyle = getSymbolAsStyle(ran.symbol(), folder, layer, app, SELECTION_YELLOW)
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
                        function rules_%(n)s(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            %(js)s
                            if (!matchFound) {
                                ruleStyles = %(elsejs)s;
                            }
                            return ruleStyles;
                        }
                        var style = rules_%(n)s(value);
                        """
                elsejs = "[]"
                selectionElsejs = "[]"
                js = ""
                selectionJs = ""
                root_rule = renderer.rootRule()
                rules = root_rule.children()
                expFile = os.path.join(folder, "resources", "js",
                                       "qgis2web_expressions.js")
                for count, rule in enumerate(rules):
                    styleCode = getSymbolAsStyle(rule.symbol(), folder, layer, app)
                    selectionStyleCode = getSymbolAsStyle(rule.symbol(), folder, layer, app, SELECTION_YELLOW)
                    name = "".join((safeName(layer.name()), "rule", unicode(count)))
                    exp = rule.filterExpression()
                    if rule.isElse():
                        elsejs = styleCode
                        selectionElsejs = selectionStyleCode
                        continue
                    name = compile_to_file(exp, name, "OpenLayers3", expFile)
                    js += """
                    if (%s(context)) {
                      ruleStyles.push.apply(ruleStyles, %s);
                      matchFound = true;
                    }
                    """ % (name, styleCode)
                    js = js.strip()
                    selectionJs += """
                    if (%s(context)) {
                      ruleStyles.push.apply(ruleStyles, %s);
                      matchFound = true;
                    }
                    """ % (name, selectionStyleCode)
                    selectionJs = selectionJs.strip()
                value = ("var value = '';")
                style = template % {"n":safeName(layer.name()), "js":js, "elsejs":elsejs}
                selectionStyle = template % {"n":safeName(layer.name()), "js":selectionJs, "elsejs":selectionElsejs}
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
                        %(context)s
                        %(cluster)s
                        %(value)s
                        %(style)s
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": style,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                            "labels":labels, "context": context}
            selectionStyle = '''function(feature, resolution){
                        %(context)s
                        %(value)s
                        %(style)s
                        var allStyles = [];
                        %(labels)s
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    }''' % {"style": selectionStyle,  "layerName": safeName(layer.name()),
                            "value": value, "cluster": cluster,
                             "labels":labels, "context": context}
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
        js = "%s(labelContext)" % (name)
        js = js.strip()
        labelText = js
        app.scripts.append('<script src="./resources/js/qgis2web_expressions.js"></script>')
    else:
        labelText = 'feature.get("%s")' % labelField.replace('"', '\\"')

    try:
        useExpr = True
        ddSize = layer.customProperty("labeling/dataDefined/Size", None)
        if ddSize is not None:
            active, isExpr, expr = ddSize.split("~~")[:2]
            useExpr = active == "1" and isExpr == "1"
        if useExpr:
            size = resolveParameterValue(expr, folder, "fontsize", app)
        else:
            size = float(layer.customProperty("labeling/fontSize"))
        if layer.customProperty("labeling/fontSizeInMapUnits").lower() == "true":
            size = "pixelsFromMapUnits(%s)" % str(size)
        else:
            size = str(size)
    except:
        size = "10"

    if str(layer.customProperty("labeling/bufferDraw")).lower() == "true":
        rHalo = str(layer.customProperty("labeling/bufferColorR"))
        gHalo = str(layer.customProperty("labeling/bufferColorG"))
        bHalo = str(layer.customProperty("labeling/bufferColorB"))
        strokeWidth = str(layer.customProperty("labeling/bufferSize"))
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
        labelRes = " && resolution > %s " % str(min)
        labelRes += "&& resolution < %s" % str(max)
    else:
        labelRes = ""

    s = '''
        var labelContext = {
            feature: feature,
            variables: {},
            layer: 'lyr_%(layerName)s'
        };
        if (%(label)s !== null%(labelRes)s) {
            var labelText = String(%(label)s);
        } else {
            var labelText = "";
        }
        var key = value + "_" + labelText + "_" + String(resolution);
        if (!textStyleCache_%(layerName)s[key]){
            var size = %(size)s;
            var font = String(size) + 'px Calibri,sans-serif'
            var text = new ol.style.Text({
                  font: font,
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
            textStyleCache_%(layerName)s[key] = new ol.style.Style({zIndex: 1000, text: text});
        }
        allStyles.push(textStyleCache_%(layerName)s[key]);
        ''' % {"halo": halo, "offsetX": offsetX, "offsetY": offsetY, "rotation": rotation,
                "size": size, "color": color, "label": labelText, "labelRes": labelRes,
                "layerName": safeName(layer.name()), "textAlign": textAlign,
                "textBaseline": textBaseline}

    return s

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


def getSymbolAsStyle(symbol, folder, layer, app, color = None):
    styles = []
    alpha = symbol.alpha()
    stylesFolder = os.path.join(folder, "data", "styles")
    for i in xrange(symbol.symbolLayerCount()):
        sl = symbol.symbolLayer(i)
        props = sl.properties()
        def property(n):
            return resolveParameterValue(props[n], folder, n, app)
        if isinstance(sl, QgsSimpleMarkerSymbolLayerV2):
            style = "image: %s" % getShape(props, alpha, folder, color, app)
        elif isinstance(sl, QgsSvgMarkerSymbolLayerV2):
            sl2 = sl.clone()
            sl2.setSizeUnit(QgsSymbolV2.Pixel)
            sl2.setSize(100)
            newSymbol = QgsMarkerSymbolV2()
            newSymbol.appendSymbolLayer(sl2)
            newSymbol.deleteSymbolLayer(0)
            img = newSymbol.asImage(QSize(100, 100))
            filename, ext = os.path.splitext(os.path.basename(sl.path()))
            path = os.path.join(stylesFolder, filename + ".png")
            img.save(path)
            if "size_dd_expression" in props and int(props["size_dd_useexpr"]) and int(props["size_dd_active"]):
                size = property("size_dd_expression")
            else:
                size = sl.size()
            style = "image: %s" % getIcon(path, size, sl.sizeUnit())
        elif isinstance(sl, QgsSimpleLineSymbolLayerV2):
            if color is None:
                if 'color' in props:
                    strokeColor = getRGBAColor(props["color"], alpha)
                else:
                    strokeColor = getRGBAColor(props["line_color"], alpha)
            else:
                strokeColor = color
            if "width_dd_useexpr" in props and int(props["width_dd_useexpr"]) and int(props["width_dd_active"]):
                lineWidth = property("width_dd_expression")
            else:
                lineWidth = property("line_width")
            lineWidthUnits = props["line_width_unit"]
            if 'penstyle' in props:
                lineStyle = props["penstyle"]
            else:
                lineStyle = props["line_style"]
            offsetValue = sl.offset()
            if offsetValue:
                offset = '''geometry: function(feature){
                              var start = feature.getGeometry().getFirstCoordinate();
                              var end = feature.getGeometry().getLastCoordinate();
                              var dx = end[0] - start[0];
                              var dy = end[1] - start[1];
                              var rotation = Math.atan2(dy, dx);
                              offset = %s;
                              x = Math.sin(rotation) * offset;
                              y = Math.cos(rotation) * offset;
                              geom = feature.getGeometry().clone()
                              geom.translate(x, y);
                              return geom;
                            },''' % (str(offsetValue))
            else:
                offset = ""
            style = "%s stroke: %s" % (offset, getStrokeStyle(strokeColor, lineStyle,
                                                              lineWidth, lineWidthUnits))
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

            if ("width_border_dd_useexpr" in props and int(props["width_border_dd_useexpr"])
                    and int(props["width_border_dd_active"])):
                borderWidth = property("width_border_dd_expression")
            else:
                borderWidth = property("outline_width")
            borderWidthUnits = props["outline_width_unit"]
            x, y = sl.offset().x(), sl.offset().y()
            if x or y:
                offset = '''geometry: function(feature){
                                geom = feature.getGeometry().clone()
                                geom.translate(%s, %s);
                                return geom;
                            },\n''' % (str(x), str(y))
            else:
                offset = ""
            style = ('''%s stroke: %s,
                        fill: %s''' %
                    (offset, getStrokeStyle(borderColor, borderStyle, borderWidth, borderWidthUnits),
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
                app.variables.append('''var patternFill_%(p)i = new ol.style.Fill({});
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
            else:
                style = '''
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

                app.variables.append('''var patternFill_%(p)s = new ol.style.Fill({});
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
        if style:
            style = style + ",\nzIndex: %i" % sl.renderingPass()
        styles.append('''new ol.style.Style({
                            %s
                        })
                        ''' % style)
    return "[ %s]" % ",".join(styles)

def getShape(props, alpha, folder, color_, app):
    if "size_dd_expression" in props and int(props["size_dd_useexpr"]) and int(props["size_dd_active"]):
        size = resolveParameterValue(props["size_dd_expression"], folder, "size_dd_expression", app)
    else:
        size = str(props["size"])
    units = props["size_unit"]
    fullSize = getMeasure(size + "/ 2.0", units)
    halfSize = getMeasure(size + "/ 4.0", units)
    color =  color_ or getRGBAColor(props["color"], alpha)
    outlineColor = color_ or getRGBAColor(props["outline_color"], alpha)
    outlineWidth = float(props["outline_width"])
    shape = props["name"]
    if "star" in shape.lower():
        return getRegularShape(color, 5,  fullSize, halfSize, outlineColor, outlineWidth)
    elif "triangle" in shape.lower():
        return getRegularShape(color, 3,  fullSize, None, outlineColor, outlineWidth)
    elif "diamond" == shape.lower():
        return getRegularShape(color, 4,  fullSize, None, outlineColor, outlineWidth)
    elif "pentagon" == shape.lower():
        return getRegularShape(color, 5,  fullSize, None, outlineColor, outlineWidth)
    elif "rectangle" == shape.lower():
        return getRegularShape(color, 4,  fullSize, None, outlineColor, outlineWidth, 3.14159 / 4.0)
    elif "cross" == shape.lower():
        return getRegularShape(color, 4,  fullSize, 0, outlineColor, outlineWidth)
    elif "cross2" == shape.lower():
        return getRegularShape(color, 4,  fullSize, 0, outlineColor, outlineWidth, 3.14159 / 4.0)
    else:
        return getCircle(color, fullSize, outlineColor, outlineWidth)

def getCircle(color, size, outlineColor, outlineWidth):
    return ("new ol.style.Circle({radius: %s, stroke: %s, fill: %s})" %
                (str(size), getStrokeStyle(outlineColor, "solid", outlineWidth),
                 getFillStyle(color)))

def getRegularShape(color, points, radius1, radius2, outlineColor, outlineWidth, angle = 0):
    if radius2 is None:
        return ("new ol.style.RegularShape({points: %s, radius: %s, stroke: %s, fill: %s, angle: %s})" %
                (str(points), str(radius1),
                 getStrokeStyle(outlineColor, "solid", outlineWidth),
                 getFillStyle(color), str(angle)))
    else:
        return ("new ol.style.RegularShape({points: %s, radius1: %s, radius2: %s, stroke: %s, fill: %s, angle: %s})" %
                (str(points), str(radius1), str(radius2),
                 getStrokeStyle(outlineColor, "solid", outlineWidth),
                 getFillStyle(color), angle))

def getIcon(path, size, units):
    size = getMeasure(size, units);
    return '''new ol.style.Icon({
                  scale: %(s)s / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "%(path)s",
            })''' % {"s": size, "path": "./data/styles/" + os.path.basename(path)}

def getMeasure(value, units):
    if units == "MapUnit" or units == 1:
        return "pixelsFromMapUnits(%s)" % str(value)
    elif units == "MM" or units == 0:
        return "pixelsFromMm(%s)" % str(value)
    else:
        return value

def getStrokeStyle(color, style, width, units="MM"):
    dash = "null"
    if style == "no":
        width = "0"
        color = '"rgba(0,0,0,0.0)"'
    else:
        width = getMeasure(width, units)
        if style != "solid":
            dash = "[6]"
    return "new ol.style.Stroke({color: %s, lineDash: %s, width: %s})" % (color, dash, width)

def getFillStyle(color):
    return "new ol.style.Fill({color: %s})" % color
