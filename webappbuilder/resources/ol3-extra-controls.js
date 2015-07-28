ol.control.CesiumControl = function(ol3d) {

  var button = document.createElement('button');
  button.innerHTML = '3D';

  var enable3DView = function(e) {
    if (ol3d.getEnabled()){
        ol3d.setEnabled(false);
        button.innerHTML = '3D';
    }
    else{
        button.innerHTML = '2D';
        ol3d.setEnabled(true);
    }
  };

  button.addEventListener('click', enable3DView, false);
  button.addEventListener('touchstart', enable3DView, false);

  var element = document.createElement('div');
  element.className = 'enable3d-control ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element
  });

};
ol.inherits(ol.control.CesiumControl, ol.control.Control);



//=======================================================
ol.control.HomeButton = function(opt_options) {

  var options = opt_options || {};

  var button = document.createElement('button');
  button.innerHTML = '<i class="glyphicon glyphicon-home"></i>';

  var this_ = this;
  var goHome = function(e) {
    map.getView().fit(originalExtent, map.getSize());
  };

  button.addEventListener('click', goHome, false);
  button.addEventListener('touchstart', goHome, false);

  var element = document.createElement('div');
  element.className = 'home-button ol-unselectable ol-control';
  element.appendChild(button);

  ol.control.Control.call(this, {
    element: element,
    target: options.target
  });

};
ol.inherits(ol.control.HomeButton, ol.control.Control);

//=======================================================

ol.control.Geolocation = function() {

    this_ = this;
    geolocate = function(){
        if (this_.geolocation){
            if (this_.geolocation.getTracking()){
                this_.getMap().removeOverlay(this_.marker)
                this_.geolocation.setTracking(false)
            }
            else{
                this_.getMap().addOverlay(this_.marker)
                this_.geolocation.setTracking(true)
                view.setCenter(this_.geolocation.getPosition());
            }
        }
        else{
            var view = this_.getMap().getView();
            this_.geolocation = new ol.Geolocation({
                    projection: view.getProjection(),
                    tracking: true
            });
            view.setCenter(this_.geolocation.getPosition());
            this_.geolocation.on('change', function(evt) {
                view.setCenter(this_.geolocation.getPosition());
            });
            this_.marker = new ol.Overlay({
                element: /** @type {Element} */ ($('<i/>').addClass('icon-flag').get(0)),
                positioning: 'bottom-left',
                stopEvent: false
            });
            this_.marker.bindTo('position', this_.geolocation);
            this_.getMap().addOverlay(this_.marker);
        }
    };
    var button = document.createElement('button');

    button.addEventListener('click', geolocate, false);
    button.addEventListener('touchstart', geolocate, false);

    var element = document.createElement('div');
    element.className = 'geolocation-control ol-unselectable ol-control';
    element.appendChild(button);

    ol.control.Control.call(this, {
      element: element,
    });

};
ol.inherits(ol.control.Geolocation, ol.control.Control);


