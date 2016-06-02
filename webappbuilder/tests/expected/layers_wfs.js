var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,'type':
                    'base-group', 'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true, 'title': 'Overlays', layers: overlayLayers});
window.wfsCallback_wfs = function(jsonData) {
                        wfsSource_wfs.addFeatures(new ol.format.GeoJSON().readFeatures(jsonData));
                    };
                    var wfsSource_wfs = new ol.source.Vector({
                        format: new ol.format.GeoJSON(),
                        loader: function(extent, resolution, projection) {
                            var script = document.createElement('script');
                            script.src = 'http://demo.boundlessgeo.com/geoserver/wfs?VERSION=1.0.0?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=osm:placenames_large&outputFormat=text/javascript&format_options=callback:wfsCallback_wfs' +
                                '&srsname=EPSG:3857&bbox=' + extent.join(',') + ',EPSG:3857';
                            document.head.appendChild(script);
                        },
                        strategy: ol.loadingstrategy.tile(new ol.tilegrid.createXYZ({maxZoom: 19}))
                    });
                    var lyr_wfs = new ol.layer.Vector({
                            opacity: 1.0,
                            source: wfsSource_wfs,  
                            style: style_wfs,
                            selectedStyle: selectionStyle_wfs,
                            title: "wfs",
                            id: "osm_placenames_large20160602142332803",
                            wfsInfo: {featureNS: '',
                    typeName: 'osm:placenames_large',
                    geometryType: 'Point',
                    geometryName: 'the_geom',
                    url: 'http://demo.boundlessgeo.com/geoserver/wfs?VERSION=1.0.0'
                  },
                  isWFST:true,
                            filters: [],
                            timeInfo: null,
                            isSelectable: true,
                            popupInfo: ""
                        });

lyr_wfs.setVisible(true);
var layersList = [lyr_wfs];
