baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_groupped = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_groupped)}),
                     
                    style: style_groupped,
                    title: "groupped",
                    id: "points20150909090651234",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true
                });
var lyr_groupped2 = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector({features: new ol.format.GeoJSON().readFeatures(geojson_groupped2)}),
                     
                    style: style_groupped2,
                    title: "groupped2",
                    id: "points20150909090705810",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true
                });
var group_group1 = new ol.layer.Group({
                                layers: [lyr_groupped,lyr_groupped2],
                                showContent: true,
                                title: "group1"});

lyr_groupped.setVisible(true);
lyr_groupped2.setVisible(true);
var layersList = [group_group1];
