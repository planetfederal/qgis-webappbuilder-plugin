


                    var textStyleCache_bakeries={}
                    var clusterStyleCache_bakeries={}
                    var style_bakeries = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_bakeries'
        };

                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(6), radius2: pixelsFromMm(pixelsFromMm(6)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(227,123,48,1.0)"}), angle: 0})
                        })
                        ];
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_bakeries = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_bakeries'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(6), radius2: pixelsFromMm(pixelsFromMm(6)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
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
                    popupInfo: "",
                    attributes: ["Y", "X", "Name", "Address", "Telephone", "Website", "Text"],
                    geometryType: "Point"
                });
bakeries_geojson_callback = function(geojson) {
                              lyr_bakeries.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };

lyr_bakeries.setVisible(true);
var layersList = [lyr_bakeries];
var layersMap  = {'lyr_bakeries':lyr_bakeries};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [255029.386545, 6248698.214055, 267586.457022, 6255570.182765];

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});

function pixelsFromMapUnits(size) {
    return size / map.getView().getResolution();
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
      React.createElement(AppBar, toolbarOptions ,
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