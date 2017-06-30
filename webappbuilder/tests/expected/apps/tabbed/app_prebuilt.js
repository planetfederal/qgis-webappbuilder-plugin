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


                    var textStyleCache_raleighdowntown={}
                    var clusterStyleCache_raleighdowntown={}
                    var style_raleighdowntown = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_raleighdowntown'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,192,1.0)", lineDash: null, width: pixelsFromMm(0.66)}),
                            fill: new ol.style.Fill({color: "rgba(198,198,198,0.0)"}),
zIndex: 0
                            })
                            ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_raleighdowntown = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_raleighdowntown'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.66)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_streets={}
                    var clusterStyleCache_streets={}
                    var style_streets = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_streets'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.294118)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                            })
                            ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_streets = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_streets'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                            })
                            ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var ranges_census_blocks_21 = function(){ return [[0.000000, 0.000000,
 [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255,255,255,0.0)", lineDash: null, width: pixelsFromMm(0.1)}),
                            fill: new ol.style.Fill({color: "rgba(255,255,255,0.0)"}),
zIndex: 0
                            })
                            ], [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.1)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]],
[0.000000, 13.404400,
 [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(253,204,49,1.0)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(253,204,49,1.0)"}),
zIndex: 0
                            })
                            ], [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]],
[13.404400, 80.294004,
 [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(186,213,74,1.0)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(186,213,74,1.0)"}),
zIndex: 0
                            })
                            ], [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]],
[80.294004, 180.695471,
 [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,167,141,1.0)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(0,167,141,1.0)"}),
zIndex: 0
                            })
                            ], [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]],
[180.695471, 5306.301793,
 [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(39,113,140,1.0)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(39,113,140,1.0)"}),
zIndex: 0
                            })
                            ], [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.2)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]]];};
                    var textStyleCache_census_blocks_21={}
                    var clusterStyleCache_census_blocks_21={}
                    var style_census_blocks_21 = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_census_blocks_21'
        };
                        
                        var value = feature.get("pop_dens");
                        var style = ranges_census_blocks_21()[0][2];
                            var ranges = ranges_census_blocks_21();
                            for (var i = 0, ii = ranges.length; i < ii; i++){
                                var range = ranges[i];
                                if (value > range[0] && value<=range[1]){
                                    style = range[2];
                                    break;
                                }
                            }
                            
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_census_blocks_21 = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_census_blocks_21'
        };
                        var value = feature.get("pop_dens");
                        var style = ranges_census_blocks_21[0][3];
                            for (var i = 0; i < ranges_census_blocks_21.length; i++){
                                var range = ranges_census_blocks_21[i];
                                if (value > range[0] && value<=range[1]){
                                    style = range[3];
                                    break;
                                }
                            }
                            
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_parks={}
                    var clusterStyleCache_parks={}
                    var style_parks = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_parks'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(128,152,72,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(186,221,105,1.0)"}),
