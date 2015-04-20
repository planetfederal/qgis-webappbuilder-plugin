sourceFromLayer = function(layer){
    var source = layer.getSource();
    if (source instanceof ol.source.Cluster){
        return source.getSource();
    }
    else{
        return source;
    }

};

//=======================================================

saveAsPng = function(){
    map.once('postcompose', function(event) {
      var canvas = event.context.canvas;
      button = document.getElementById('export-as-image');
      button.href = canvas.toDataURL('image/png');
    });
    map.renderSync();
};

//=======================================================

showAttributesTable = function() {

    panels = document.getElementsByClassName('table-panel');
    if (panels.length != 0){
        this.panel.style.display = 'block';
        return;
    }
    var selectedFeatures = selectInteraction.getFeatures().getArray();
    this.selectedRowIndices = [];

    var this_ = this;
    this.toggleRowSelection = function(){
        if (isDuringMultipleSelection){
            return;
        }
        if (this_.panel.style.display === 'none'){
            return;
        }
        this_.selectedRowIndices = [];
        var rows = this_.table.getElementsByTagName("tr");
        var layerFeatures = sourceFromLayer(this_.currentLayer).getFeatures();
        for (i = 0; i < layerFeatures.length; i++) {
            var row = rows[i];
            var idx = selectedFeatures.indexOf(layerFeatures[i]);
            if (idx !== -1){
                row.className = "row-selected";
                this_.selectedRowIndices.push(i);
            }
            else{
                row.className = "row-unselected";
                if (this_.onlySelectedCheck.checked){
                    row.style.display = 'none';
                }
                else{
                    row.style.display = 'table-row';
                }
            }
        }
    };
    selectInteraction.getFeatures().on('change:length', function(evt){this.toggleRowSelection()}, this);

    this.renderPanel = function() {
        this.formContainer = document.createElement("form");
        this.formContainer.className = "form-inline";
        this.panel.appendChild(this.formContainer);
        this.createSelector(map);
        this.createButtons();
        var p = document.createElement('p');
        this.panel.appendChild(p);
        this.currentLayer = map.getLayers().getArray().slice().reverse()[0];
        this.tablePanel = document.createElement('div');
        this.tablePanel.className = 'table-panel';
        this.panel.appendChild(this.tablePanel);
        this.renderTable();
    };

    this.createButtons = function() {
        this_ = this;
        zoomTo = document.createElement("button");
        zoomTo.setAttribute("type", "button");
        zoomTo.innerHTML = '<i class="glyphicon glyphicon-search"></i> Zoom to selected';
        zoomTo.className = "btn btn-default";
        zoomTo.onclick = function(){
            features = sourceFromLayer(this_.currentLayer).getFeatures();
            extent = ol.extent.createEmpty();
            for (i = 0; i < this_.selectedRowIndices.length; i++){
                extent = ol.extent.extend(extent,
                    features[this_.selectedRowIndices[i]].getGeometry().getExtent());
            }
            map.getView().fitExtent(extent, map.getSize());
        };
        this.formContainer.appendChild(zoomTo);
        clear =  document.createElement("button");
        clear.setAttribute("type", "button");
        clear.innerHTML = '<i class="glyphicon glyphicon-trash"></i> Clear selected';
        clear.className = "btn btn-default";
        clear.onclick = function(){
            var rows = this_.table.getElementsByTagName("tr");
            var sel = this_.selectedRowIndices.slice();
            for (var i = 0; i < sel.length; i++) {
                feature = sourceFromLayer(this_.currentLayer).getFeatures()[sel[i]];
                selectInteraction.getFeatures().remove(feature);
            }
        };
        this.formContainer.appendChild(clear);

        onlySelected = document.createElement("label");
        this.onlySelectedCheck = document.createElement("input");
        this.onlySelectedCheck.setAttribute("type", "checkbox");
        this.onlySelectedCheck.setAttribute("value", "");
        onlySelectedCheck.onclick = this.toggleRowSelection;
        onlySelected.appendChild(this.onlySelectedCheck);
        onlySelected.appendChild(document.createTextNode(" Show only selected features"));
        this.formContainer.appendChild(onlySelected);
    }


    this.renderTable = function() {
        try{
            this.tablePanel.removeChild(this.table);
        }
        catch(err){}

        this.table = document.createElement("TABLE");
        this.table.border = "1";

        cols = sourceFromLayer(this.currentLayer).getFeatures()[0].getKeys();
        var row = this.table.insertRow(-1);

        for (var i = 0; i < cols.length; i++) {
            if (cols[i] != 'geometry') {
                var headerCell = document.createElement("TH");
                headerCell.innerHTML = cols[i];
                row.appendChild(headerCell);
            }
        }

        this_ = this;
        this.selectedRowIndices = [];
        layerFeatures = sourceFromLayer(this.currentLayer).getFeatures();
        for (i = 0; i < layerFeatures.length; i++) {
            feature = layerFeatures[i];
            keys = feature.getKeys();
            row = this_.table.insertRow(-1);
            if (selectedFeatures.indexOf(feature) != -1){
                row.className = "row-selected";
                this.selectedRowIndices.push(i);
            }
            else{
                row.className = "row-unselected";
                if (this_.onlySelectedCheck.checked){
                    row.style.display = 'none';
                }
                else{
                    row.style.display = 'table-row';
                }
            }
            for (var j = 0; j < keys.length; j++) {
                if (keys[j] != 'geometry') {
                    var cell = row.insertCell(-1);
                    cell.innerHTML = feature.get(keys[j]);
                }
            }
        }

        if (selectableLayersList.indexOf(this.currentLayer) != -1){
            var rows = this.table.getElementsByTagName("tr");
            for (i = 0; i < rows.length; i++) {
                (function (idx) {
                    rows[idx].addEventListener("click",
                        function () {
                            feature = layerFeatures[idx];
                            if (this.className != "row-selected"){
                                selectInteraction.getFeatures().push(feature);
                            }
                            else{
                                selectInteraction.getFeatures().remove(feature);
                            }
                        }, false);
                })(i);
            }
        }
        this.tablePanel.appendChild(this.table);
    };

    this.createSelector = function(map) {
        label = document.createElement("label");
        label.innerHTML = "Layer:";
        this.formContainer.appendChild(label);
        this.sel = document.createElement('select');
        this.sel.className = "form-control";
        this_ = this;
        this.sel.onchange = function(){
            var lyr = null;
            var lyrs = map.getLayers().getArray().slice().reverse();
            for (i = 0; i < lyrs.length; i++){
                if (lyrs[i].get('title') == this.value){
                    this_.currentLayer = lyrs[i];
                    break;
                }
            }
            this_.renderTable();
        };
        var lyrs = map.getLayers().getArray().slice().reverse();
        for (var i = 0, l; i < lyrs.length; i++) {
            l = lyrs[i];
            if (l.get('title') && l instanceof ol.layer.Vector) {
                var option = document.createElement('option');
                option.value = option.textContent = l.get('title');
                this.sel.appendChild(option);
            }
        }
        this.formContainer.appendChild(this.sel);
    };

    this.panel = document.getElementsByClassName('attributes-table')[0];
    this.renderPanel();
    this.panel.style.display = 'block';

    var closer = document.getElementById('attributes-table-closer');
    closer.onclick = function() {
        this_.panel.style.display = 'none';
        closer.blur();
        return false;
    };

};

