injectTapEventPlugin();

var defaultFill = new ol.style.Fill({
  color: 'rgba(255,255,255,0.4)'
});
var defaultStroke = new ol.style.Stroke({
  color: '#3399CC',
  width: 1.25
});
var defaultSelectionFill = new ol.style.Fill({
  color: 'rgba(255,255,0,0.4)'
});
var defaultSelectionStroke = new ol.style.Stroke({
  color: '#FFFF00',
  width: 1.25
});


                    var textStyleCache_points_cluster={}
                    var clusterStyleCache_points_cluster={}
                    var style_points_cluster = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points_cluster'
        };
                        var features = feature.get('features');
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
                                    var color = '#3399CC'
                                    var style = clusterStyleCache_points_cluster[numVisible]
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
                                        clusterStyleCache_points_cluster[numVisible] = style;
                                    }
                                    return style;
                                }
                            }
                            feature = feature.get('features')[0];
                            
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(77,158,253,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_points_cluster = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points_cluster'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

             var style_points_heatmap = [
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
              var selectionStyle_points_heatmap = [
               new ol.style.Style({
                 image: new ol.style.Circle({
                   fill: defaultSelectionFill,
                   stroke: defaultSelectionStroke,
                   radius: 5
                 }),
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
               })
             ];

                    var textStyleCache_points={}
                    var clusterStyleCache_points={}
                    var style_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points'
        };
                        
                        var value = '';
                        
                        function rules_points(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (pointsrule0_eval_expression(context) && resolution > 0.280000672002 && resolution < 28.0000672002) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(182,246,102,1.0)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (pointsrule1_eval_expression(context) && resolution > 28.0000672002 && resolution < 280.000672002) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(104,139,99,1.0)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (pointsrule2_eval_expression(context) && resolution > 280.000672002 && resolution < 560.001344003) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(237,12,49,1.0)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points'
        };
                        var value = '';
                        
                        function rules_points(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (pointsrule0_eval_expression(context) && resolution > 0.280000672002 && resolution < 28.0000672002) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (pointsrule1_eval_expression(context) && resolution > 28.0000672002 && resolution < 280.000672002) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (pointsrule2_eval_expression(context) && resolution > 280.000672002 && resolution < 560.001344003) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_points2_labels={}
                    var clusterStyleCache_points2_labels={}
                    var style_points2_labels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points2_labels'
        };
                        
                        var value = '';
                        var style = [
                                   new ol.style.Style({})
                                 ];
                        var allStyles = [];
                        
        var labelContext = {
            feature: feature,
            variables: {},
            layer: 'lyr_points2_labels'
        };
        if (feature.get("lbl") !== null) {
            var labelText = String(feature.get("lbl"));
        } else {
            var labelText = "";
        }
        var key = value + "_" + labelText + "_" + String(resolution);
        if (!textStyleCache_points2_labels[key]){
            var size = 14.0 * 2;
            var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
            var text = new ol.style.Text({
                  font: font,
                  text: labelText,
                  fill: new ol.style.Fill({
                    color: "rgba(0, 0, 0, 255)"
                  }),
                  textBaseline: "middle",
                  textAlign: "start",
                  rotation: -0.0,
                  offsetX: 0,
                  offsetY: 0 
                });
            textStyleCache_points2_labels[key] = new ol.style.Style({zIndex: 1000, text: text});
        }
        allStyles.push(textStyleCache_points2_labels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_points2_labels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points2_labels'
        };
                        var value = '';
                        var style = [
                                   new ol.style.Style({})
                                 ];
                        var allStyles = [];
                        
        var labelContext = {
            feature: feature,
            variables: {},
            layer: 'lyr_points2_labels'
        };
        if (feature.get("lbl") !== null) {
            var labelText = String(feature.get("lbl"));
        } else {
            var labelText = "";
        }
        var key = value + "_" + labelText + "_" + String(resolution);
        if (!textStyleCache_points2_labels[key]){
            var size = 14.0 * 2;
            var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
            var text = new ol.style.Text({
                  font: font,
                  text: labelText,
                  fill: new ol.style.Fill({
                    color: "rgba(0, 0, 0, 255)"
                  }),
                  textBaseline: "middle",
                  textAlign: "start",
                  rotation: -0.0,
                  offsetX: 0,
                  offsetY: 0 
                });
            textStyleCache_points2_labels[key] = new ol.style.Style({zIndex: 1000, text: text});
        }
        allStyles.push(textStyleCache_points2_labels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group',
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true,
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var cluster_points_cluster = new ol.source.Cluster({
                    distance: 40.0,
                    source: new ol.source.Vector(),
                });
                var lyr_points_cluster = new ol.layer.Vector({
                    opacity: 1.0,
                    source: cluster_points_cluster, 
minResolution:2800.00672002,
 maxResolution:28000.0672002,

                    style: style_points_cluster,
                    selectedStyle: selectionStyle_points_cluster,
                    title: "points_cluster",
                    id: "points_heatmap_copy20170518133711174",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Point"
                });
var lyr_points_cluster_overview = new ol.layer.Vector({
                    source: cluster_points_cluster, 
minResolution:2800.00672002,
 maxResolution:28000.0672002,

                    style: style_points_cluster});
points_cluster_geojson_callback = function(geojson) {
                              lyr_points_cluster.getSource().getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_points_cluster_overview.getSource().setSource(lyr_points_cluster.getSource().getSource());
                        };
var lyr_points_heatmap = new ol.layer.Heatmap({
                    source: new ol.source.Vector(),
                    
minResolution:560.001344003,
 maxResolution:2800.00672002,

                    radius: 10 * 2,
                    gradient: ['#ffffff', '#000000'],
                    blur: 15,
                    shadow: 250,
                    
                    title: "points_heatmap"
                    });
var lyr_points_heatmap_overview = new ol.layer.Heatmap({
                    source: new ol.source.Vector(),
                    
minResolution:560.001344003,
 maxResolution:2800.00672002,

                    radius: 10 * 2,
                    gradient: ['#ffffff', '#000000'],
                    blur: 15,
                    shadow: 250,
                    
                    title: "points_heatmap"
                    });
points_heatmap_geojson_callback = function(geojson) {
                              lyr_points_heatmap.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_points_heatmap_overview.setSource(lyr_points_heatmap.getSource());
                        };
var lyr_points = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_points,
                    selectedStyle: selectionStyle_points,
                    title: "points",
                    id: "points_shp20150708141950508",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Point"
                });