//====================================================


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
    var name = layer.get('title');
    if (name){
        var div = "<li data-layerid='" + name + "'>";
        if (layer instanceof ol.layer.Group){
            name = "<b>" + name + "</b>";
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
            if (layer.get("type") != "base" && this.showZoomTo){
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
            var layers = layer.getLayers().getArray()
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



//====================================================

ol.control.Legend = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ?
      options.tipLabel : 'Legend';

    this.hiddenClassName = 'ol-unselectable ol-control legend';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName;

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    this.panel = document.createElement('div');
    this.panel.className = 'legend-panel';
    this.panel.id = "legend";
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

ol.inherits(ol.control.Legend, ol.control.Control);

ol.control.Legend.prototype.showPanel = function() {
    if (this.element.className != this.shownClassName) {
        this.element.className = this.shownClassName;
            this.renderPanel();
    }
};

ol.control.Legend.prototype.hidePanel = function() {
    if (this.element.className != this.hiddenClassName) {
        this.element.className = this.hiddenClassName;
    }
};

ol.control.Legend.prototype.renderPanel = function() {
    var map = this.getMap();
    this_ = this;
    $('#legend').empty();
    var list = $('<ul/>').appendTo('#legend');
    list.addClass("expandableList");
    for (var name in legendData){
        var element = "<li><label for='legend-layer-"+ name +"'>" + name +
            "</label><input type='checkbox' checked id='legend-layer-" + name + "' /><ul> ";
        var groups = legendData[name];
        for (var group in groups){
            element += "<li><img src='./legend/" + groups[group] + "'>" + group + "</li>";
        }
        element += " </li>";
        list.append(element);
    }
};

//=======================================================
ol.control.TimeLine = function(opt_options) {

    var options = opt_options || {minDate: 0, maxDate:1, interval:1, numIntervals:2};

    var element = document.createElement('div');
    element.className = "timeline ol-control";

    var ul = document.createElement('ul');

    var li = document.createElement('li');
    this.button = document.createElement("button");
    this.button.innerHTML = '<i class="glyphicon glyphicon-play"></i>';
    this.button.setAttribute("id", "timelineButton");
    var this_ = this;
    this.button.onclick = function(){
        if (this.innerHTML == '<i class="glyphicon glyphicon-play"></i>'){
            this.innerHTML = '<i class="glyphicon glyphicon-pause"></i>';
            this.autoplayTimer = setInterval(this_.autoplay, options.interval);
        }
        else{
            this.innerHTML = '<i class="glyphicon glyphicon-play"></i>';
            clearInterval(this.autoplayTimer);
        }
    };
    li.appendChild(this.button);
    ul.appendChild(li);

    var li2 = document.createElement('li');
    this.range = document.createElement("input");
    this.range.setAttribute("type", "range");
    this.range.setAttribute("id", "timelineRange");
    li2.appendChild(this.range);
    ul.appendChild(li2);

    var li3 = document.createElement('li');
    this.date = document.createElement("input");
    this.date.setAttribute("type", "date");
    this.date.setAttribute("required", "required");
    this.date.setAttribute("id", "timelineDate");
    li3.appendChild(this.date);
    ul.appendChild(li3);

    var minDateMilli = options.minDate;
    var maxDateMilli = options.maxDate;

    currentTimelineTime = minDateMilli;

    this.range.setAttribute("min", minDateMilli);
    this.range.setAttribute("max", maxDateMilli);
    this.range.setAttribute("value", minDateMilli);

    var minDate = new Date(minDateMilli);
    minDate = minDate.getFullYear().toString() + "-" + (minDate.getMonth() + 1).toString()
                + "-" + (minDate.getDate() + 1).toString();
    var maxDate = new Date(minDateMilli);
    maxDate = maxDate.getFullYear().toString() + "-" + (maxDate.getMonth() + 1).toString()
                + "-" + (maxDate.getDate() + 1).toString();
    this.date.setAttribute("min", minDate);
    this.date.setAttribute("max", maxDate);
    this.date.valueAsNumber = this.range.valueAsNumber;

    var this_ = this;
    this.range.onchange = function() {
        this_.date.valueAsNumber = this_.range.valueAsNumber;
        currentTimelineTime = this_.range.valueAsNumber;
        this_.refreshTimeLayers();
    };

    this.date.onchange = function() {
        this_.range.valueAsNumber = this_.date.valueAsNumber;
        currentTimelineTime = this_.range.valueAsNumber;
        this_.refreshTimeLayers();
    };

    autoplayInterval = (maxDateMilli - minDateMilli) / options.numIntervals;
    this.autoplay = function(){
        var newTime = this_.range.valueAsNumber + autoplayInterval;
        if (newTime > maxDateMilli){
            newTime = minDateMilli;
        }
        this_.range.valueAsNumber = newTime;
        this_.date.valueAsNumber = newTime
        currentTimelineTime = newTime;
        this_.refreshTimeLayers();
    }

    element.appendChild(ul);

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });
};
ol.inherits(ol.control.TimeLine, ol.control.Control);

ol.control.TimeLine.prototype.setMap = function(map) {
    ol.control.Control.prototype.setMap.call(this, map);
    this.refreshTimeLayers();
};

ol.control.TimeLine.prototype.refreshTimeLayers = function() {
    var map = this.getMap();
    if (map){
        var layers = map.getLayerGroup().getLayers().getArray();
        for(var i=0,len=layers.length; i<len; i++){
            var layer = layers[i];
            if (layer.getLayers){
                var groupLayers = layer.getLayers().getArray();
                for(var j=0,groupLen=groupLayers.length; j<groupLen; j++){
                    var groupLayer = groupLayers[j];
                    var timeInfo = groupLayer.get('timeInfo');
                    if (timeInfo){
                        groupLayer.getSource().changed();
                    }
                }
            }
            else{
                var timeInfo = layer.get('timeInfo');
                if (timeInfo){
                    layer.getSource().changed();
                }
            }
        }
    }
};