//===================


searchAddress = function(){
    var inp = document.getElementById("geocoding-search");
    if (inp.value === ""){
        document.getElementById('geocoding-results').style.display = 'none';
        return;
    }
    $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=5&q=' + inp.value, function(data) {
        var items = [];

        $.each(data, function(key, val) {
            bb = val.boundingbox;
            items.push("<li><a href='#' onclick='goToAddress(" + bb[0] + ", " + bb[2] + ", " + bb[1] + ", " + bb[3]
                        + ", \"" + val.osm_type + "\");return false;'>" + val.display_name + '</a></li>');
        });

        $('#geocoding-results').empty();
        if (items.length !== 0) {
            $('<ul/>', {
                html: items.join('')
            }).appendTo('#geocoding-results');
        } else {
            $('<p>', { html: "No results found" }).appendTo('#geocoding-results');
        }
        document.getElementById('geocoding-results').style.display = 'block';
    });
};

goToAddress = function(lat1, lng1, lat2, lng2, osm_type) {
    document.getElementById('geocoding-results').style.display = 'none';
    map.getView().setCenter(ol.proj.transform([lng1, lat1], 'EPSG:4326', 'EPSG:3857'));
    map.getView().setZoom(10);
};

searchBoxKeyPressed = function(){
    e = e || window.event;
    if (e.keyCode == 13){
        searchAddress();
    }
}


//===========================================

goToBookmarkByName = function(name){
    for(var i=0; i<bookmarks.length; i++){
        if (bookmarks[i][0] === name){
            map.getView().fitExtent(bookmarks[i][1], map.getSize());
        }
    }
};

