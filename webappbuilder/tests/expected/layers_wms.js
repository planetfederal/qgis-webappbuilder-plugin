var lyr_wms = new ol.layer.Tile({
                        opacity: 1.0,
                        timeInfo: null,
                         
                        source: new ol.source.TileWMS(({
                          url: "http://nsidc.org/cgi-bin/atlas_south?",
                          params: {"LAYERS": "blue_marble_01" , "TILED": "true", "STYLES": ""},
                        })),
                        title: "wms",
                        id: "satellite_imagery__January__2004_20161108090137234",
                        popupInfo: "",
                        projection: "EPSG:4326"
                      });

lyr_wms.setVisible(true);
var layersList = [lyr_wms];
