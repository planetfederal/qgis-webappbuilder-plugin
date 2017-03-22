var lyr_wms = new ol.layer.Tile({
                        opacity: 1.0,
                        timeInfo: null,

                        source: new ol.source.TileWMS(({
                          crossOrigin:'anonymous',
                          url: "http://demo.mapserver.org/cgi-bin/wms?",
                          params: {"LAYERS": "continents" , "TILED": "true", "STYLES": ""},
                        })),
                        title: "wms",
                        id: "World_continents20161110111935176",
                        popupInfo: "",
                        projection: "EPSG:4326"
                      });

lyr_wms.setVisible(true);
var layersList = [lyr_wms];