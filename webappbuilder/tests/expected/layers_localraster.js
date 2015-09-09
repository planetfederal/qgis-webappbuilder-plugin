baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_raster = new ol.layer.Image({
                                opacity: 1.0,
                                 
                                title: "raster",
                                id: "raster20150909093752545",
                                timeInfo: null,
                                source: new ol.source.ImageStatic({
                                   url: "./layers/raster.jpg",
                                    projection: "EPSG:3857",
                                    alwaysInRange: true,
                                    imageSize: [91, 91],
                                    imageExtent: [50093.770857, 50094.285871, 1063101.137076, 1068058.094050]
                                })
                            });

lyr_raster.setVisible(true);
var layersList = [lyr_raster];