var lyr_points_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_points});
points_geojson_callback = function(geojson) {
                              lyr_points.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_points_overview.setSource(lyr_points.getSource());
                        };
var lyr_points2_labels = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_points2_labels,
                    selectedStyle: selectionStyle_points2_labels,
                    title: "points2_labels",
                    id: "points2_labels20170522083800220",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["lbl"],
                    geometryType: "Point"
                });
var lyr_points2_labels_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_points2_labels});
points2_labels_geojson_callback = function(geojson) {
                              lyr_points2_labels.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_points2_labels_overview.setSource(lyr_points2_labels.getSource());
                        };

lyr_points_cluster.setVisible(true);
lyr_points_heatmap.setVisible(true);
lyr_points.setVisible(true);
lyr_points2_labels.setVisible(true);
var layersList = [lyr_points_cluster,lyr_points_heatmap,lyr_points,lyr_points2_labels];
var layersMap  = {'lyr_points_cluster':lyr_points_cluster,'lyr_points_heatmap':lyr_points_heatmap,'lyr_points':lyr_points,'lyr_points2_labels':lyr_points2_labels};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [-6093721.407950, -1412194.714072, 7827740.566531, 2902352.606335];
var unitsConversion = 111325.0;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});

function pixelsFromMapUnits(size) {
    return size / map.getView().getResolution() * unitsConversion;
};

function pixelsFromMm(size) {
    return 96 / 25.4 * size;
};

var BasicApp = React.createClass({
  childContextTypes: {
    muiTheme: React.PropTypes.object
  },
  getChildContext: function() {
    return {
      muiTheme: getMuiTheme()
    };
  },
  componentDidMount: function() {
    
  },
  _toggle: function(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  },
  _toggleTable: function() {
    this._toggle(document.getElementById('table-panel'));
    this.refs.table.getWrappedInstance().setDimensionsOnState();
  },
  _toggleWFST: function() {
    this._toggle(document.getElementById('wfst'));
  },
  _toggleQuery: function() {
    this._toggle(document.getElementById('query-panel'));
  },
  _toggleEdit: function() {
    this._toggle(document.getElementById('edit-tool-panel'));
  },
  _hideAboutPanel: function(evt) {
    evt.preventDefault();
    document.getElementById('about-panel').style.display = 'none';
  },
  _toggleChartPanel: function(evt) {
    evt.preventDefault();
    this._toggle(document.getElementById('chart-panel'));
  },
  render: function() {
    var toolbarOptions = {showMenuIconButton: false, title:"My Web App"};
    return React.createElement("div", {id: 'content'},
      React.createElement(Header, toolbarOptions ),
      React.createElement(MapPanel, {useHistory: true, extent: originalExtent, id: 'map', map: map}
        ,
React.createElement("div", {id: 'popup', className: 'ol-popup'},
                                    React.createElement(InfoPopup, {toggleGroup: 'navigation', map: map, hover: false})
                                  )
      )
      
    );
  }
});

ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(BasicApp)), document.getElementById('main'));
