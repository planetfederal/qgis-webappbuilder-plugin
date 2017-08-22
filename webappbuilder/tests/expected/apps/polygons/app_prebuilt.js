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

var patternFill_5 = new ol.style.Fill({});
                        var patternImg_5 = new Image();
                        patternImg_5.src = './data/styles/patternFill_5.png';
                        patternImg_5.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_5, 'repeat');
                          patternFill_5 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_6 = new ol.style.Fill({});
                        var patternImg_6 = new Image();
                        patternImg_6.src = './data/styles/patternFill_6.png';
                        patternImg_6.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_6, 'repeat');
                          patternFill_6 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_7 = new ol.style.Fill({});
                        var patternImg_7 = new Image();
                        patternImg_7.src = './data/styles/patternFill_7.png';
                        patternImg_7.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_7, 'repeat');
                          patternFill_7 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_8 = new ol.style.Fill({});
                        var patternImg_8 = new Image();
                        patternImg_8.src = './data/styles/patternFill_8.png';
                        patternImg_8.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_8, 'repeat');
                          patternFill_8 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_17 = new ol.style.Fill({});
                        var patternImg_17 = new Image();
                        patternImg_17.src = './data/styles/patternFill_17.png';
                        patternImg_17.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_17, 'repeat');
                          patternFill_17 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_18 = new ol.style.Fill({});
                        var patternImg_18 = new Image();
                        patternImg_18.src = './data/styles/patternFill_18.png';
                        patternImg_18.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_18, 'repeat');
                          patternFill_18 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_19 = new ol.style.Fill({});
                        var patternImg_19 = new Image();
                        patternImg_19.src = './data/styles/patternFill_19.png';
                        patternImg_19.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_19, 'repeat');
                          patternFill_19 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_20 = new ol.style.Fill({});
                        var patternImg_20 = new Image();
                        patternImg_20.src = './data/styles/patternFill_20.png';
                        patternImg_20.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_20, 'repeat');
                          patternFill_20 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var categories_polygons = function(){ return {"2": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: [6], width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(32,225,68,1.0)"}),
zIndex: 0
                            })
                            ],
"3": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1)}),
                            fill: new ol.style.Fill({color: "rgba(116,229,72,1.0)"}),
zIndex: 0
                            })
                            ],
"4": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(0,0,0,0.0)"}),
zIndex: 0
                            })
                            ],
"5": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(217,116,133,1.0)"}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                fill: patternFill_5,
zIndex: 0
                            })
                            ],
"6": [ new ol.style.Style({
                                fill: patternFill_6,
zIndex: 0
                            })
                            ],
"7": [ new ol.style.Style({
                                fill: patternFill_7,
zIndex: 0
                            })
                            ],
"8": [ new ol.style.Style({
                                fill: patternFill_8,
zIndex: 0
                            })
                            ],
"9": [ new ol.style.Style({
                                
                            })
                            ],
"10": [ new ol.style.Style({
                                
                            })
                            ],
"11": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(244,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(110,181,234,1.0)"}),
zIndex: 0
                            })
                            ],
"12": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(29,37,130,1.0)"}),
zIndex: 0
                            })
                            ]};};var categoriesSelected_polygons = {"2": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ],
"3": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ],
"4": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ],
"5": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                fill: patternFill_17,
zIndex: 0
                            })
                            ],
"6": [ new ol.style.Style({
                                fill: patternFill_18,
zIndex: 0
                            })
                            ],
"7": [ new ol.style.Style({
                                fill: patternFill_19,
zIndex: 0
                            })
                            ],
"8": [ new ol.style.Style({
                                fill: patternFill_20,
zIndex: 0
                            })
                            ],
"9": [ new ol.style.Style({
                                
                            })
                            ],
"10": [ new ol.style.Style({
                                
                            })
                            ],
"11": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ],
"12": [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ]};
                    var textStyleCache_polygons={}
                    var clusterStyleCache_polygons={}
                    var style_polygons = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons'
        };
                        
                        var value = feature.get("n");
                        var style = categories_polygons()[value];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_polygons = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons'
        };
                        var value = feature.get("n");
                        var style = categoriesSelected_polygons[value]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_polygons_cant_select={}
                    var clusterStyleCache_polygons_cant_select={}
                    var style_polygons_cant_select = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons_cant_select'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(152,219,150,1.0)"}),
zIndex: 0
                            })
                            ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_polygons_cant_select = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons_cant_select'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
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
var lyr_polygons = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_polygons,
                    selectedStyle: selectionStyle_polygons,
                    title: "polygons",
                    id: "polygons20170524084645695",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Polygon"
                });
polygons_geojson_callback = function(geojson) {
                              lyr_polygons.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_polygons_cant_select = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_polygons_cant_select,
                    selectedStyle: selectionStyle_polygons_cant_select,
                    title: "polygons_cant_select",
                    id: "polygons_cant_select20170524084620499",
                    filters: [],
                    timeInfo: null,
                    isSelectable: false,
                    popupInfo: "<table class='popup-table'><tr><th>Attribute</th><th>Value</th><tr><td>n</td><td style='text-align:right'>[n]</td></tr></table>",
                    attributes: ["n"],
                    geometryType: "Polygon"
                });
polygons_cant_select_geojson_callback = function(geojson) {
                              lyr_polygons_cant_select.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };

lyr_polygons.setVisible(true);
lyr_polygons_cant_select.setVisible(true);
var layersList = [lyr_polygons,lyr_polygons_cant_select];
var layersMap  = {'lyr_polygons':lyr_polygons,'lyr_polygons_cant_select':lyr_polygons_cant_select};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [-5317761.624767, -439604.376249, 5344570.145096, 1683909.699684];
var unitsConversion = 111325.0;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});



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
    var toolbarOptions = {title:"Polygons"};
    return React.createElement("div", {id: 'content'},
      React.createElement(Header, toolbarOptions ,
React.createElement(Select, {toggleGroup: 'navigation', map:map}),
React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})),
      React.createElement(MapPanel, {useHistory: true, extent: originalExtent, id: 'map', map: map}
        ,
React.createElement("div", {id: 'about-panel', className:'about-panel'},
                                        React.createElement("a", {href:'#', id:'about-panel-closer',
                                            className:'about-panel-closer', onClick:this._hideAboutPanel.bind(this)},
                                              "X"
                                        ),
                                        React.createElement("div", {dangerouslySetInnerHTML:{__html: 'You should be able to select the rectangles on the left, but not those on the right. Hovering over the polygons in the right should show a popup'}})
                                    ),
React.createElement("div", {id: 'popup', className: 'ol-popup'},
                                    React.createElement(InfoPopup, {toggleGroup: 'navigation', map: map, hover: true})
                                  )
      )
      
    );
  }
});

ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(BasicApp)), document.getElementById('main'));