zIndex: 0
                            })
                            ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_parks'
            };
            if (getFeatureAttribute(feature, "NAME") !== null) {
                var labelText = String(getFeatureAttribute(feature, "NAME"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_parks[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "Ubuntu",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(33, 103, 28, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_parks[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_parks[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_parks = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_parks'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_parks'
            };
            if (getFeatureAttribute(feature, "NAME") !== null) {
                var labelText = String(getFeatureAttribute(feature, "NAME"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_parks[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "Ubuntu",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(33, 103, 28, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_parks[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_parks[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_landmarks={}
                    var clusterStyleCache_landmarks={}
                    var style_landmarks = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_landmarks'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(31,120,180,1.0)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_landmarks = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_landmarks'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group',
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true,
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var lyr_raleighdowntown = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_raleighdowntown,
                    selectedStyle: selectionStyle_raleighdowntown,
                    title: "Raleigh downtown",
                    id: "raleigh_downtown20161228143332835",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["OBJECTID", "OVERLAY", "OLAY_DECOD", "ZONE_CASE", "ORDINANCE", "EFF_DATE", "OVERLAY_TY", "Shape_Leng", "Shape_Area"],
                    geometryType: "Polygon"
                });
raleighdowntown_geojson_callback = function(geojson) {
                              lyr_raleighdowntown.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_streets = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_streets,
                    selectedStyle: selectionStyle_streets,
                    title: "Streets",
                    id: "raleigh_downtown_streets20161228143254740",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["STREET_ID", "CARTONAME", "LABELNAME", "FRLEFT_A", "TOLEFT_A", "FRRIGHT_A", "TORIGHT_A", "L_ZIPNAME", "R_ZIPNAME", "ZIP_L", "ZIP_R", "CLASSNAME", "STID", "STATEROAD", "CORP", "DIR_PRE", "STNAME", "STYPE", "DIR_SUF", "FRLEFT", "TOLEFT", "FRRIGHT", "TORIGHT", "SPEED", "F_ELEV", "T_ELEV", "ONE_WAY", "FT_COST", "TF_COST", "CARTO_LEVE", "INPUT_", "CLASS", "STSEG", "STATE", "ERROR", "COMMENTS", "CREATE_DAT", "CREATE_WHO", "EDIT_DATE", "EDIT_WHO", "Shape_Leng", "FLAG", "OPID"],
                    geometryType: "Line"
                });
streets_geojson_callback = function(geojson) {
                              lyr_streets.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_census_blocks_21 = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_census_blocks_21,
                    selectedStyle: selectionStyle_census_blocks_21,
                    title: "Census_blocks_2010",
                    id: "raleigh_downtown_blocks_201020170320131722800",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["STATEFP10", "COUNTYFP10", "TRACTCE10", "BLOCKCE10", "GEOID10", "NAME10", "Shape_Leng", "Shape_Area", "TOTAL_POP", "TOTAL_HU", "OCCUPIED", "VACANT", "pop_dens"],
                    geometryType: "Polygon"
                });
census_blocks_21_geojson_callback = function(geojson) {
                              lyr_census_blocks_21.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_parks = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_parks,
                    selectedStyle: selectionStyle_parks,
                    title: "Parks",
                    id: "raleigh_downtown_parks20170320123421893",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["OBJECTID", "NAME", "PARK_TYPE", "FILE_NUMBE", "ID_NUMBER", "DEVELOPED", "MAP_ACRES", "SHAPEAREA", "SHAPELEN"],
                    geometryType: "Polygon"
                });
parks_geojson_callback = function(geojson) {
                              lyr_parks.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_landmarks = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_landmarks,
                    selectedStyle: selectionStyle_landmarks,
                    title: "landmarks",
                    id: "raleigh_downtown_landmarks20170320122528962",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["OBJECTID", "NAME", "ADDRESS", "ORDINANCE", "ORD_DATE", "NR_STATUS", "SIGN_PERIO", "ACREAGE", "ORD_LINK"],
                    geometryType: "Point"
                });
landmarks_geojson_callback = function(geojson) {
                              lyr_landmarks.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var group_pointsofinterest = new ol.layer.Group({
                                layers: [lyr_parks,lyr_landmarks],
                                showContent: true,
                                isGroupExpanded: true,
                                title: "points of interest"});

lyr_raleighdowntown.setVisible(true);
lyr_streets.setVisible(true);
lyr_census_blocks_21.setVisible(true);
lyr_parks.setVisible(true);
lyr_landmarks.setVisible(true);
var layersList = [lyr_raleighdowntown,lyr_streets,lyr_census_blocks_21,group_pointsofinterest];
var layersMap  = {'lyr_raleighdowntown':lyr_raleighdowntown,'lyr_streets':lyr_streets,'lyr_census_blocks_21':lyr_census_blocks_21,'group_pointsofinterest':group_pointsofinterest};
var legendData = {"raleigh_downtown20161228143332835": [{"href": "0_0.png", "title": ""}], "raleigh_downtown_blocks_201020170320131722800": [{"href": "2_0.png", "title": "0.0-0.0"}, {"href": "2_1.png", "title": "0.0-13.4043999293"}, {"href": "2_2.png", "title": "13.4043999293-80.2940043564"}, {"href": "2_3.png", "title": "80.2940043564-180.695471118"}, {"href": "2_4.png", "title": "180.695471118-5306.30179256"}], "raleigh_downtown_parks20170320123421893": [{"href": "3_0.png", "title": ""}], "raleigh_downtown_streets20161228143254740": [{"href": "1_0.png", "title": ""}], "raleigh_downtown_landmarks20170320122528962": [{"href": "4_0.png", "title": ""}]};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [-8758974.611255, 4267399.165927, -8749941.716367, 4273506.920653];
var unitsConversion = 1;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});



var TabbedApp = React.createClass({
  childContextTypes: {
    muiTheme: React.PropTypes.object
  },
  getChildContext: function() {
    return {
      muiTheme: getMuiTheme()
    };
  },
  getInitialState: function() {
    return {leftNavOpen: false, addLayerOpen: false};
  },
  componentDidMount: function() {
    
  },
  leftNavClose: function(value) {
    this.setState({
      leftNavOpen: false
    }, function() {
      map.updateSize();
    });
  },
  leftNavOpen: function(value) {
    this.setState({
      leftNavOpen: true
    }, function() {
      map.updateSize();
    });
  },
  layerListOpen: function(value) {
    this.setState({
      addLayerOpen: true
    });
  },
  layerListClose: function(value) {
    this.setState({
      addLayerOpen: false
    });
  },
  _toggle: function(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  },
  _toggleEdit: function() {
    this._toggle(document.getElementById('edit-tool-panel'));
  },
  _toggleWFST: function() {
    this._toggle(document.getElementById('wfst'));
  },
  render: function() {
    var leftNavWidth = 360;
    var toolbarOptions = Object.assign({
      style: {left: this.state.leftNavOpen ? leftNavWidth : 0, width: this.state.leftNavOpen ? 'calc(100% - ' + leftNavWidth + 'px)' : '100%'},
      showLeftIcon: !this.state.leftNavOpen,
      onLeftIconTouchTap: this.leftNavOpen
    }, {title:"My Web App"});
    return React.createElement("div", {id: 'content'},
      React.createElement(LeftNav, {tabList: [React.createElement(Tab,{key:1, value:1, label:"Geocoding"},
                                    React.createElement("div", {id:"geocoding-tab"},
                                        React.createElement(Geocoding, {maxResults:5})
                                    ),
                                    React.createElement("div", {id:"geocoding-results"},
                                        React.createElement(GeocodingResults, {map:map,
                                        zoom:10})
                                    )
                                ),
React.createElement(Tab,{key:2, value:2, label:'layers', onActive: this.layerListOpen.bind(this)},
                                 React.createElement("div",{id: "layerlist"},
                                    React.createElement(LayerList, {showOpacity:false, showDownload:false,
                                        addLayer: {
                                          open: this.state.addLayerOpen,
                                          onRequestClose:this.layerListClose.bind(this)
                                        },
                                        inlineDialogs: true,
                                        icon: React.createElement(Button, {buttonType: "Flat", label: "ADD"}),
                                        showZoomTo:false, allowReordering:false,
                                        allowFiltering:true,
                                        downloadFormat:'GeoJSON', showUpload:true, map:map,
                                        includeLegend:true, allowStyling:true, showTable:true})))], open: this.state.leftNavOpen, onRequestClose: this.leftNavClose}),
      React.createElement("div", undefined,
        React.createElement(Header, toolbarOptions ),
        React.createElement("div", {className: 'map', style: {left: this.state.leftNavOpen ? leftNavWidth : 0, width: this.state.leftNavOpen ? 'calc(100% - ' + leftNavWidth + 'px)' : '100%'}},
          React.createElement(MapPanel, {id: 'map', useHistory: true, extent: originalExtent, map: map}
            ,
React.createElement("div", {id: 'popup', className: 'ol-popup'},
                                    React.createElement(InfoPopup, {toggleGroup: 'navigation', map: map, hover: false})
                                  )
          )
          ,
React.createElement("div",{id: "legend"},
                                React.createElement(QGISLegend, {map:map, size:20, legendBasePath:'./resources/legend/',showExpandedOnStartup:false, legendData:legendData})
                            )
        )
      )
    );
  }
});

ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(TabbedApp)), document.getElementById('main'));
