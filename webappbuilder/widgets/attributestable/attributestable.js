showAttributesTable = function(){
    busyProcess(showAttributesTable_);
};

showAttributesTable_ = function() {
    var panels = document.getElementsByClassName('table-panel');
    if (panels.length !== 0){
        this.panel.style.display = 'block';
        return;
    }
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
        var selectedFeatures = selectionManager.getSelection(this_.currentLayer);
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
        var zoomTo = document.createElement("button");
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
        var clear =  document.createElement("button");
        clear.setAttribute("type", "button");
        clear.innerHTML = '<i class="glyphicon glyphicon-trash"></i> Clear selected';
        clear.className = "btn btn-default";
        clear.onclick = function(){
            selectionManager.setSelection([], this_.currentLayer);
        };
        this.formContainer.appendChild(clear);

        var group = document.createElement('div');
        group.className = "input-group";
        var tableFilterLabel = document.createElement("span");
        tableFilterLabel.innerHTML = "Filter";
        tableFilterLabel.className = "input-group-addon";
        group.appendChild(tableFilterLabel);
        this.tableFilterBox = document.createElement("input");
        this.tableFilterBox.setAttribute("type", "text");
        this.tableFilterBox.setAttribute("value", "");
        this.tableFilterBox.className = "form-control";
        this.tableFilterBox.setAttribute("placeholder", "Type filter expression...");
        this.tableFilterBox.onkeyup = this.filterTable;
        group.appendChild(this.tableFilterBox);
        this.formContainer.appendChild(group);

        onlySelected = document.createElement("label");
        this.onlySelectedCheck = document.createElement("input");
        this.onlySelectedCheck.setAttribute("type", "checkbox");
        this.onlySelectedCheck.setAttribute("value", "");
        this.onlySelectedCheck.onclick = this.filterTable;
        onlySelected.appendChild(this.onlySelectedCheck);
        onlySelected.appendChild(document.createTextNode(" Show only selected features"));
        this.formContainer.appendChild(onlySelected);

    };

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
                    cell.style.whiteSpace = "nowrap";
                }
            }
        }

        if (this.currentLayer.get("isSelectable")){
            var rows = this.table.getElementsByTagName("tr");
            for (var i = 1; i < rows.length; i++) {
                (function(idx){
                rows[idx].addEventListener("click",function(){
                    this_.rowClicked(idx, rows[idx]);
                }, false);})(i);
            }
        }
        this.tablePanel.appendChild(this.table);
    };

    this.isLink = function(text){
        var regexpUrl = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
        var isUrl = regexpUrl.test(text);
        var regexpFile = /.*[\\\\/].*\..*/;
        var isFile = regexpFile.test(text);
        return isUrl || isFile;
    };

    this.rowClicked = function(idx, row){
        var layerFeatures = sourceFromLayer(this.currentLayer).getFeatures();
        if (window.event.shiftKey && this_.lastSelectedRow){
            selFeatures = [];
            var min = Math.min(idx, this_.lastSelectedRow);
            var max = Math.max(idx, this_.lastSelectedRow);
            for (var j = min; j <= max; j++){
                selFeatures.push(layerFeatures[j - 1]);
            }
            selectionManager.clearSelection(this.currentLayer);
            selectionManager.addToSelection(selFeatures, this.currentLayer);
        }
        else if (window.event.ctrlKey){
            var feature = layerFeatures[idx - 1];
            if (row.className != "row-selected" && row.className != "row-selected row-hidden-feature"){
                selectionManager.addToSelection([feature], this.currentLayer);
            }
            else{
                selectionManager.removeFromSelection(feature, this.currentLayer);
            }
        }
        else{
            selectionManager.clearSelection(this.currentLayer);
            selectionManager.addToSelection([layerFeatures[idx - 1]], this.currentLayer);
        }
        this_.lastSelectedRow = idx;
    };

    this.createSelector = function(map) {

        var group = document.createElement('div');
        group.className = "input-group";
        label = document.createElement("span");
        label.innerHTML = "Layer";
        label.className = "input-group-addon";
        this.sel = document.createElement('select');
        this.sel.className = "form-control";
        group.appendChild(label)
        group.appendChild(this.sel)
        this_ = this;
        var vectorLayers = getVectorLayers();
        this.sel.onchange = function(){
            for (var i = 0; i < vectorLayers.length; i++){
                if (vectorLayers[i].get('title') == this.value){
                    this_.currentLayer = vectorLayers[i];
                    this_.lastSelectedRow = null;
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

        this.formContainer.appendChild(group);
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
