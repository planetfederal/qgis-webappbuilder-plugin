var src_raster = new ol.source.ImageStatic({
                                url: "./data/raster.png",
                                projection: "EPSG:3857",
                                alwaysInRange: true,
                                imageSize: [91, 91],
                                imageExtent: [50093.770857, 50094.285871, 1063101.137076, 1068058.094050]
                          });

                          var raster_raster = new ol.source.Raster({
                                sources: [src_raster],
                                operation: function(pixels, data) {
                                    var pixel = pixels[0];
                                    if (pixel[0] === 0 && pixel[1] === 0 && pixel[2] === 0) {
                                        pixel[3] = 0;
                                    }
                                    return pixel;
                                  }
                          });

                          var lyr_raster = new ol.layer.Image({
                                opacity: 1.0,
                                 
                                title: "raster",
                                id: "raster20150909093752545",
                                timeInfo: null,
                                source: raster_raster
                            });

lyr_raster.setVisible(true);
var layersList = [lyr_raster];
