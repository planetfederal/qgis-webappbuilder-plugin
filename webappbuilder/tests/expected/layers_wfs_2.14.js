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
                            script.src = '?service=WFS&version=1.1.0&request=GetFeature' +
                                '&typename=&outputFormat=text/javascript&format_options=callback:wfsCallback_wfs' +
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
                            id: "ne_ne_10m_populated_places20160615104639878",
                            wfsInfo: {featureNS: '',
                    typeName: '',
                    geometryType: 'Point',
                    geometryName: 'the_geom',
                    url: ''
                  },
                  isWFST:false,
                            filters: [],
                            timeInfo: null,
                            isSelectable: true,
                            popupInfo: ""
                        });

lyr_wfs.setVisible(true);
var layersList = [lyr_wfs];
