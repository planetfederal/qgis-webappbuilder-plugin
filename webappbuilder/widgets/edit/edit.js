var showEditPanel = function(){

    var select = document.getElementById('edit-layer');
    if (select.options.length === 0){
        var populateLayers = function(){
            $("#edit-layer").empty();
            for (var i = 0, lay; i < getVectorLayers().length; i++) {
                lay = getVectorLayers()[i];
                var coll = sourceFromLayer(lay).getFeaturesCollection();
                if (coll){
                    var option = document.createElement('option');
                    option.value = option.textContent = lay.get('title');
                    select.appendChild(option);
                }
            }
        };
        populateLayers();
        select.onchange = function(e) {
            enableEditTool();
        };
        map.getLayers().on("change:length", populateLayers);
    }

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
        if (currentInteraction instanceof ol.interaction.Draw){
            toggleEdit.className = "btn btn-default";
            disableEditTool();
        }
        else{
            var layerName = document.getElementById('edit-layer').value;
            var layer = getLayerFromLayerName(layerName);
            if (layer){
                toggleEdit.className = "btn btn-primary"
                enableEditTool();
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
            '<div class="form-inline"> ' +
            '<label class="col-md-6 control-label" for="new-layer-name"> Layer name </label>'+
            '<div class="col-md-4"> <input id="new-layer-name" type="text" class="form-control input-md">' +
            '</div></div>'+
            '<div class="form-inline"> ' +
            '<label class="col-md-6 control-label" for="geom-type-dropdown"> Geometry type</label> ' +
            '<div class="col-md-4">' +
            '<select class="form-control" id="geom-type-dropdown">'+
            '<option>Point</option>'+
            '<option>LineString</option>'+
            '<option>Polygon</option>'+
            '</select></div></div>' +
            '<div class="form-inline"> ' +
            '<label class="col-md-6 control-label" for="new-layer-fields"> Attributes </label>'+
            '<div class="col-md-4"> <input id="new-layer-fields" type="text" class="form-control input-md">' +
            '</div></div>'+
            '</form></div></div>';

    bootbox.dialog({
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
                    _createEmptyLayer(title, type, attributes)
                }
            }
        }
    });
};

var _createEmptyLayer = function(title, type, attributes){

    var layer = new ol.layer.Vector({
        title: title,
        geomType: type,
        schema: attributes,
        isSelectable: true,
        isRemovable: true,
        source: new ol.source.Vector({features: new ol.Collection()}),
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

    map.addLayer(layer);

};

var disableEditTool = function(){
    map.removeInteraction(currentInteraction);
    currentInteraction = null;
}

var enableEditTool = function(){

    var layerName = document.getElementById('edit-layer').value;
    var layer = getLayerFromLayerName(layerName);
    var geomType = layer.get("geomType")
    var schema;
    if (geomType){
        schema = layer.get("schema")
    }
    else{
        var source = sourceFromLayer(layer);
        var geom = source.getFeatures()[0].getGeometry()
        if (geom instanceof ol.geom.Point || geom instanceof ol.geom.Point){
            geomType = "Point";
        }
        else if (geom instanceof ol.geom.LineString || geom instanceof ol.geom.MultiLineString){
            geomType = "LineString";
        }
        else if (geom instanceof ol.geom.Polygon || geom instanceof ol.geom.MultiPolygon){
            geomType = "Polygon";
        }

        //TODO
    }

    if (currentInteraction){
        map.removeInteraction(currentInteraction);
        currentInteraction = null;
    }

    var editInteraction = new ol.interaction.Draw({
                                    features: layer.getSource().getFeaturesCollection(),
                                    type: geomType});

    map.addInteraction(editInteraction);
    currentInteraction = editInteraction;

}