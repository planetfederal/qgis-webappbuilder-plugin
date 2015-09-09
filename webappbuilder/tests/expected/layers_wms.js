baseLayers = [];var baseLayersGroup = new ol.layer.Group({'type': 'base', 'title': 'Base maps', layers: baseLayers});
var lyr_wms = new ol.layer.Tile({
                        opacity: 1.0,
                        timeInfo: null,
                         
                        source: new ol.source.TileWMS(({
                          url: "http://demo.boundlessgeo.com/geoserver/wms",
                          params: {"LAYERS": "osm:osm", "TILED": "true", "STYLES": ""},
                        })),
                        title: "wms",
                        id: "osm_osm20150909090852137"
                      });

lyr_wms.setVisible(true);
var layersList = [lyr_wms];
