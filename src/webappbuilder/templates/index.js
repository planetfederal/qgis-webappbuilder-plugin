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
  })

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
map.getView().fitExtent(originalExtent, map.getSize());

var selectInteraction = new ol.interaction.Select({
  layers: function(layer){
    return selectableLayersList.indexOf(layer) != -1;
  },
  style: @SELECTIONSTYLE@,
  toggleCondition: ol.events.condition.shiftKeyOnly,
  filter: function(feature, layer){
    features = f.get("features")
    if (features){
        return false;
    }
    else{
        return true
    }
  }
});
map.addInteraction(selectInteraction);

isDuringMultipleSelection = false;

var selectedFeatures = selectInteraction.getFeatures();
selectedFeatures.clear = function(){
    isDuringMultipleSelection = true;
    while (this.getLength() > 1) {
        this.pop();
    }
    isDuringMultipleSelection = false;
    if (this.getLength()){
        this.pop();
    }
}


var currentInteraction;

@CESIUM@

var NO_POPUP = 0
var ALL_ATTRIBUTES = 1

@POPUPLAYERS@

var highlightOverlay = new ol.FeatureOverlay({
  map: map,
  style: [@HIGHLIGHTSTYLE@]
});

var doHighlight = @DOHIGHLIGHT@;
var doHover = @ONHOVER@;

var decluster = function(f){
    features = f.get("features")
    if (features){
        if (features.length > 1){
            return null;
        }
        else{
            return features[0];
        }
    }
    else{
        return f;
    }
}

var highlight;
var onPointerMove = function(evt) {
    if (!doHover && !doHighlight) {
        return;
    }
    var pixel = map.getEventPixel(evt.originalEvent);
    var coord = evt.coordinate;
    var popupField;
    var popupText = '';
    var currentFeature;
    var currentFeatureKeys;
    map.forEachFeatureAtPixel(pixel, function(feature, layer) {
        feature = decluster(feature);
        if (feature){
            currentFeature = feature;
            currentFeatureKeys = currentFeature.getKeys();
            var field = popupLayers[singleLayersList.indexOf(layer)];
            if (field == NO_POPUP) {} else if (field == ALL_ATTRIBUTES) {
                for (var i = 0; i < currentFeatureKeys.length; i++) {
                    if (currentFeatureKeys[i] != 'geometry') {
                        popupField = "<b>" + currentFeatureKeys[i] + '</b>: ' + currentFeature.get(currentFeatureKeys[i]);
                        popupText = popupText + popupField + '<br>';
                    }
                }
            } else {
                var value = feature.get(field);
                if (value) {
                    popupText = "<b>" + field + '</b>: ' + value;
                }
            }
        }
    });

    if (doHighlight) {
        if (currentFeature !== highlight) {
            if (highlight) {
                highlightOverlay.removeFeature(highlight);
            }
            if (currentFeature) {
                highlightOverlay.addFeature(currentFeature);
            }
            highlight = currentFeature;
        }
    }

    if (doHover) {
        if (popupText) {
            overlayPopup.setPosition(coord);
            content.innerHTML = popupText;
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
            closer.blur();
        }
    }
};

var onSingleClick = function(evt) {
    if (doHover) {
        return;
    }
    var pixel = map.getEventPixel(evt.originalEvent);
    var coord = evt.coordinate;
    var popupField;
    var popupText = '';
    var currentFeature;
    var currentFeatureKeys;
    map.forEachFeatureAtPixel(pixel, function(feature, layer) {
        feature = decluster(feature);
        if (feature){
            currentFeature = feature;
            currentFeatureKeys = currentFeature.getKeys();
            var field = popupLayers[singleLayersList.indexOf(layer)];
            if (field == NO_POPUP) {} else if (field == ALL_ATTRIBUTES) {
                for (var i = 0; i < currentFeatureKeys.length; i++) {
                    if (currentFeatureKeys[i] != 'geometry') {
                        popupField = "<b>" + currentFeatureKeys[i] + '</b>: ' + currentFeature.get(currentFeatureKeys[i]);
                        popupText = popupText + popupField + '<br>';
                    }
                }
            } else {
                var value = feature.get(field);
                if (value) {
                    popupText = "<b>" + field + '</b>: ' + value;
                }
            }
        }
    });

    if (popupText) {
        overlayPopup.setPosition(coord);
        content.innerHTML = popupText;
        container.style.display = 'block';
    } else {
        container.style.display = 'none';
        closer.blur();
    }
};


map.on('pointermove', function(evt) {
  onPointerMove(evt);
});
map.on('singleclick', function(evt) {
  onSingleClick(evt);
});
