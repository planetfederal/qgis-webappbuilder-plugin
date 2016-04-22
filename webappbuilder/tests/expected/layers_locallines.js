var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,'type':
                    'base-group', 'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 'title': 'Overlays', layers: overlayLayers});
var lyr_lines = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_lines,
                    selectedStyle: selectionStyle_lines,
                    title: "lines",
                    id: "lines_shp20150708163456077",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: ""
                });
lines_geojson_callback = function(geojson) {
                              lyr_lines.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };

lyr_lines.setVisible(true);
var layersList = [lyr_lines];
