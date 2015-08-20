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

var getTileLayers = function(){
    var allLayers = getAllNonBaseLayers();
    var tileLayers = [];
    var len = allLayers.length;
    for (var i = 0; i < len; i++){
        var s= allLayers[i].getSource();
        if (s instanceof ol.source.TileWMS){
            tileLayers.push(allLayers[i]);
        }
    }
    return tileLayers;
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

    this.clearSelection = function(layer){
        layer.selectedFeatures = [];
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

var currentInteractions;

var removeInteractions = function(){

    if (currentInteractions){
        for (var i = 0; i < currentInteractions.length; i++){
            map.removeInteraction(currentInteractions[i]);
        }
        currentInteractions = null;
    }

};