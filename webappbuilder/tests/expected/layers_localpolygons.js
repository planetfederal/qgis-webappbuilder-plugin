var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,'type':
                    'base-group', 'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 'title': 'Overlays', layers: overlayLayers});
var lyr_polygons = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),

                    style: style_polygons,
                    selectedStyle: selectionStyle_polygons,
                    title: "polygons",
                    id: "graticule20150708141425208",
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

lyr_polygons.setVisible(true);
var layersList = [lyr_polygons];
