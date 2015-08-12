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

