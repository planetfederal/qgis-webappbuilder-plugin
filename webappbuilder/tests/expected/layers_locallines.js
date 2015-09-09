baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_lines = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_lines)}),
                     
                    style: style_lines,
                    title: "lines",
                    id: "lines_shp20150708163456077",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true
                });

lyr_lines.setVisible(true);
var layersList = [lyr_lines];
