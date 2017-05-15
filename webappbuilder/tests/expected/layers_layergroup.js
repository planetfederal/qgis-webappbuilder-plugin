var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group', 
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var lyr_groupped = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_groupped,
                    selectedStyle: selectionStyle_groupped,
                    title: "groupped",
                    id: "points20150909090651234",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Point"
                });
groupped_geojson_callback = function(geojson) {
                              lyr_groupped.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };
var lyr_groupped2 = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_groupped2,
                    selectedStyle: selectionStyle_groupped2,
                    title: "groupped2",
                    id: "points20150909090705810",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Point"
                });
groupped2_geojson_callback = function(geojson) {
                              lyr_groupped2.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                        };
var group_group1 = new ol.layer.Group({
                                layers: [lyr_groupped,lyr_groupped2],
                                showContent: true,
                                isGroupExpanded: true,
                                title: "group1"});

lyr_groupped.setVisible(true);
lyr_groupped2.setVisible(true);
var layersList = [group_group1];