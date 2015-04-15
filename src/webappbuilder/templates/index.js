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
map.getView().fitExtent(@BOUNDS@, map.getSize());

var selectInteraction = new ol.interaction.Select({
  layers: function(layer){
    return selectableLayersList.indexOf(layer) != -1;
  },
  style: @SELECTIONSTYLE@,
  addCondition: ol.events.condition.platformModifierKeyOnly,
  removeCondition: ol.events.condition.platformModifierKeyOnly
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

var dragBoxInteraction = new ol.interaction.DragBox({
    condition: ol.events.condition.shiftKeyOnly,
    style: new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: [0, 0, 255, 1]
        })
    })
});
map.addInteraction(dragBoxInteraction);

dragBoxInteraction.on('boxend', function(e) {
    var toAdd = [];
    var extent = dragBoxInteraction.getGeometry().getExtent();
    var selectedFeatures = selectInteraction.getFeatures();
    for (i = 0; i < selectableLayersList.length; i++) {
        source = selectableLayersList[i].getSource()
        source.forEachFeatureIntersectingExtent(extent, function(feature) {
            toAdd.push(feature);
        });
    }
    if (toAdd.length !== 0){
        isDuringMultipleSelection = true;
        selectedFeatures.extend(toAdd.slice(0, -1));
        isDuringMultipleSelection = false;
        selectedFeatures.push(toAdd[toAdd.length - 1]);
    }

});

dragBoxInteraction.on('boxstart', function(e) {
    var selectedFeatures = selectInteraction.getFeatures();
    isDuringMultipleSelection = true;
    selectedFeatures.clear();
    isDuringMultipleSelection = false;
});


@CESIUM@

var NO_POPUP = 0
var ALL_FIELDS = 1

@POPUPLAYERS@

var highlightOverlay = new ol.FeatureOverlay({
  map: map,
  style: [@HIGHLIGHTSTYLE@]
});


var doHighlight = @DOHIGHLIGHT@;
var doHover = @ONHOVER@;

var highlight;
var onPointerMove = function(evt) {
  if (!doHover && !doHighlight){
    return;
  }
  var pixel = map.getEventPixel(evt.originalEvent);
  var coord = evt.coordinate;
  var popupField;
  var popupText = '';
  var currentFeature;
  var currentFeatureKeys;
  map.forEachFeatureAtPixel(pixel, function(feature, layer) {
    currentFeature = feature;
    currentFeatureKeys = currentFeature.getKeys();
    var field = popupLayers[singleLayersList.indexOf(layer)];
    if (field == NO_POPUP){
    }
    else if (field == ALL_FIELDS){
      for ( var i=0; i<currentFeatureKeys.length;i++) {
          if (currentFeatureKeys[i] != 'geometry') {
              popupField = currentFeatureKeys[i] + ': '+ currentFeature.get(currentFeatureKeys[i]);
              popupText = popupText + popupField+'<br>';
          }
      }
    }
    else{
      var value = feature.get(field);
      if (value){
        popupText = field + ': ' + value;
      }
    }
  });

  if (doHighlight){
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

  if (doHover){
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
  if (doHover){
    return;
  }
  var pixel = map.getEventPixel(evt.originalEvent);
  var coord = evt.coordinate;
  var popupField;
  var popupText = '';
  var currentFeature;
  var currentFeatureKeys;
  map.forEachFeatureAtPixel(pixel, function(feature, layer) {
    currentFeature = feature;
    currentFeatureKeys = currentFeature.getKeys();
    var field = popupLayers[singleLayersList.indexOf(layer)];
    if (field == NO_POPUP){
    }
    else if (field == ALL_FIELDS){
      for ( var i=0; i<currentFeatureKeys.length;i++) {
          if (currentFeatureKeys[i] != 'geometry') {
              popupField = currentFeatureKeys[i] + ': '+ currentFeature.get(currentFeatureKeys[i]);
              popupText = popupText + popupField+'<br>';
          }
      }
    }
    else{
      var value = feature.get(field);
      if (value){
        popupText = field + ': '+ value;
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
