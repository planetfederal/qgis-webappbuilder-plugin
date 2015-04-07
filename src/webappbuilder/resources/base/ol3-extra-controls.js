ol.control.CesiumControl = function(ol3d) {

  var button = document.createElement('button');
  button.innerHTML = '3D';

  var enable3DView = function(e) {
    if (ol3d.getEnabled()){
        ol3d.setEnabled(false)
        button.innerHTML = '3D';
    }
    else{
        button.innerHTML = '2D';
        ol3d.setEnabled(true)
    }
  };

  button.addEventListener('click', enable3DView, false);
  button.addEventListener('touchstart', enable3DView, false);

  var element = document.createElement('div');
  element.className = 'enable3d-control ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element,
  });

};
ol.inherits(ol.control.CesiumControl, ol.control.Control);

//=======================================================

ol.control.SaveAsPng = function() {

  var button = document.createElement('button');

  var saveAsPng = function(e){
    map.once('postcompose', function(event) {
      var canvas = event.context.canvas;
      button.href = canvas.toDataURL('image/png');
    });
    map.renderSync()
  };

  button.addEventListener('click', saveAsPng, false);
  button.addEventListener('touchstart', saveAsPng, false);

  var element = document.createElement('div');
  element.className = 'savepng-control ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element,
  });

};
ol.inherits(ol.control.SaveAsPng, ol.control.Control);

//=======================================================

ol.control.AttributesTable = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
      options.tipLabel : 'Attributes table';

    this.mapListeners = [];
    this.selectedRowIndices = [];

    this.hiddenClassName = 'ol-unselectable ol-control attributes-table';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    this.panel = document.createElement('div');
    this.panel.className = 'panel';
    element.appendChild(this.panel);

    var this_ = this;
    button.onclick = function(e) {
        this_.changeVisibility();
    };

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });


};

ol.inherits(ol.control.AttributesTable, ol.control.Control);

ol.control.AttributesTable.prototype.renderPanel = function() {
    interactions = this.getMap().getInteractions();
    this.selectInteraction = null;
    for (i = 0; i < interactions.length; i++){
        if (typeof interactions[i] === "ol.interaction.Select"){
            this.selectInteraction = interactions[i];
            break;
        }
    }
    while(this.panel.firstChild) {
        this.panel.removeChild(this.panel.firstChild);
    }
    text = document.createTextNode("Layer: ")
    this.panel.appendChild(text)    
    this.createSelector(this.getMap())
    this.createButtons()
    var p = document.createElement('p');
    this.panel.appendChild(p)
    this.currentLayer = this.getMap().getLayers().getArray().slice().reverse()[0];
    this.tablePanel = document.createElement('div');
    this.tablePanel.className = 'inner-panel';
    this.panel.appendChild(this.tablePanel);
    this.renderTable();
};

ol.control.AttributesTable.prototype.createButtons = function() {
    this_ = this;
    zoomTo = document.createElement("input");
    zoomTo.setAttribute("type", "button");
    zoomTo.setAttribute("value", "Zoom to selected");
    zoomTo.onclick = function(){
        features = this_.currentLayer.getSource().getFeatures();
        extent = ol.extent.createEmpty()
        for (i = 0; i < this_.selectedRowIndices.length; i++){
            extent = ol.extent.extend(extent,
                features[this_.selectedRowIndices[i]].getGeometry().getExtent())
        }
    };
    this.panel.appendChild(zoomTo)
    clear =  document.createElement("input")
    clear.setAttribute("type", "button")
    clear.setAttribute("value", "Clear selected")
    clear.onclick = function(){
        this_.selected = []
        var rows = this_.table.getElementsByTagName("tr");    
        for (var i = 0; i < rows.length; i++) {
            rows[i].className = "row-unselected";
        }
    };
    this.panel.appendChild(clear);
}


ol.control.AttributesTable.prototype.changeVisibility = function() {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
        this.renderPanel();
    }
    else{
        this.element.className = this.hiddenClassName;
    }
};


