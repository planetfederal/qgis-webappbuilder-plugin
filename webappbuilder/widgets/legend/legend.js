
ol.control.Legend = function(opt_options) {

    var options = opt_options || {};

    var tipLabel = options.tipLabel ? options.tipLabel : 'Legend';

    this.expandOnHover = options.expandOnHover === true;
    this.showExpandedOnStartup = options.showExpandedOnStartup === true;

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

    if (options.expandOnHover){
        element.onmouseover = function(e) {
            this_.showPanel();
        };
        element.onmouseout = function(e) {
            e = e || window.event;
            if (!element.contains(e.toElement)) {
                this_.hidePanel();
            }
        };
    }
    else{
        button.onclick = function(e) {
            if (this_.element.className != this_.shownClassName) {
                this_.showPanel();
            }
            else{
                this_.hidePanel();
            }
        };
    }

    ol.control.Control.call(this, {
        element: element,
        target: options.target
    });

    if (options.showExpandedOnStartup){
        this.showPanel();
    }

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
        var symbols = legendData[name];
        for (var i = 0; i < symbols.length; i++){
            element += "<li><img src='./legend/" + symbols[i][1] + "'>" + symbols[i][0] + "</li>";
        }
        element += " </li>";
        list.append(element);
    }
};

ol.control.Legend.prototype.setMap = function(map) {
    ol.control.Control.prototype.setMap.call(this, map);
    if (map) {
        map.getLayers().on("change:length", this.renderPanel);
    }
    if (this.showExpandedOnStartup){
        this.renderPanel();
    }
};