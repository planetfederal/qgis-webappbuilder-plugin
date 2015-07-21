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

var currentInteraction;

@CESIUM@

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
            popupDef = popupLayers[allLayers.indexOf(layer)];
            if (popupDef) {
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

    var len = allLayers.length;
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
                $.get(url, {}, function(data) {
                        popupTexts.push(data);
                    });
            } else if (popupDef !== "") {
                var url = layer.getSource().getGetFeatureInfoUrl(
                    evt.coordinate,
                    map.getView().getResolution(),
                    map.getView().getProjection(), {
                        'INFO_FORMAT': 'application/json'
                    }
                );
                $.get(url, {}, function(data) {
                    for (var f = 0; f < data.features.length; f++) {
                        var feature = data.features[f];
                        for (var property in feature) {
                            if (feature.hasOwnProperty(property)) {
                                if (property != 'geometry') {
                                    var value = feature[property];
                                    if (value) {
                                        popupDef = popupDef.split("[" + property + "]").join(
                                            String(value));
                                    } else {
                                        popupDef = popupDef.split("[" + property + "]").join("NULL");
                                    }
                                }
                            }
                        }
                    }
                    popupTexts.push(popupDef);
                });
            }
        }
    }
    if (popupTexts.length) {
        overlayPopup.setPosition(coord);
        content.innerHTML = popupTexts.join("<hr>");
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
        closer.blur();
    }
};

map.on('@POPUPEVENT@', function(evt) {
  popupEventTriggered(evt);
});