panToBookmark = function(i){
    var pan = ol.animation.pan({
        duration: 500,
        source: view.getCenter()
    });
    var zoom = ol.animation.zoom({
        duration: 500,
        resolution: view.getResolution(),
        source: view.getZoom()
    });
    map.beforeRender(pan,zoom);
    map.getView().fitExtent(bookmarks[i][1], map.getSize());
};

goToBookmark = function(i){
    map.getView().fitExtent(bookmarks[i][1], map.getSize());
};

flyToBookmark = function(i){
    map.getView().fitExtent(bookmarks[i][1], map.getSize());
};

//===========================================
var measureInteraction;
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

    if (measureInteraction){
        map.removeInteraction(measureInteraction);
    }

    if (measureType === null){
        map.on('pointermove', onPointerMove);
        map.removeLayer(measureVector);
        for (i=0; i<measureTooltips.length; i++){
            map.removeOverlay(measureTooltips[i]);
        }
        measureSource.clear();
        map.addInteraction(selectInteraction);
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
      measureInteraction = new ol.interaction.Draw({
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
      map.removeInteraction(selectInteraction);
      map.addInteraction(measureInteraction);
      createMeasureTooltip();

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

//==============================================

openChart = function(c){

    chartPanel = document.getElementById('chart-panel');
    chartPanel.style.display = 'block';

    this.drawFromSelection = function(){
        if (isDuringMultipleSelection){
            return;
        }
        if (chartPanel.style.display === 'none'){
            return;
        }

        var layerName = charts[c].layer;
        var categoryField = charts[c].categoryField;
        var valueFields = charts[c].valueFields;
        var selectedFeatures = selectInteraction.getFeatures().getArray();
        var lyrs = map.getLayers().getArray();
        var lyr = null;
        for (i = 0; i < lyrs.length; i++){
            if (lyrs[i].get('title') == layerName){
                lyr = lyrs[i];
                break;
            }
        }
        layerFeatures = sourceFromLayer(lyr).getFeatures();
        var columns = [["x"]];
        if (charts[c].displayMode === DISPLAY_MODE_COUNT){
            columns.push(["Feature count"]);
        }
        else{
            for (i = 0; i < valueFields.length; i++) {
                columns.push([valueFields[i]]);
            }
        }
        var selectedCount = 0;
        if (charts[c].displayMode === DISPLAY_MODE_FEATURE){
            for (i = 0; i < selectedFeatures.length; i++) {
                if (layerFeatures.indexOf(selectedFeatures[i]) !== -1){
                    selectedCount++;
                    columns[0].push(selectedFeatures[i].get(categoryField));
                    for (j = 0; j < valueFields.length; j++) {
                        columns[j+1].push(selectedFeatures[i].get(valueFields[j]));
                    }
                }
            }
        }
        else if (charts[c].displayMode === DISPLAY_MODE_CATEGORY){
            values = {};
            for (i = 0; i < selectedFeatures.length; i++) {
                if (layerFeatures.indexOf(selectedFeatures[i]) !== -1){
                    cat = selectedFeatures[i].get(categoryField).toString();
                    if (!(cat in values)){
                        values[cat] = [];
                        for (j = 0; j < valueFields.length; j++) {
                            values[cat].push([selectedFeatures[i].get(valueFields[j])]);
                        }
                    }
                    else{
                        for (j = 0; j < valueFields.length; j++) {
                            values[cat][j].push(selectedFeatures[i].get(valueFields[j]));
                        }
                    }
                }
            }
            for (var key in values){
                columns[0].push(key);
                aggregated = [];
                for (i = 0; i < valueFields.length; i++) {
                    if (charts[c].operation === AGGREGATION_SUM || charts[c].operation === AGGREGATION_AVG){
                        v = 0;
                        for (var j = 0; j < values[key][i].length; j++){
                            v += values[key][i][j];
                        }
                        if (charts[c].operation === AGGREGATION_AVG){
                            v /= values[key][i].length;
                        }
                    }
                    else if (charts[c].operation === AGGREGATION_MIN){
                        Math.min.apply(Math, values[key][i]);
                    }
                    else if (charts[c].operation === AGGREGATION_MAX){
                        Math.max.apply(Math, values[key][i]);
                    }
                    columns[i + 1].push(v);
                }
            }
        }
        else if (charts[c].displayMode === DISPLAY_MODE_COUNT){
            values = {};
            for (i = 0; i < selectedFeatures.length; i++) {
                if (layerFeatures.indexOf(selectedFeatures[i]) !== -1){
                    selectedCount++;
                    cat = selectedFeatures[i].get(categoryField).toString();
                    if (!(cat in values)){
                        values[cat] = 1;
                    }
                    else{
                        values[cat]++;
                    }
                }
            }
            for (var key in values){
                columns[0].push(key);
                columns[1].push(values[key]);
            }
        }
        var info = document.getElementById('chart-panel-info');
        info.innerHTML = selectedCount.toString() + " features selected in layer " + layerName;

        var chart = c3.generate({
            bindto: '#chart',
            data: {
                x: 'x',
                columns: columns,
                type: 'bar'
            },
            axis: {
                x: {
                    type: 'category',
                    tick: {
                        rotate: 70,
                        multiline:false
                    },
                    height: 80
                }
            }
        });
    };

    this.drawFromSelection();

    selectInteraction.getFeatures().on('change:length', this.drawFromSelection, this);

    var this_ = this;
    var closer = document.getElementById('chart-panel-closer');
    closer.onclick = function() {
        chartPanel.style.display = 'none';
        closer.blur();
        return false;
    };
};

//===========================================

showQueryPanel = function(){

    var select = document.getElementById('query-layer');
    if (select.options.length === 0){
        var lyrs = map.getLayers().getArray().slice().reverse();
        for (var i = 0, l; i < lyrs.length; i++) {
            l = lyrs[i];
            if (l.get('title') && l instanceof ol.layer.Vector) {
                var option = document.createElement('option');
                option.value = option.textContent = l.get('title');
                select.appendChild(option);
            }
        }
    }

    var close = document.getElementById('btn-close-query');
    close.onclick = function() {
        document.getElementById('query-panel').style.display = 'none';
        return false;
    };

    var NEW_SELECTION = 0;
    var ADD_TO_SELECTION = 1;
    var IN_SELECTION = 2;

    this_ = this;
    var queryNew = document.getElementById('btn-query-new');
    queryNew.onclick = function(){
        this_.selectFromQuery(NEW_SELECTION);
    };
    var queryAdd = document.getElementById('btn-query-add');
    queryAdd.onclick = function(){
        this_.selectFromQuery(ADD_TO_SELECTION);
    };
    var queryIn = document.getElementById('btn-query-in');
    queryIn.onclick = function(){
        this_.selectFromQuery(IN_SELECTION);
    };
    this.selectFromQuery = function(mode) {
        if (this_.queryFilter){
            var layer = null;
            var layerName = document.getElementById('query-layer').value;
            var lyrs = map.getLayers().getArray().slice().reverse();
            for (i = 0; i < lyrs.length; i++){
                if (lyrs[i].get('title') === layerName){
                    layer = lyrs[i];
                    break;
                }
            }
            var layerFeatures = sourceFromLayer(layer).getFeatures();
            var selectedFeatures = selectInteraction.getFeatures();
            var selectedFeaturesArray = selectedFeatures.getArray();
            if (mode === NEW_SELECTION){
                var toRemove = [];
                for (i = 0; i < selectedFeatures.getLength(); i++) {
                    feature = selectedFeaturesArray[i];
                    if (layerFeatures.indexOf(feature) != -1){
                        toRemove.push(feature);
                    }
                }
                for (i = 0; i < toRemove.length; i++){
                    selectedFeatures.remove(toRemove[i]);
                }
            }

            for (i = 0; i < layerFeatures.length; i++) {
                feature_ = layerFeatures[i];
                if (mode === IN_SELECTION){
                    if (selectedFeaturesArray.indexOf(feature_) == -1){
                        continue;
                    }
                }
                keys = feature_.getKeys();
                feature = {};
                for (var j = 0; j < keys.length; j++){
                    feature[keys[j]] = feature_.get(keys[j]);
                }
                if (this_.queryFilter(feature)){
                    if (mode !== IN_SELECTION){
                        selectedFeatures.push(feature_);
                    }
                }
                else if (mode === IN_SELECTION){
                    selectedFeatures.remove(feature_);
                }
            }
        }
    };

    document.getElementById('query-panel').style.display = 'block';

    this.updateExpression = function(){
        var input = $('#query-expression');
        var expression = input.val();
        if (!expression) {
            this_.queryFilter = null;
            input.css('background-color', '#fff');
        }
        else {
            try {
                this_.queryFilter = compileExpression(expression);
                input.css('background-color', '#fff');
            }
            catch (e) {
                this_.queryFilter = null;
                input.css('background-color', '#fdd');
            }
        }
    };

    $('#query-expression').keyup(this.updateExpression)
    .focus();

};