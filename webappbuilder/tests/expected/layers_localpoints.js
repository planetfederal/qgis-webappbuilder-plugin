var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,'type':
                    'base-group', 'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 'title': 'Overlays', layers: overlayLayers});
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
                    popupInfo: ""
                });
points_geojson_callback = function(geojson) {
                              lyr_points.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };

lyr_points.setVisible(true);
var layersList = [lyr_points];
