baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_points = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_points)}),
                     
                    style: style_points,
                    title: "points",
                    id: "points_shp20150708141950508",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true
                });

lyr_points.setVisible(true);
var layersList = [lyr_points];
