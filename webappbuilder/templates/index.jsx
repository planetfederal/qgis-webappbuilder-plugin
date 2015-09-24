@IMPORTS@

var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');
closer.onclick = function() {
  container.style.display = 'none';
  closer.blur();
  return false;
};

var overlayPopup = new ol.Overlay({
  element: container
});

var view = new ol.View({
    @VIEW@
});

var pointZoom = @POINTZOOM@;

var map = new ol.Map({
  controls: [
    @CONTROLS@
  ],
  target: document.getElementById('map'),
  renderer: 'canvas',
  overlays: [overlayPopup],
  layers: layersList,
  view: view
});

var originalExtent = @BOUNDS@;
map.getView().fit(originalExtent, map.getSize());

@POSTMAP@

@POPUPLAYERS@

var popupEventTriggered = function(evt) {
    var pixel = map.getEventPixel(evt.originalEvent);
    var coord = evt.coordinate;
    var popupTexts = [];
    var currentFeature;
    var allLayers = getAllNonBaseLayers();
    map.forEachFeatureAtPixel(pixel, function(feature, layer) {
        feature = decluster(feature);
        if (feature) {
            var popupDef = popupLayers[allLayers.indexOf(layer)];
            var res = map.getView().getResolution();
            var visible = layer.getVisible() && layer.getMaxResolution() > res
                                            && layer.getMinResolution() < res;
            if (popupDef && visible) {
                var featureKeys = feature.getKeys();
                for (var i = 0; i < featureKeys.length; i++) {
                    if (featureKeys[i] != 'geometry') {
                        var value = feature.get(featureKeys[i]);
                        if (value) {
                            popupDef = popupDef.split("[" + featureKeys[i] + "]").join(
                                String(feature.get(featureKeys[i])))
                        } else {
                            popupDef = popupDef.split("[" + featureKeys[i] + "]").join("NULL")
                        }
                    }
                }
                popupTexts.push(popupDef);
            }
        }
    });

    var fetchData = function(cb) {
        var len = allLayers.length;
        var finishedQueries = 0;
        var finishedQuery = function(){
            finishedQueries++;
            if (len == finishedQueries) {
                cb();
            }
        };
        var geojsonFormat = new ol.format.GeoJSON();
        for (var i = 0; i < len; i++) {
            var layer = allLayers[i];
            if (layer.getSource() instanceof ol.source.TileWMS) {
                var popupDef = popupLayers[allLayers.indexOf(layer)];
                if (popupDef == "#AllAttributes") {
                    var url = layer.getSource().getGetFeatureInfoUrl(
                        evt.coordinate,
                        map.getView().getResolution(),
                        map.getView().getProjection(), {
                            'INFO_FORMAT': 'text/plain'
                        }
                    );
                    $.ajax({
                        type: 'GET',
                        url: url,
                        success: function(data) {
                            popupTexts.push(data);
                            finishedQuery();
                        },
                        error: function(){
                            popupTexts.push('<iframe seamless src="' + url + '"></iframe>');
                            finishedQuery();
                        }
                    });
                } else if (popupDef !== "") {
                    var url = layer.getSource().getGetFeatureInfoUrl(
                        evt.coordinate,
                        map.getView().getResolution(),
                        map.getView().getProjection(), {
                            'INFO_FORMAT': 'application/json'
                        }
                    );
                    $.ajax({
                        url: url,
                        success: function(data) {
                            var features = geojsonFormat.readFeatures(data);
                            if (features.length)
                                for (var f = 0; f < features.length; f++) {
                                    var popupContent = popupDef;
                                    var feature = features[f];
                                    var values = feature.getProperties();
                                    for (var key in values) {
                                        if (key != 'geometry') {
                                            var value = values[key];
                                            if (value) {
                                                popupContent = popupDef.split("[" + key + "]").join(
                                                    String(value));
                                            } else {
                                                popupContent = popupDef.split("[" + key + "]").join("NULL");
                                            }
                                        }
                                    }
                                    popupTexts.push(popupContent);
                                }
                            else{
                                popupTexts.push("No features at this location");
                            }
                            finishedQuery();
                        },
                        error: function(){
                            popupTexts.push('<iframe seamless src="' + url + '"></iframe>');
                            finishedQuery();
                        }
                    });
                }
                else{
                    finishedQuery();
                }
            } else {
                finishedQuery();
            }
        }
    };

    fetchData(function() {
        if (popupTexts.length) {
            overlayPopup.setPosition(coord);
            content.innerHTML = popupTexts.join("<hr>");
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
            closer.blur();
        }
    });

};

map.on('@POPUPEVENT@', function(evt) {
  popupEventTriggered(evt);
});

@REACT@
