baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_polygons = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_polygons)}),
                     
                    style: style_polygons,
                    title: "polygons",
                    id: "graticule20150708141425208",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true
                });

lyr_polygons.setVisible(true);
var layersList = [lyr_polygons];
