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


                    var textStyleCache_migration_at_213_collapsed_directionswanderungen213linestring={}
                    var clusterStyleCache_migration_at_213_collapsed_directionswanderungen213linestring={}
                    var style_migration_at_213_collapsed_directionswanderungen213linestring = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_migration_at_213_collapsed_directionswanderungen213linestring'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                                geometry: function(feature){
                            var curve = bezier(geomgenerator674377244746970594098582_eval_expression(context));
                            var width = kilometersFromPixels(pixelsFromMm(arrow_width_dd_expression74155417458606378_eval_expression(context))) * 1000.0 / 2.0 ;
                            if (width > 0){
                                var length = kilometersFromPixels(pixelsFromMm(head_length_dd_expression5390563927422695764782661_eval_expression(context))) * 1000;
                                var thickness = width + kilometersFromPixels(pixelsFromMm(head_thickness_dd_expression196046489053596_eval_expression(context))) * 1000
                                var turfCurve = geojsonFromGeometry(curve);
                                var dist = turf.lineDistance(turfCurve) - length / 1000.0;
                                var shortCurve = geometryFromGeojson(turf.lineSliceAlong(turfCurve, 0, dist))
                                var center = shortCurve.getLastCoordinate();
                                var last = shortCurve.getCoordinates()[shortCurve.getCoordinates().length - 2]
                                var tip = curve.getLastCoordinate();
                                var dx = center[0] - last[0];
                                var dy = center[1] - last[1];
                                var angle = Math.atan2(dy, dx) - (Math.PI / 2.0);
                                var p1 = [center[0] + Math.cos(angle) * thickness,  center[1] + Math.sin(angle) * thickness];
                                var p2 = [center[0] - Math.cos(angle) * thickness,  center[1] - Math.sin(angle) * thickness];
                                var arrow = new ol.geom.Polygon([[tip, p1, p2, tip]]);
                                var buffer = fnc_buffer([shortCurve, width], {});
                                var union = fnc_union([arrow, buffer], {});
                                return union;
                            }
                            else{
                                return null;
                            }
                        },
stroke: new ol.style.Stroke({color: "rgba(255,255,255,1.0)", lineDash: null, width: pixelsFromMm(0.4)}),
                            fill: new ol.style.Fill({color: "rgba(0,0,0,1.0)"}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                geometry: geomgenerator7058809145244317259_eval_expression(context),
stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255,255,255,1.0)"}),
zIndex: 1
                            })
                            ,new ol.style.Style({
                                geometry: geomgenerator063256762446830280373864_eval_expression(context),
stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255,255,255,1.0)"}),
zIndex: 2
                            })
                            ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_migration_at_213_collapsed_directionswanderungen213linestring = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_migration_at_213_collapsed_directionswanderungen213linestring'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                                geometry: function(feature){
                            var curve = bezier(geomgenerator195139411455929428336811_eval_expression(context));
                            var width = kilometersFromPixels(pixelsFromMm(arrow_width_dd_expression2214555243499804050118_eval_expression(context))) * 1000.0 / 2.0 ;
                            if (width > 0){
                                var length = kilometersFromPixels(pixelsFromMm(head_length_dd_expression9945709994109909802_eval_expression(context))) * 1000;
                                var thickness = width + kilometersFromPixels(pixelsFromMm(head_thickness_dd_expression964216617436854871448_eval_expression(context))) * 1000
                                var turfCurve = geojsonFromGeometry(curve);
                                var dist = turf.lineDistance(turfCurve) - length / 1000.0;
                                var shortCurve = geometryFromGeojson(turf.lineSliceAlong(turfCurve, 0, dist))
                                var center = shortCurve.getLastCoordinate();
                                var last = shortCurve.getCoordinates()[shortCurve.getCoordinates().length - 2]
                                var tip = curve.getLastCoordinate();
                                var dx = center[0] - last[0];
                                var dy = center[1] - last[1];
                                var angle = Math.atan2(dy, dx) - (Math.PI / 2.0);
                                var p1 = [center[0] + Math.cos(angle) * thickness,  center[1] + Math.sin(angle) * thickness];
                                var p2 = [center[0] - Math.cos(angle) * thickness,  center[1] - Math.sin(angle) * thickness];
                                var arrow = new ol.geom.Polygon([[tip, p1, p2, tip]]);
                                var buffer = fnc_buffer([shortCurve, width], {});
                                var union = fnc_union([arrow, buffer], {});
                                return union;
                            }
                            else{
                                return null;
                            }
                        },
stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.4)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                geometry: geomgenerator5378200546104036077414_eval_expression(context),
stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 1
                            })
                            ,new ol.style.Style({
                                geometry: geomgenerator8834468867579617_eval_expression(context),
stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                            fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 2
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
var lyr_migration_at_213_collapsed_directionswanderungen213linestring = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_migration_at_213_collapsed_directionswanderungen213linestring,
                    selectedStyle: selectionStyle_migration_at_213_collapsed_directionswanderungen213linestring,
                    title: "migration_AT_2013_collapsed_directions wanderungen2013 LineString",
                    id: "migration_AT_2013_collapsed_directions20170613083043483",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "weight"],
                    geometryType: "Line"
                });
migration_at_213_collapsed_directionswanderungen213linestring_geojson_callback = function(geojson) {
                              lyr_migration_at_213_collapsed_directionswanderungen213linestring.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };

lyr_migration_at_213_collapsed_directionswanderungen213linestring.setVisible(true);
var layersList = [lyr_migration_at_213_collapsed_directionswanderungen213linestring];
var layersMap  = {'lyr_migration_at_213_collapsed_directionswanderungen213linestring':lyr_migration_at_213_collapsed_directionswanderungen213linestring};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [686188.197902, 5645629.469679, 2434447.524053, 6386681.372111];
var unitsConversion = 1;

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
    var toolbarOptions = {title:"My Web App"};
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