ol.control.AttributesTable.prototype.renderTable = function() {    
    try{
        this.tablePanel.removeChild(this.table);
    }
    catch(err){}
    this.table = document.createElement("TABLE");
    this.table.border = "1";

    cols = this.currentLayer.getSource().getFeatures()[0].getKeys();
    var row = this.table.insertRow(-1);
    
    for (var i = 0; i < cols.length; i++) {
        if (cols[i] != 'geometry') {
            var headerCell = document.createElement("TH");
            headerCell.innerHTML = cols[i];
            row.appendChild(headerCell);
        }
    }

    this_ = this
    this.currentLayer.getSource().forEachFeature(function(feature){
        keys = feature.getKeys();
        row = this_.table.insertRow(-1);  
        for (var j = 0; j < keys.length; j++) {
            if (keys[j] != 'geometry') {
                var cell = row.insertCell(-1);
                cell.innerHTML = feature.get(keys[j]);                
            }            
        }
    });

    var rows = this.table.getElementsByTagName("tr");    
    for (var i = 0; i < rows.length; i++) {
        (function (idx) {
            rows[idx].addEventListener("click", 
                function () {
                    if (this.className != "row-selected"){
                        this.className = "row-selected"
                        this_.selectedRowIndices.push(idx)
                    }
                    else{
                        arrayIdx = this_.selectedRowIndices.indexOf(idx)
                        this_.selectedRowIndices.splice(arrayIdx, 1)
                        this.className = "row-unselected"   
                    }
                }, false);
        })(i);
    }
    this.tablePanel.appendChild(this.table);
};


ol.control.AttributesTable.prototype.createSelector = function(map) {
    this.sel = document.createElement('select');    
    this_ = this
    this.sel.onchange = function(){
        var lyr = null;
        var lyrs = this_.getMap().getLayers().getArray().slice().reverse();
        for (i = 0; i < lyrs.length; i++){
            if (lyrs[i].get('title') == this.value){
                this_.currentLayer = lyrs[i];
                break
            }
        }        
        this_.renderTable()};
    var lyrs = map.getLayers().getArray().slice().reverse();
    for (var i = 0, l; i < lyrs.length; i++) {
        l = lyrs[i];
        if (l.get('title') && !(typeof l.getSource === "undefined")) {
            var option = document.createElement('option');    
            option.value = option.textContent = l.get('title');
            this.sel.appendChild(option);
        }
    }
    this.panel.appendChild(this.sel);
};

ol.control.AttributesTable.prototype.setMap = function(map) {
    // Clean up listeners associated with the previous map
    for (var i = 0, key; i < this.mapListeners.length; i++) {
        this.getMap().unByKey(this.mapListeners[i]);
    }
    this.mapListeners.length = 0;
    // Wire up listeners etc. and store reference to new map
    ol.control.Control.prototype.setMap.call(this, map);
    if (map) {
        this.renderPanel();
    }
};


//======================================================================


ol.control.ChartTool = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
      options.tipLabel : 'ChartTool';

    this.mapListeners = [];

    this.hiddenClassName = 'ol-unselectable ol-control chart-tool';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    this.panel = document.createElement('div');
    this.panel.className = 'panel';
    element.appendChild(this.panel);

    var this_ = this;
    button.onclick = function(e) {
        this_.changeVisibility();
    };

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });


};

ol.inherits(ol.control.ChartTool, ol.control.Control);

ol.control.ChartTool.prototype.renderPanel = function() {


};

ol.control.ChartTool.prototype.changeVisibility = function() {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
        this.renderPanel();
    }
    else{
        this.element.className = this.hiddenClassName;
    }

};

ol.control.ChartTool.prototype.setMap = function(map) {
    // Clean up listeners associated with the previous map
    for (var i = 0, key; i < this.mapListeners.length; i++) {
        this.getMap().unByKey(this.mapListeners[i]);
    }
    this.mapListeners.length = 0;
    // Wire up listeners etc. and store reference to new map
    ol.control.Control.prototype.setMap.call(this, map);
    if (map) {
        var this_ = this;
        this.renderPanel();
    }
};
