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


/*
Adapted from https://github.com/walkermatt/ol3-layerswitcher (c) Matt Walker.
And https://github.com/acanimal/thebookofopenlayers3 (c) Antonio Santiago
*/
ol.control.LayerSwitcher = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
      options.tipLabel : 'Layers list';

    this.showOpacity = options.showOpacity === true;
    this.showDownload = options.showDownload === true;
    this.showZoomTo = options.showZoomTo === true;
    this.allowReordering = options.allowReordering === true;
    this.allowFiltering = options.allowFiltering === true;

    this.hiddenClassName = 'ol-unselectable ol-control layer-switcher';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName;

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    this.panel = document.createElement('div');
    this.panel.className = 'layer-tree-panel';
    this.panel.id = "layertree";
    element.appendChild(this.panel);

    var this_ = this;
    element.onmouseover = function(e) {
        this_.showPanel();
    };
    button.onclick = function(e) {
        this_.showPanel();
    };
    element.onmouseout = function(e) {
        e = e || window.event;
        if (!element.contains(e.toElement)) {
            this_.hidePanel();
        }
    };

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });

};

ol.inherits(ol.control.LayerSwitcher, ol.control.Control);

ol.control.LayerSwitcher.prototype.showPanel = function() {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
            this.renderPanel();
    }
};

ol.control.LayerSwitcher.prototype.hidePanel = function() {
    if (this.element.className != this.hiddenClassName) {
        this.element.className = this.hiddenClassName;
    }
};


ol.control.LayerSwitcher.prototype.renderPanel = function() {
    var map = this.getMap();
    this_ = this;
    $('#layertree').empty();
    var list = $('<ul/>').appendTo('#layertree');
    var layers = map.getLayerGroup().getLayers().getArray();
    var len = layers.length;
    for (var i = len -1; i >=0; i--){
        list.append(this.buildLayerTree(layers[i]), false);
    }
    function indexOf(layers, layer) {
        var length = layers.getLength();
        for (var i = 0; i < length; i++) {
            if (layer === layers.item(i)) {
                return i;
            }
        }
        return -1;
    }
    var findBy = function(layer, value) {
        var name = layer.get('title');
        if (name === value) {
            return layer;
        }
        if (layer.getLayers) {
            var layers = layer.getLayers().getArray();
            var len = layers.length, result;
            for (var j = 0; j < len; j++) {
                result = findBy(layers[j], value);
                if (result) {
                    return result;
                }
            }
        }
        return null;
    };

    if (this.showOpacity){
        $('input.opacity').slider().on('slide', function(ev) {
            var layername = $(this).closest('li').data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            layer.setOpacity(ev.value);
        });
    }
    if (this.showZoomTo){
        $('.layer-zoom-to').on('click', function() {
            var layername = $(this).closest('li').data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            map.getView().fit(layer.getSource().getExtent(), map.getSize());
        });
    }
    if (this.showDownload){
        $('.layer-download').on('click', function() {
            var layername = $(this).closest('li').data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            var geojson = new ol.format.GeoJSON();
            var features = layer.getSource().getFeatures();
            var json = geojson.writeFeatures(features);
            var dl = document.createElement('a');
            dl.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(json));
            dl.setAttribute('download', layername + '.geojson');
            dl.click();
        });
    }
    if (this.allowReordering){
        $('.layer-move-up').on('click', function() {
            var li = $(this).closest('li');
            var layername = li.data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            var layers = map.getLayers();
            var index = indexOf(layers, layer);
            if (index < layers.getLength() - 1) {
                var next = layers.item(index + 1);
                layers.setAt(index + 1, layer);
                layers.setAt(index, next);
                li.prev().before(li);
            }
        });
        $('.layer-move-down').on('click', function() {
            var li = $(this).closest('li');
            var layername = li.data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            var layers = map.getLayers();
            var index = indexOf(layers, layer);
            if (index > 1) {
                var prev = layers.item(index - 1);
                layers.setAt(index - 1, layer);
                layers.setAt(index, prev);
                li.next().after(li);
            }
        });
    }
    $('.layer-check').on('click', function() {
        var layername = $(this).closest('li').data('layerid');
        var layer = findBy(map.getLayerGroup(), layername);
        layer.setVisible(!layer.getVisible());
        $(this).checked = layer.getVisible();
    });
    $('.layer-remove').on('click', function() {
        var layername = $(this).closest('li').data('layerid');
        var layer = findBy(map.getLayerGroup(), layername);
        map.removeLayer(layer);
        this_.renderPanel();
    });
    $('.layer-set-filters').on('click', function() {
        var layername = $(this).closest('li').data('layerid');
        var layer = findBy(map.getLayerGroup(), layername);
        editLayerFilters(layer);
    });

};


ol.control.LayerSwitcher.prototype.buildLayerTree = function(layer, isInGroup) {
    var elem;
    var view = this.getMap().getView();
    var name = layer.get('title');
    if (name){
        var div = "<li data-layerid='" + name + "'>";
        if (layer instanceof ol.layer.Group){
            name = "<b>" + name + "</b>";
        }
        else if (layer.getMinResolution() > view.getResolution() ||
                layer.getMaxResolution() < view.getResolution()){
            name = "<font color='#bbbbbb'>" + name + "</font>";
        }

        if (layer.getVisible()){
            div += "<input class='layer-check' type='checkbox' checked>" + name;
        }
        else{
            div += "<input class='layer-check' type='checkbox'>" + name;
        }
        if (this.showOpacity){
            div += "<input style='width:80px;' class='opacity' type='text' data-slider-value='" + layer.getOpacity().toString()
                 + "' data-slider-min='0' data-slider-max='1' data-slider-step='0.1' data-slider-tooltip='hide'>";
        }
        if (!(layer instanceof ol.layer.Group)){
            if (!(layer instanceof ol.layer.Tile) && this.showZoomTo){
                div += "<a title='Zoom to layer' href='#' style='padding-left:15px;' href='#'><i class='layer-zoom-to glyphicon glyphicon-zoom-in'></i></a>";
            }
            if (layer instanceof ol.layer.Vector && this.showDownload){
                div += "<a title='Download layer' href='#' style='padding-left:15px;'><i class='layer-download glyphicon glyphicon-download-alt'></i></a>";
            }
            if (layer instanceof ol.layer.Vector && this.allowFiltering){
                div += "<a title='Filter layer' href='#' style='padding-left:15px;'><i class='layer-set-filters glyphicon glyphicon-filter'></i></a>";
            }
        }
        if (layer.get("type") != "base" && this.allowReordering && !isInGroup){
            div += "<a title='Move up' href='#' style='padding-left:15px;' href='#'><i class='layer-move-up glyphicon glyphicon-triangle-top'></i></a>";
            div += "<a title='Move dowm' href='#' style='padding-left:15px;' href='#'><i class='layer-move-down glyphicon glyphicon-triangle-bottom'></i></a>";
        }
        if (layer.get("isRemovable")){
            div += "<a title='Remove' href='#' style='padding-left:15px;' href='#'><i class='layer-remove glyphicon glyphicon-remove'></i></a>";
        }

        if (layer.getLayers && layer.get("showContent")) {
            var sublayersElem = '';
            var layers = layer.getLayers().getArray();
            var len = layers.length;
            for (var i = len - 1; i >= 0; i--) {
                sublayersElem += this.buildLayerTree(layers[i], true);
            }
            elem = div + " <ul>" + sublayersElem + "</ul></li>";
        } else {
            elem = div + " </li>";
        }
    }
    else{
        elem = "";
    }
    return elem;
};

