var showEditPanel = function(){

    var select = document.getElementById('edit-layer');
    var populateLayers = function(){
        $("#edit-layer").empty();
        var vectorLayers = getVectorLayers();
        var editableLayersFound = false;
        for (var i = 0, lay; i < getVectorLayers().length; i++) {
            lay = vectorLayers[i];
            var coll = sourceFromLayer(lay).getFeaturesCollection();
            if (coll){
                var option = document.createElement('option');
                option.value = option.textContent = lay.get('title');
                select.appendChild(option);
                editableLayersFound = true;
            }
        }
        if (!editableLayersFound){
            var option = document.createElement('option');
            option.value = option.textContent = "[No editable layers available]";
            select.appendChild(option);
        }
    };
    if (select.options.length === 0){
        select.onchange = function(e) {
            if (currentInteractions && currentInteractions[1] instanceof ol.interaction.Modify){
                enableEditTool();
            }
        };
        map.getInteractions().on("change:length", function(){
            var interactions = map.getInteractions().getArray();
            for (var i = 0; i < interactions.length; i++){
                if (interactions[i] instanceof ol.interaction.Modify){
                    return;
                }
            }
            var toggleEdit = document.getElementById('btn-edit-tool');
            toggleEdit.innerHTML = "Enable edit mode";
            toggleEdit.className = "btn btn-primary";
        });
        map.getLayers().on("change:length", populateLayers);
    }
    populateLayers();


    var close = document.getElementById('btn-close-edit');
    if (close){
        close.onclick = function() {
            document.getElementById('edit-tool-panel').style.display = 'none';
            return false;
        };
    }

    var addLayer = document.getElementById('btn-add-empty-layer');
    addLayer.onclick = function(){
        createEmptyLayer();
    };
    var toggleEdit = document.getElementById('btn-edit-tool');
    toggleEdit.onclick = function(){
        if (currentInteractions && currentInteractions[1] instanceof ol.interaction.Modify){
            removeInteractions();
            toggleEdit.innerHTML = "Enable edit mode";
            toggleEdit.className = "btn btn-primary";
        }
        else{
            var layerName = document.getElementById('edit-layer').value;
            var layer = getLayerFromLayerName(layerName);
            if (layer){
                enableEditTool();
                toggleEdit.innerHTML = "Disable edit mode";
                toggleEdit.className = "btn btn-success";
            }
            else{
                var panel = document.getElementById('edit-tool-panel');
                var alert = document.createElement("div");
                alert.className = "alert alert-warning";
                alert.innerHTML = '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
                    'No editable layer is available. Create one to start editing.';
                panel.appendChild(alert);
            }
        }
    };

    document.getElementById('edit-tool-panel').style.display = 'block';

};

var createEmptyLayer = function(){

    var html = '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal"> ' +
            '<div class="form-group"> ' +
            '<label class="col-md-6 control-label" for="new-layer-name"> Layer name </label>'+
            '<div class="col-md-4"> <input id="new-layer-name" type="text" class="form-control input-md">' +
            '</div></div>'+
            '<div class="form-group"> ' +
            '<label class="col-md-6 control-label" for="geom-type-dropdown"> Geometry type</label> ' +
            '<div class="col-md-4">' +
            '<select class="form-control" id="geom-type-dropdown">'+
            '<option>Point</option>'+
            '<option>LineString</option>'+
            '<option>Polygon</option>'+
            '</select></div></div>' +
            '<div class="form-group"> ' +
            '<label class="col-md-6 control-label" for="new-layer-fields"> Attributes (comma-separated names) </label>'+
            '<div class="col-md-4"> <input id="new-layer-fields" type="text" class="form-control input-md">' +
            '</div></div>'+
            '<div class="form-group"> ' +
            '<label class="col-md-6 control-label" for="new-layer-color"> Color </label>'+
            '<div class="col-md-4"> <input value="#000000" id="new-layer-color" type="text" class="color-picker form-control">' +
            '</div></div>'+
            '<div class="form-group"> ' +
            '<label class="col-md-6 control-label" for="new-layer-fillcolor"> Fill color (polygons only) </label>'+
            '<div class="col-md-4"> <input value="#0000aa" id="new-layer-fillcolor" type="text" class="color-picker form-control">' +
            '</div></div>'+
            '</form></div></div>';

    var dialog = bootbox.dialog({
        title: "Create empty layer",
        message: html,
        buttons: {
            success: {
                label: "Ok",
                className: "btn-success",
                callback: function () {
                    var type = $("#geom-type-dropdown").val();
                    var attributes = $("#new-layer-fields").val();
                    var title = $("#new-layer-name").val().toString();
                    var color = $("#new-layer-color").val().toString();
                    var fillColor = $("#new-layer-fillcolor").val().toString();
                    _createEmptyLayer(title, type, attributes, color, fillColor);
                }
            }
        },
        show: false
    });

    dialog.on('show.bs.modal', function(){
        $(".color-picker").colorpicker();
    });

    dialog.modal("show");
};

