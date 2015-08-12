
ol.control.Geolocation = function() {

    this_ = this;
    geolocate = function(){
        if (this_.geolocation){
            if (this_.geolocation.getTracking()){
                this_.getMap().removeOverlay(this_.marker);
                this_.geolocation.setTracking(false);
            }
            else{
                this_.getMap().addOverlay(this_.marker);
                this_.geolocation.setTracking(true);
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
