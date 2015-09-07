
ol.control.Geolocation = function() {

    var this_ = this;
    var geolocate = function(){
        var view = this_.getMap().getView();
        if (this_.geolocation){
            if (this_.geolocation.getTracking()){
                this_.getMap().removeOverlay(this_.marker);
                this_.geolocation.setTracking(false);
            }
            else{
                var pos = this_.geolocation.getPosition();
                this_.getMap().addOverlay(this_.marker);
                this_.geolocation.setTracking(true);
                view.setCenter(pos);
                this_.marker.setPosition(pos);
            }
        }
        else{
            this_.geolocation = new ol.Geolocation({
                    projection: view.getProjection(),
                    tracking: true
            });
            var pos = this_.geolocation.getPosition();
            view.setCenter(pos);
            this_.marker = new ol.Overlay({
                element: $('<i/>').addClass('icon-flag').get(0),
                positioning: 'bottom-left',
                stopEvent: false
            });
            this_.marker.setPosition(pos);
            this_.geolocation.on('change:position', function() {
                var pos = this_.geolocation.getPosition();
                this_.marker.setPosition(pos);
                view.setCenter(pos);
            });
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
