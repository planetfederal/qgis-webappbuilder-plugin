saveAsPng = function(){
    map.once('postcompose', function(event) {
      var canvas = event.context.canvas;
      button.href = canvas.toDataURL('image/png');
    });
    map.renderSync();
};


//=======================================================

showAttributesTable = function() {

    panels = document.getElementsByClassName('table-panel');
    if (panels.length != 0){        
        this.panel.style.display = 'block';
        return                    
    }

    this.mapListeners = [];
    this.selectedRowIndices = [];

    this.renderPanel = function() {
        interactions = map.getInteractions();
        this.selectInteraction = null;
        for (i = 0; i < interactions.length; i++){
            if (typeof interactions[i] === "ol.interaction.Select"){
                this.selectInteraction = interactions[i];
                break;
            }
        }
        text = document.createTextNode("Layer: ");
        this.panel.appendChild(text);
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
        zoomTo.innerHTML = "Zoom to selected";
        zoomTo.onclick = function(){
            features = this_.currentLayer.getSource().getFeatures();
            extent = ol.extent.createEmpty()
            for (i = 0; i < this_.selectedRowIndices.length; i++){
                extent = ol.extent.extend(extent,
                    features[this_.selectedRowIndices[i]].getGeometry().getExtent())
            }
        };
        this.panel.appendChild(zoomTo)
        clear =  document.createElement("button")
        clear.setAttribute("type", "button")
        clear.innerHTML = "Clear selected"
        clear.onclick = function(){
            this_.selected = []
            var rows = this_.table.getElementsByTagName("tr");    
            for (var i = 0; i < rows.length; i++) {
                rows[i].className = "row-unselected";
            }
        };
        this.panel.appendChild(clear);
    }


    this.changeVisibility = function() {
        if (this.element.className != this.shownClassName) {
            this.element.className = this.shownClassName;
            this.renderPanel();
        }
        else{
            this.element.className = this.hiddenClassName;
        }
    };


    this.renderTable = function() {    
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


    this.createSelector = function(map) {
        this.sel = document.createElement('select');    
        this_ = this
        this.sel.onchange = function(){
            var lyr = null;
            var lyrs = map.getLayers().getArray().slice().reverse();
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

    this.panel = document.getElementsByClassName('attributes-table')[0];
    this.renderPanel()
    this.panel.style.display = 'block';

    var this_ = this;
    var closer = document.getElementById('attributes-table-closer');
    closer.onclick = function() {
        this_.panel.style.display = 'none';
        closer.blur();
        return false;
    };

};





