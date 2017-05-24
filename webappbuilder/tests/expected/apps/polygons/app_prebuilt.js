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

var patternFill_1 = new ol.style.Fill({});
                        var patternImg_1 = new Image();
                        patternImg_1.src = './data/styles/patternFill_1.svg';
                        patternImg_1.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_1, 'repeat');
                          patternFill_1 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_2 = new ol.style.Fill({});
                        var patternImg_2 = new Image();
                        patternImg_2.src = './data/styles/patternFill_2.svg';
                        patternImg_2.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_2, 'repeat');
                          patternFill_2 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_3 = new ol.style.Fill({});
                        var patternImg_3 = new Image();
                        patternImg_3.src = './data/styles/patternFill_3.svg';
                        patternImg_3.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_3, 'repeat');
                          patternFill_3 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_4 = new ol.style.Fill({});
                        var patternImg_4 = new Image();
                        patternImg_4.src = './data/styles/patternFill_4.svg';
                        patternImg_4.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_4, 'repeat');
                          patternFill_4 = new ol.style.Fill({
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
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.0)}),
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
                            fill: patternFill_1,
zIndex: 0
                        })
                        ],
"6": [ new ol.style.Style({
                            fill: patternFill_2,
zIndex: 0
                        })
                        ],
"7": [ new ol.style.Style({
                            fill: patternFill_3,
zIndex: 0
                        })
                        ],
"8": [ new ol.style.Style({
                            fill: patternFill_4,
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
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}),
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
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ],
"6": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ],
"7": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ],
"8": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
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
var lyr_polygons_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_polygons});
polygons_geojson_callback = function(geojson) {
                              lyr_polygons.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_polygons_overview.setSource(lyr_polygons.getSource());
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
var lyr_polygons_cant_select_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_polygons_cant_select});
polygons_cant_select_geojson_callback = function(geojson) {
                              lyr_polygons_cant_select.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_polygons_cant_select_overview.setSource(lyr_polygons_cant_select.getSource());
                        };

lyr_polygons.setVisible(true);
lyr_polygons_cant_select.setVisible(true);
var layersList = [lyr_polygons,lyr_polygons_cant_select];
var layersMap  = {'lyr_polygons':lyr_polygons,'lyr_polygons_cant_select':lyr_polygons_cant_select};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [-2365871.712687, -439604.376249, 2392680.233016, 1683909.699684];
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
