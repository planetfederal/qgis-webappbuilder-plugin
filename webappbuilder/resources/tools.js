var getLayerFromLayerName = function(name){
    var layer;
    var selectableLayersList = getSelectableLayers();
    for (i = 0; i < selectableLayersList.length; i++){
        if (selectableLayersList[i].get('title') == name){
            layer = selectableLayersList[i];
            break;
        }
    }
    return layer;
};

var getSourceFromLayerName = function(name){
    return sourceFromLayer(getLayerFromLayerName(name));
};

var getFeaturesFromLayerName = function(name){
    return getSourceFromLayerName(name).getFeatures();
};

var sourceFromLayer = function(layer){
    var source = layer.getSource();
    if (source instanceof ol.source.Cluster){
        return source.getSource();
    }
    else{
        return source;
    }

};

var toggleAboutPanel = function(show){
    var panel = document.getElementById('about-panel');
    if (show){
        panel.style.display = 'block';
    }
    else{
        panel.style.display = 'none';
    }
};

var decluster = function(f) {
    var features = f.get("features");
    if (features) {
        if (features.length > 1) {
            return null;
        } else {
            return features[0];
        }
    } else {
        return f;
    }
};

var getAllNonBaseLayers = function(rootLayer){
    if (typeof rootLayer === 'undefined') {
        rootLayer = map.getLayerGroup();
    }
    var nonBaseLayers = [];
    var layers = rootLayer.getLayers().getArray();
    var len = layers.length;
    for (var i = 0; i < len; i++){
        var layer = layers[i];
        if (layer.getLayers) {
            var groupLayers = getAllNonBaseLayers(layer);
            nonBaseLayers.push.apply(nonBaseLayers, groupLayers);
        }
        else if (layer.get("type") != "base"){
            nonBaseLayers.push(layer);
        }
    }
    return nonBaseLayers;
};

var getVectorLayers = function(){
    var allLayers = getAllNonBaseLayers();
    var vectorLayers = [];
    var len = allLayers.length;
    for (var i = 0; i < len; i++){
        if (allLayers[i] instanceof ol.layer.Vector){
            vectorLayers.push(allLayers[i]);
        }
    }
    return vectorLayers;
};


var getSelectableLayers = function(){
    var allLayers = getAllNonBaseLayers();
    var selectableLayers = [];
    var len = allLayers.length;
    for (var i = 0; i < len; i++){
        if (allLayers[i].get("isSelectable")){
            selectableLayers.push(allLayers[i]);
        }
    }
    return selectableLayers;
};

function busyProcess(f) {
    $("html").css("cursor", "progress");
    funct = function() {
            f();
            $("html").css("cursor", "default");
        };
    window.setTimeout(funct, 500);
}

//=======================================================
//Selection functions
//=======================================================

var SelectionManager = function(){

    this.listeners = [];

    this.addToSelection = function(features, layer){
        if (typeof layer.selectedFeatures === 'undefined') {
            layer.selectedFeatures = [];
        }
        $.merge(layer.selectedFeatures, features);
        this.notify();
        var source = sourceFromLayer(layer);
        source.dispatchEvent('change');
    };

    this.removeFromSelection = function(feature, layer){
        if (typeof layer.selectedFeatures === 'undefined') {
            return;
        }
        var idx = layer.selectedFeatures.indexOf(feature);
        if (idx > -1) {
            layer.selectedFeatures.splice(idx, 1);
        }
        this.notify();
        var source = sourceFromLayer(layer);
        source.dispatchEvent('change');
    };

    this.setSelection = function(features, layer){
        layer.selectedFeatures = [];
        $.merge(layer.selectedFeatures, features);
        this.notify();
        var source = sourceFromLayer(layer);
        source.dispatchEvent('change');
    };

    this.getSelection = function(layer){
        if (typeof layer.selectedFeatures === 'undefined') {
           return [];
        }
        else{
            return layer.selectedFeatures;
        }
    };

    this.listen = function(listener) {
        if (typeof listener === 'function' && this.listeners.indexOf(listener) == -1) {
            this.listeners.push(listener);
        }
    };

    this.notify = function() {
        for (var i = 0; i < this.listeners.length; i++){
            this.listeners[i].apply(this);
        }
    };

};

