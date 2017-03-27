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


                    var textStyleCache_bakeries={}
                    var clusterStyleCache_bakeries={}
                    var style_bakeries = function(feature, resolution){

                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: 11.4, radius2: 5.7, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(227,123,48,1.0)"}), angle: 0})
                        })
                        ];
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_bakeries = function(feature, resolution){

                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: 11.4, radius2: 5.7, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ]
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,'type':
                    'base-group', 'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 'title': 'Overlays', layers: overlayLayers});
var lyr_bakeries = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),

                    style: style_bakeries,
                    selectedStyle: selectionStyle_bakeries,
                    title: "bakeries",
                    id: "bakeries20150709073321023",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: ""
                });
bakeries_geojson_callback = function(geojson) {
                              lyr_bakeries.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };

lyr_bakeries.setVisible(true);
var layersList = [lyr_bakeries];
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [256354.556143, 6247253.046488, 266261.287425, 6257016.770510];

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
    if (el.style.display === 'block' || el.style.display === '') {
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
    var toolbarOptions = {style: {height: 71}, showMenuIconButton: false, title:"My Web App"};
    return React.createElement("div", {id: 'content'},
      React.createElement(AppBar, toolbarOptions,
       React.createElement(Select, {toggleGroup: 'navigation', map:map}),
React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})
      ),
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
