var measureSource = new ol.source.Vector();
var measureVector = new ol.layer.Vector({
  source: measureSource,
  style: new ol.style.Style({
    fill: new ol.style.Fill({
      color: 'rgba(255, 255, 255, 0.2)'
    }),
    stroke: new ol.style.Stroke({
      color: '#ffcc33',
      width: 2
    }),
    image: new ol.style.Circle({
      radius: 7,
      fill: new ol.style.Fill({
        color: '#ffcc33'
      })
    })
  })
});
var measureTooltips=[];

measureTool = function(measureType){

    if (currentInteraction){
        map.removeInteraction(currentInteraction);
    }

    if (measureType === null){
        for (var i=0; i<measureTooltips.length; i++){
            map.removeOverlay(measureTooltips[i]);
        }
        measureSource.clear();
        return;
    }

    var sketch;
    var measureTooltipElement;
    var measureTooltip;

    var pointerMoveHandler = function(evt) {
      if (evt.dragging) {
        return;
      }
      var tooltipCoord = evt.coordinate;
      if (sketch) {
        var output;
        var geom = (sketch.getGeometry());
        if (geom instanceof ol.geom.Polygon) {
          output = formatArea(/** @type {ol.geom.Polygon} */ (geom));
          tooltipCoord = geom.getInteriorPoint().getCoordinates();
        } else if (geom instanceof ol.geom.LineString) {
          output = formatLength( /** @type {ol.geom.LineString} */ (geom));
          tooltipCoord = geom.getLastCoordinate();
        }
        measureTooltipElement.innerHTML = output;
        measureTooltip.setPosition(tooltipCoord);
      }
    };

    map.on('pointermove', pointerMoveHandler);
    map.removeLayer(measureVector);
    map.addLayer(measureVector);

    var addInteraction = function(){
      var type = (measureType == 'area' ? 'Polygon' : 'LineString');
      var measureInteraction = new ol.interaction.Draw({
        source: measureSource,
        type: /** @type {ol.geom.GeometryType} */ (type),
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

      measureInteraction.on('drawstart',
          function(evt) {
            sketch = evt.feature;
          }, this);

      measureInteraction.on('drawend',
          function(evt) {
            measureTooltipElement.className = 'tooltip tooltip-static';
            measureTooltip.setOffset([0, -7]);
            sketch = null;
            measureTooltipElement = null;
            createMeasureTooltip();
          }, this);


      map.addInteraction(measureInteraction);
      currentInteraction = measureInteraction;
      createMeasureTooltip();

    };


    var createMeasureTooltip = function() {
      if (measureTooltipElement) {
        measureTooltipElement.parentNode.removeChild(measureTooltipElement);
      }
      measureTooltipElement = document.createElement('div');
      measureTooltipElement.className = 'tooltip tooltip-measure';
      measureTooltip = new ol.Overlay({
        element: measureTooltipElement,
        offset: [0, -15],
        positioning: 'bottom-center'
      });
      measureTooltips.push(measureTooltip);
      map.addOverlay(measureTooltip);
    };

    var formatLength = function(line) {
      var length = Math.round(line.getLength() * 100) / 100;
      var output;
      if (length > 100) {
        output = (Math.round(length / 1000 * 100) / 100) +
            ' ' + 'km';
      } else {
        output = (Math.round(length * 100) / 100) +
            ' ' + 'm';
      }
      return output;
    };

    var formatArea = function(polygon) {
      var area = polygon.getArea();
      var output;
      if (area > 10000) {
        output = (Math.round(area / 1000000 * 100) / 100) +
            ' ' + 'km<sup>2</sup>';
      } else {
        output = (Math.round(area * 100) / 100) +
            ' ' + 'm<sup>2</sup>';
      }
      return output;
    };

    addInteraction();
};