var selectionManager = new SelectionManager();

//=======================================================

saveAsPng = function(){
  canvas = document.getElementsByTagName('canvas')[0];
  canvas.toBlob(function (blob) {
    saveAs(blob, 'map.png');
  });
};

//=======================================================
showAttributesTable = function(){
    busyProcess(showAttributesTable_);
    //$("html").css("cursor", "progress");
    //window.setTimeout(showAttributesTable_, 10);
};

showAttributesTable_ = function() {
    var panels = document.getElementsByClassName('table-panel');
    if (panels.length !== 0){
        this.panel.style.display = 'block';
        return;
    }
    //var selectedFeatures = selectInteraction.getFeatures().getArray();
    this.selectedRowIndices = [];

    var this_ = this;
    this.filterTable = function(){
        if (this_.panel.style.display === 'none'){
            return;
        }

        var filterText = this_.tableFilterBox.value.toUpperCase();
        var passesFilter = function(f){
            if (filterText === ""){
                return true;
            }
            var keys = f.getKeys();
            for (var i = 0; i< keys.length; i++) {
                if (keys[i] != 'geometry') {
                    var text = "";
                    var value = f.get(keys[i]);
                    if (value){
                        text = value.toString().toUpperCase();
                    }
                    if (text.indexOf(filterText) != -1){
                        return true;
                    }
                }
            }
            return false;
        };

        this_.selectedRowIndices = [];
        var rows = this_.table.getElementsByTagName("tr");
        var layerFeatures = sourceFromLayer(this_.currentLayer).getFeatures();
        var selectedFeatures = selectionManager.getSelection(this_.currentLayer)
        for (var i = 0; i < layerFeatures.length; i++) {
            var row = rows[i + 1];
            var idx = selectedFeatures.indexOf(layerFeatures[i]);
            if (idx !== -1){
                row.className = "row-selected";
                row.style.display = passesFilter(layerFeatures[i]) ? 'table-row' : 'none';
                this_.selectedRowIndices.push(i);
            }
            else{
                row.className = "row-unselected";
                row.style.display = ! this_.onlySelectedCheck.checked
                    && passesFilter(layerFeatures[i]) ? 'table-row' : 'none';
            }
            if (layerFeatures[i].hide){
                row.className = row.className + " row-hidden-feature";
            }
        }
    };
    selectionManager.listen(this.filterTable);

    this.renderPanel = function() {
        this.formContainer = document.createElement("form");
        this.formContainer.className = "form-inline";
        this.panel.appendChild(this.formContainer);
        this.createSelector(map);
        this.createButtons();
        var p = document.createElement('p');
        this.panel.appendChild(p);
        this.currentLayer = getVectorLayers()[0];
        this.tablePanel = document.createElement('div');
        this.tablePanel.className = 'table-panel';
        this.panel.appendChild(this.tablePanel);
        this.renderTable();
    };

    this.createButtons = function() {
        var this_ = this;
        zoomTo = document.createElement("button");
        zoomTo.setAttribute("type", "button");
        zoomTo.innerHTML = '<i class="glyphicon glyphicon-search"></i> Zoom to selected';
        zoomTo.className = "btn btn-default";
        zoomTo.onclick = function(){
            features = sourceFromLayer(this_.currentLayer).getFeatures();
            extent = ol.extent.createEmpty();
            for (var i = 0; i < this_.selectedRowIndices.length; i++){
                extent = ol.extent.extend(extent,
                    features[this_.selectedRowIndices[i]].getGeometry().getExtent());
            }
            if (extent[0] == extent[2]){
                map.getView().setCenter([extent[0], extent[1]]);
                map.getView().setZoom(pointZoom);
            }
            else{
                map.getView().fit(extent, map.getSize());
            }
        };
        this.formContainer.appendChild(zoomTo);
        clear =  document.createElement("button");
        clear.setAttribute("type", "button");
        clear.innerHTML = '<i class="glyphicon glyphicon-trash"></i> Clear selected';
        clear.className = "btn btn-default";
        clear.onclick = function(){
            selectionManager.setSelection([], this_.currentLayer);
        };
        this.formContainer.appendChild(clear);

        tableFilterLabel = document.createElement("label");
        tableFilterLabel.innerHTML = " Filter:"
        this.formContainer.appendChild(tableFilterLabel);
        this.tableFilterBox = document.createElement("input");
        this.tableFilterBox.setAttribute("type", "text");
        this.tableFilterBox.setAttribute("value", "");
        this.tableFilterBox.className = "form-control";
        this.tableFilterBox.setAttribute("placeholder", "Type filter expression...")
        this.tableFilterBox.onkeyup = this.filterTable;
        this.formContainer.appendChild(this.tableFilterBox);

        onlySelected = document.createElement("label");
        this.onlySelectedCheck = document.createElement("input");
        this.onlySelectedCheck.setAttribute("type", "checkbox");
        this.onlySelectedCheck.setAttribute("value", "");
        this.onlySelectedCheck.onclick = this.filterTable;
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

        var cols = sourceFromLayer(this.currentLayer).getFeatures()[0].getKeys();
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
        var selectedFeatures = selectionManager.getSelection(this.currentLayer)
        layerFeatures = sourceFromLayer(this.currentLayer).getFeatures();
        for (var i = 0; i < layerFeatures.length; i++) {
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
            if (feature.hide === true){
                row.className = row.className + " row-hidden-feature";
            }
            for (var j = 0; j < keys.length; j++) {
                if (keys[j] != 'geometry') {
                    var cell = row.insertCell(-1);
                    var text = feature.get(keys[j]);
                    if (this.isLink(text)){
                        text = "<a href='" + text + "' target='_blank' >" + text + "</a>";
                    }
                    cell.innerHTML = text;
                    cell.style.whiteSpace = "nowrap"
                }
            }
        }

        if (this.currentLayer.get("isSelectable")){
            var rows = this.table.getElementsByTagName("tr");
            for (var i = 1; i < rows.length; i++) {
                (function (idx) {
                    rows[idx].addEventListener("click",function(){
                        this_.rowClicked(rows[idx], idx)}, false);
                    }
                )(i);
            }
        }
        this.tablePanel.appendChild(this.table);
    };

    this.isLink = function(text){
        var regexpUrl = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
        var isUrl = regexpUrl.test(text);
        var regexpFile = /.*[\\\\/].*\..*/
        var isFile = regexpFile.test(text);
        return isUrl || isFile;
    };

    this.rowClicked = function(row, idx){
        var layerFeatures = sourceFromLayer(this.currentLayer).getFeatures();
        var feature = layerFeatures[idx - 1];
        if (row.className != "row-selected" && row.className != "row-selected row-hidden-feature"){
            selectionManager.addToSelection([feature], this.currentLayer);
        }
        else{
            selectionManager.removeFromSelection(feature, this.currentLayer);
        }
    }

    this.createSelector = function(map) {
        label = document.createElement("label");
        label.innerHTML = "Layer:";
        this.formContainer.appendChild(label);
        this.sel = document.createElement('select');
        this.sel.className = "form-control";
        this_ = this;
        var vectorLayers = getVectorLayers()
        this.sel.onchange = function(){
            for (var i = 0; i < vectorLayers.length; i++){
                if (vectorLayers[i].get('title') == this.value){
                    this_.currentLayer = vectorLayers[i];
                    break;
                }
            }
            this_.renderTable();
        };

        for (var i = 0, l; i < vectorLayers.length; i++) {
            l = vectorLayers[i];
            var title = l.get('title');
            if (title){
                var option = document.createElement('option');
                option.value = option.textContent = title;
                this.sel.appendChild(option);
            }
        }

        this.formContainer.appendChild(this.sel);
    };

    this.panel = document.getElementsByClassName('attributes-table')[0];
    this.renderPanel();
    this.panel.style.display = 'block';

    var closer = document.getElementById('attributes-table-closer');
    if (closer){
        closer.onclick = function() {
            this_.panel.style.display = 'none';
            closer.blur();
            return false;
        };
    }
    $("html").css("cursor", "default");

};