var _createEmptyLayer = function(title, type, attributes, color, fillColor){

    var layer = new ol.layer.Vector({
        title: title,
        geomType: type,
        schema: attributes,
        isSelectable: true,
        isRemovable: true,
        source: new ol.source.Vector({features: new ol.Collection()}),
    });

    var style = function(feature, resolution) {
        var selected = layer.selectedFeatures;
        if (selected && selected.indexOf(feature) != -1) {
            return [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: "rgba(255, 204, 0, 1)",
                        }),
                        stroke: new ol.style.Stroke({
                            color: "rgba(255, 204, 0, 1)",
                            width: 2
                        }),
                        image: new ol.style.Circle({
                            radius: 7,
                            fill: new ol.style.Fill({
                                color: "rgba(255, 204, 0, 1)",
                            })
                        })
                    })];
        }
        else{
            return [new ol.style.Style({
                        fill: new ol.style.Fill({
                            color: fillColor
                        }),
                        stroke: new ol.style.Stroke({
                            color: color,
                            width: 2
                        }),
                        image: new ol.style.Circle({
                            radius: 7,
                            fill: new ol.style.Fill({
                                color: color
                            })
                        })
                    })];
        }
    };

    layer.setStyle(style);
    map.addLayer(layer);

};

var enableEditTool = function(){

    var layerName = document.getElementById('edit-layer').value;
    var layer = getLayerFromLayerName(layerName);
    var geomType = layer.get("geomType");
    var schema = layer.get("schema").trim();

    removeInteractions();

    var featColl = layer.getSource().getFeaturesCollection();
    var editInteraction = new ol.interaction.Draw({
                                    features: featColl,
                                    type: geomType});

    if (schema.length !== 0 ){
        editInteraction.on("drawend", function(e){
            var feature = e.feature;
            var attributes = schema.split(",");
            editNewFeatureAttributes(feature, attributes);
        });
    }

    var modifyInteraction = new ol.interaction.Modify({
      features: featColl,
      deleteCondition: function(event) {
        return ol.events.condition.shiftKeyOnly(event) &&
            ol.events.condition.singleClick(event);
      }
    });

    map.addInteraction(modifyInteraction);
    map.addInteraction(editInteraction);

    currentInteractions = [editInteraction, modifyInteraction];

}

var editNewFeatureAttributes = function(feature, attributes){

    var html = '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal">';

    for (var i = 0; i < attributes.length; i++) {
        var attr = attributes[i];
        html += '<div class="form-group"> ' +
                '<label class="col-md-6 control-label"' +
                '" for="new-layer-field-value-' + attr +'">' + attr +'</label> ' +
                '<div class="col-md-4"> <input id="new-layer-field-value-' + attr +'" name="' + attr +
                '" type="text" class="form-control input-md"> </div></div>';
    }

    html += '</form></div></div>';
    bootbox.dialog({
        title: "New feature attributes",
        message: html,
        buttons: {
            success: {
                label: "Ok",
                className: "btn-success",
                callback: function () {
                    for (var i = 0; i < attributes.length; i++) {
                        var value = $("#new-layer-field-value-" + attributes[i]).val();
                        feature.set(attributes[i], value);
                    }
                }
            }
        }
    });

}