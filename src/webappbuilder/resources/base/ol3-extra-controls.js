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
ol.control.HomeButton = function(opt_options) {

  var options = opt_options || {};

  var button = document.createElement('button');
  button.innerHTML = '<i class="glyphicon glyphicon-home"></i>';

  var this_ = this;
  var goHome = function(e) {
    map.getView().fitExtent(originalExtent, map.getSize());
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
    }
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
    this.showGroupContent = options.showGroupContent === true;

    this.firstTime = true;

    this.hiddenClassName = 'ol-unselectable ol-control layer-switcher';
    this.shownClassName = this.hiddenClassName + ' shown';

    var element = document.createElement('div');
    element.className = this.hiddenClassName;

    var button = document.createElement('button');
    button.setAttribute('title', tipLabel);
    element.appendChild(button);

    this.panel = document.createElement('div');
    this.panel.className = 'layer-tree-panel';
    this.panel.id = "layertree"
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
        if (this.firstTime){
            this.renderPanel();
            this.firstTime = false;
        }

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
    $('#layertree').empty()
    var list = $('<ul/>').appendTo('#layertree');
    var layers = map.getLayerGroup().getLayers().getArray();
    var len = layers.length;
    for (var i = len -1; i >=0; i--){
        list.append(this.buildLayerTree(layers[i]), false)
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
        name = layer.get('title')
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
            map.getView().fitExtent(layer.getSource().getExtent(), map.getSize());
        });
    }
    if (this.showDownload){
        $('.layer-download').on('click', function() {
            var layername = $(this).closest('li').data('layerid');
            var layer = findBy(map.getLayerGroup(), layername);
            var geojson = new ol.format.GeoJSON;
            var features = layer.getSource().getFeatures();
            var json = geojson.writeFeatures(features);
            var dl = document.createElement('a');
            dl.setAttribute('href', 'data:text/json;charset=utf-8,' + encodeURIComponent(content));
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
        if (layer.getVisible()) {
            $(this).removeClass('glyphicon-unchecked').addClass('glyphicon-check');
        } else {
            $(this).removeClass('glyphicon-check').addClass('glyphicon-unchecked');
        }
    });

};


ol.control.LayerSwitcher.prototype.buildLayerTree = function(layer, isInGroup) {
    var elem;
    var name = layer.get('title');
    if (name){
        var div = "<li data-layerid='" + name + "'>";
        if (layer instanceof ol.layer.Group){
            name = "<b>" + name + "</b>"
        }
        div += "<span><i class='layer-check glyphicon glyphicon-check'></i> " + name + "</span>";
        if (!(layer instanceof ol.layer.Group)){
            if (this.showOpacity){
                div += "<input style='width:80px;' class='opacity' type='text' value='' data-slider-min='0' data-slider-max='1' data-slider-step='0.1' data-slider-tooltip='hide'>";
            }
            if (layer.get("type") != "base" && this.showZoomTo){
                div += "<a title='Zoom to layer' href='#' style='padding-left:15px;' href='#'><i class='layer-zoom-to glyphicon glyphicon-zoom-in'></i></a>";
            }
            if (layer instanceof ol.layer.Vector && this.showDownload){
                div += "<a title='Download layer' href='#' style='padding-left:15px;'><i class='layer-download glyphicon glyphicon-download-alt'></i></a>";
            }
        }
        if (layer.get("type") != "base" && this.allowReordering && !isInGroup){
            div += "<a title='Move up' href='#' style='padding-left:15px;' href='#'><i class='layer-move-up glyphicon glyphicon-triangle-top'></i></a>";
            div += "<a title='Move dowm' href='#' style='padding-left:15px;' href='#'><i class='layer-move-down glyphicon glyphicon-triangle-bottom'></i></a>";
        }

        if (layer.getLayers && this.showGroupContent) {
            var sublayersElem = '';
            var layers = layer.getLayers().getArray(),
                    len = layers.length;
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
}


