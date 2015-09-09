baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
geojsonFormat_wfs = new ol.format.GeoJSON();
                    var wfsSource_wfs = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        loader: function(extent, resolution, projection) {
                            var url = 'http://demo.boundlessgeo.com/geoserver/wfs?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=osm:placenames_large&outputFormat=text/javascript&format_options=callback:loadFeatures_wfs' +
                                '&srsname=EPSG:3857&bbox=' + extent.join(',') + ',EPSG:3857';
                            $.ajax({
                                url: url,
                                dataType: 'jsonp'
                            });
                        },
                        strategy: ol.loadingstrategy.tile(new ol.tilegrid.createXYZ({maxZoom: 19})),
                    });
                    var loadFeatures_wfs = function(response) {
                        wfsSource_wfs.addFeatures(
                                geojsonFormat_wfs.readFeatures(response,
                                    {dataProjection: 'EPSG:3857', featureProjection: 'EPSG:3857'}));
                    };

                    var lyr_wfs = new ol.layer.Vector({
                            opacity: 1.0,
                            source: wfsSource_wfs,  
                            style: style_wfs,
                            title: "wfs",
                            id: "Countries_and_States20150909091003951",
                            filters: [],
                            timeInfo: null,
                            isSelectable: true
                        });

lyr_wfs.setVisible(true);
var layersList = [lyr_wfs];
