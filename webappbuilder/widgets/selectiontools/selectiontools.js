var selectByRectangle = function(){

    removeInteractions();

    var dragBoxInteraction = new ol.interaction.DragBox({
        condition: ol.events.condition.noModifierKeys,
        style: new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: [0, 0, 255, 1]
            })
        })
    });

    dragBoxInteraction.on('boxend', function(e) {
        var extent = dragBoxInteraction.getGeometry().getExtent();
        for (var i = 0; i < getSelectableLayers().length; i++) {
            var toAdd = [];
            var layer = getSelectableLayers()[i]
            var source = sourceFromLayer(layer);
            source.forEachFeatureIntersectingExtent(extent, function(feature) {
                toAdd.push(feature);
            });
            selectionManager.setSelection(toAdd, layer);
        }

    });

    dragBoxInteraction.on('boxstart', function(e) {
    });

    map.addInteraction(dragBoxInteraction);
    currentInteractions = [dragBoxInteraction];

};

var selectByPolygonSource = new ol.source.Vector();

var selectByPolygon = function(){

    removeInteractions();

    var polygon;

    var addInteraction = function(){
      var selectByPolygonInteraction = new ol.interaction.Draw({
        source: selectByPolygonSource,
        type: 'Polygon',
        style: new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(255, 255, 255, 0.2)'
          }),
          stroke: new ol.style.Stroke({
            color: 'rgba(0, 0, 0, 0.5)',
            lineDash: [10, 10],
            width: 2
          }),
          image: new ol.style.Circle({
            radius: 5,
            stroke: new ol.style.Stroke({
              color: 'rgba(0, 0, 0, 0.7)'
            }),
            fill: new ol.style.Fill({
              color: 'rgba(255, 255, 255, 0.2)'
            })
          })
        })
      });

      selectByPolygonInteraction.on('drawstart',
          function(evt) {
            polygon = evt.feature;
          }, this);

      selectByPolygonInteraction.on('drawend',
          function(evt) {
            doSelection();
            polygon = null;
          }, this);


      map.addInteraction(selectByPolygonInteraction);
      currentInteractions = [selectByPolygonInteraction];

    };


    var doSelection = function() {
        //Only correct for points and this might not be the most efficient way...
        if (polygon){
            var geom = polygon.getGeometry();
            var polygExtent = geom.getExtent();
            for (var i = 0; i < getSelectableLayers().length; i++) {
                var toAdd = [];
                var layer = getSelectableLayers()[i]
                var source = sourceFromLayer(layer);
                source.forEachFeatureIntersectingExtent(polygExtent, function(feature) {
                    var extent = feature.getGeometry().getExtent();
                    if (geom.intersectsExtent(extent)){
                        toAdd.push(feature);
                    }
                });
                selectionManager.setSelection(toAdd, layer);
            }
        }

    };

    addInteraction();
};