//===================

var geocodingStyle = new ol.style.Style({
  image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
    anchor: [0.5, 46],
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    opacity: 0.75,
    src: './resources/marker.png'
  }))
});
var geocodingSource = new ol.source.Vector({});
var geocodingLayer = new ol.layer.Vector({
  source: geocodingSource
});

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
    var pos = ol.proj.transform([lng1, lat1], 'EPSG:4326', 'EPSG:3857')
    map.getView().setCenter(pos);
    map.getView().setZoom(10);
    var feat = new ol.Feature({
      geometry: new ol.geom.Point(pos),
    });
    feat.setStyle(geocodingStyle);
    geocodingSource.clear()
    geocodingSource.addFeature(feat)
    map.removeLayer(geocodingLayer)
    map.addLayer(geocodingLayer)
};

searchBoxKeyPressed = function(e){
    e = e || window.event;
    if (e.keyCode == 13){
        searchAddress();
    }
}


//===========================================

getBookmarkExtentInViewCrs = function(extent){

    var viewCrs = view.getProjection().getCode()
    return ol.proj.transformExtent(extent, "EPSG:3857", viewCrs)

};

goToBookmarkByName = function(name){
    for(var i=0; i<bookmarks.length; i++){
        if (bookmarks[i][0] === name){
            map.getView().fit(getBookmarkExtentInViewCrs(bookmarks[i][1]),
                map.getSize());
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
    goToBookmark(i);

};

goToBookmark = function(i){
    bookmark = bookmarks[i];
    if (bookmark){
        map.getView().fit(getBookmarkExtentInViewCrs(bookmark[1]), map.getSize());
    }
    else{
        map.getView().fit(originalExtent, map.getSize());
    }
};

//===========================================
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
        map.removeInteraction(currentInteraction)
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

//==============================================

openChart = function(c){

    chartPanel = document.getElementById('chart-panel');
    chartPanel.style.display = 'block';

    this.drawFromSelection = function(){
        if (chartPanel.style.display === 'none'){
            return;
        }

        $('body').addClass('waiting');
        var layerName = charts[c].layer;
        var categoryField = charts[c].categoryField;
        var valueFields = charts[c].valueFields;
        var lyrs = map.getLayers().getArray();
        var lyr = null;
        for (var i = 0; i < lyrs.length; i++){
            if (lyrs[i].get('title') == layerName){
                lyr = lyrs[i];
                break;
            }
        }
        var selectedFeatures = selectionManager.getSelection(lyr);
        var columns = [["x"]];
        if (charts[c].displayMode === DISPLAY_MODE_COUNT){
            columns.push(["Feature count"]);
        }
        else{
            for (var i = 0; i < valueFields.length; i++) {
                columns.push([valueFields[i]]);
            }
        }
        var selectedCount = 0;
        if (charts[c].displayMode === DISPLAY_MODE_FEATURE){
            for (var i = 0; i < selectedFeatures.length; i++) {
                columns[0].push(selectedFeatures[i].get(categoryField));
                for (var j = 0; j < valueFields.length; j++) {
                    columns[j+1].push(selectedFeatures[i].get(valueFields[j]));
                }
            }
        }
        else if (charts[c].displayMode === DISPLAY_MODE_CATEGORY){
            values = {};
            for (var i = 0; i < selectedFeatures.length; i++) {
                cat = selectedFeatures[i].get(categoryField);
                if (cat == null){
                    continue;
                }
                cat = cat.toString();
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
            for (var key in values){
                columns[0].push(key);
                aggregated = [];
                for (var i = 0; i < valueFields.length; i++) {
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
            for (var i = 0; i < selectedFeatures.length; i++) {
                cat = selectedFeatures[i].get(categoryField)
                if (cat == null){
                    continue;
                }
                cat = cat.toString();
                if (!(cat in values)){
                    values[cat] = 1;
                }
                else{
                    values[cat]++;
                }
            }

            var sorted = [];
            for (var key in values){
                sorted.push([key, values[key]]);
            }
            sorted.sort(function(a, b) {return b[1] - a[1]});

            for (var i = 0; i < sorted.length; i++) {
                columns[0].push(sorted[i][0]);
                columns[1].push(sorted[i][1]);
            }
        }
        var info = document.getElementById('chart-panel-info');
        info.innerHTML = selectedFeatures.length.toString() + " features selected in layer " + layerName;

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
        $('body').addClass('waiting');
    };

    this.drawFromSelection();

    selectionManager.listen(this.drawFromSelection);

    var this_ = this;
    var closer = document.getElementById('chart-panel-closer');
    if (closer){
        closer.onclick = function() {
            chartPanel.style.display = 'none';
            closer.blur();
            return false;
        };
    }
};

//===========================================

showQueryPanel = function(){

    var select = document.getElementById('query-layer');
    if (select.options.length === 0){
        for (var i = 0, l; i < getSelectableLayers().length; i++) {
            l = getSelectableLayers()[i];
            var option = document.createElement('option');
            option.value = option.textContent = l.get('title');
            select.appendChild(option);
        }
    }

    var close = document.getElementById('btn-close-query');
    if (close){
        close.onclick = function() {
            document.getElementById('query-panel').style.display = 'none';
            return false;
        };
    }

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
            for (var i = 0; i < lyrs.length; i++){
                if (lyrs[i].get('title') === layerName){
                    layer = lyrs[i];
                    break;
                }
            }
            var layerFeatures = sourceFromLayer(layer).getFeatures();
            var selectedFeatures = selectionManager.getSelection(layer);
            var createFeatureObject = function(feature_){
                feature = {};
                keys = feature_.getKeys();
                for (var j = 0; j < keys.length; j++){
                    feature[keys[j]] = feature_.get(keys[j]);
                }
                return feature;
            }
            if (mode === NEW_SELECTION){
                var newSelection = [];
                for (var i = 0; i < layerFeatures.length; i++) {
                    var feature = createFeatureObject(layerFeatures[i]);
                    if (this_.queryFilter(feature)){
                        newSelection.push(layerFeatures[i]);
                    }
                }
                selectionManager.setSelection(newSelection, layer)
            }
            else if (mode === IN_SELECTION){
                var newSelection = [];
                for (var i = 0; i < selectedFeatures.length; i++) {
                    var feature = createFeatureObject(selectedFeatures[i]);
                    if (this_.queryFilter(feature)){
                        newSelection.push(selectedFeatures[i]);
                    }
                }
                selectionManager.setSelection(newSelection, layer)
            }
            else{
                var newSelection = [];
                for (var i = 0; i < layerFeatures.length; i++) {
                    if (selectedFeatures.indexOf(layerFeatures[i]) != -1){
                        newSelection.push(layerFeatures[i]);
                    }
                    else{
                        var feature = createFeatureObject(layerFeatures[i]);
                        if (this_.queryFilter(feature)){
                            newSelection.push(layerFeatures[i]);
                        }
                    }
                }
                selectionManager.setSelection(newSelection, layer)
            }
            selectionManager.setSelection(newSelection, layer)



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

//============================================================================

selectByRectangle = function(){

    measureTool(null);
    if (currentInteraction){
        map.removeInteraction(currentInteraction)
    }
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
    currentInteraction = dragBoxInteraction;

};

//===========================================================================

removeSelectionTool = function(){

    measureTool(null);
    if (currentInteraction){
        map.removeInteraction(currentInteraction);
        currentInteraction = null;
    }
};


//============================================================================

var selectByPolygonSource = new ol.source.Vector();

selectByPolygon = function(){

    measureTool(null);
    if (currentInteraction){
        map.removeInteraction(currentInteraction);
    }

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
      currentInteraction = selectByPolygonInteraction;

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

//==========================================

var addLayerFromFile = function(){

    var readFeatures = function(text){
        var formats = [new ol.format.GeoJSON(), new ol.format.KML(), new ol.format.GPX()]
        for(var i=0, len=formats.length; i< len; i++){
            var format = formats[i];
            try {
                var crs = format.readProjection(text);
                var features = format.readFeatures(text,
                        {dataProjection: crs.getCode(),
                        featureProjection: map.getView().getProjection().getCode()});
                return features;
            } catch (e) {}
        }
        return null;
    }

    var _addLayerFromFile = function(f){
        if (f) {
            var r = new FileReader();
            r.onload = function(e) {
                var contents = e.target.result;
                var features = readFeatures(contents);
                if (features){
                    var lyr = new ol.layer.Vector({
                        source:  new ol.source.Vector({
                                    features: features
                                }),
                        title: f.name,
                        isRemovable: true,
                        isSelectable: true
                    });
                    map.addLayer(lyr);
                }
                else{
                    $("html").css("cursor", "default");
                    alert("Failed to load file");
                }
            }
            r.readAsText(f);
        } else {
            alert("Failed to load file");
        }
    };

    var input = document.createElement('input');
    input.type = "file";
    input.accept=".geojson, .gpx, .kml"
    $(input).on("change", function(){
        var filename = input.files[0];
        busyProcess(function(){_addLayerFromFile(filename)}, 500);
        ;
    });
    $(input).trigger('click');

    return false;

};

var editLayerFilters = function(layer){
    var layername = layer.get("title");
    var filters = layer.get("filters");

    var html =  '<div class="row">  ' +
            '<div class="col-md-12"> <form class="form-horizontal"> ' +
            '<div id="filter-form-group" class="form-group"> ' +
            '<div class="col-sm-10"><input id="filter-textbox" value="" type="text" class="form-control input-md"/></div>' +
            '<div class="col-sm-2"><button type="button" onclick="addFilterToLayer(\'' + layername + '\')" class="btn btn-primary">Add</button></div>' +
            '</div></form><hr><form id="layer-filters" class="form-horizontal">'

    for (var i = 0; i < filters.length; i++) {
        var filter = filters[i];
        var filterName = filter.replace(/\W+/g,"");
        html +=  ' <div class="form-group" id="filter_' + filterName + '"> ' +
                '<div class="col-sm-10"><label>' + filter + '</label></div>' +
                '<div class="col-sm-2"><button type="button"' +
                ' onclick="removeFilterFromLayer(\'' + filterName + "','" + layername + '\')"  class="btn btn-link">Remove</button></div>' +
                '</div>';
    }
    html += '</form></div></div>';
    bootbox.dialog({
        title: "Filters for layer " + layer.get("title"),
        message: html,
        buttons: {
            success: {
                label: "Close",
                className: "btn-success",
                callback: function () {
                }
            }
        }
    });

}


var removeFilterFromLayer = function(filter, layername){
    var layer = getLayerFromLayerName(layername);
    var filters = layer.get("filters");
    for (var i = 0; i < filters.length; i++){
        var filterName = filters[i].replace(/\W+/g,"");
        if (filterName == filter){
            filters.splice(i, 1);
            break;
        }
    }
    layer.set("filters", filters);
    var div = $("#filter_" + filter);
    div.remove();
    updateLayerFilteredRendering(layer);
};

var addFilterToLayer = function(layername){
    var layer = getLayerFromLayerName(layername);
    var filters = layer.get("filters");
    var filter = $("#filter-textbox").val()
    try{
        compileExpression(filter);
        $("#filter-form-group").attr("class", "form-group")
    }
    catch(e){
        $("#filter-form-group").attr("class", "form-group has-error")
        return;
    }
    filters.push(filter)
    layer.set("filters", filters);
    var filterName = filter.replace(/\W+/g,"");
    html =  ' <div class="form-group" id="filter_' + filterName  + '"> ' +
            '<div class="col-sm-10"><label>' + filter + '</label></div>' +
            '<div class="col-sm-2"><button type="button"' +
            ' onclick="removeFilterFromLayer(\'' + filterName + "','" + layername + '\')"  class="btn btn-link">Remove</button></div>' +
            '</div>';
    $("#layer-filters").append(html);
    updateLayerFilteredRendering(layer);


};

var updateLayerFilteredRendering = function(layer){

    var filterExpressions = layer.get("filters");
    var filters = [];
    for(var i = 0; i<filterExpressions.length; i++){
        filters.push(compileExpression(filterExpressions[i]));
    }
    var layerFeatures = sourceFromLayer(layer).getFeatures();
    var createFeatureObject = function(feature_){
        feature = {};
        keys = feature_.getKeys();
        for (var j = 0; j < keys.length; j++){
            feature[keys[j]] = feature_.get(keys[j]);
        }
        return feature;
    };

    for (var i = 0; i < layerFeatures.length; i++) {
        var feature = createFeatureObject(layerFeatures[i]);
        var hide = false;
        for (var j = 0; j < filters.length; j++){
            if (!filters[j](feature)){
                hide = true;
                continue;
            }
        }
        layerFeatures[i].hide = hide;
    }
    layer.getSource().changed();

};
