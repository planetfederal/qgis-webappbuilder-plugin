
var geocodingStyle = new ol.style.Style({
  image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
    anchor: [0.5, 46],
    anchorXUnits: 'fraction',
    anchorYUnits: 'pixels',
    opacity: 0.75,
    src: './resources/marker.png'
  }))
});
var geocodingSource = new ol.source.Vector({});
var geocodingLayer = new ol.layer.Vector({
  source: geocodingSource
});

searchAddress = function(){
    var inp = document.getElementById("geocoding-search");
    if (inp.value === ""){
        document.getElementById('geocoding-results').style.display = 'none';
        return;
    }
    $.getJSON('http://nominatim.openstreetmap.org/search?format=json&limit=5&q=' + inp.value, function(data) {
        var items = [];

        $.each(data, function(key, val) {
            bb = val.boundingbox;
            items.push("<li><a href='#' onclick='goToAddress(" + bb[0] + ", " + bb[2] + ", " + bb[1] + ", " + bb[3]
                        + ", \"" + val.osm_type + "\");return false;'>" + val.display_name + '</a></li>');
        });

        $('#geocoding-results').empty();
        if (items.length !== 0) {
            $('<ul/>', {
                html: items.join('')
            }).appendTo('#geocoding-results');
        } else {
            $('<p>', { html: "No results found" }).appendTo('#geocoding-results');
        }
        document.getElementById('geocoding-results').style.display = 'block';
    });
};

goToAddress = function(lat1, lng1, lat2, lng2, osm_type) {
    document.getElementById('geocoding-results').style.display = 'none';
    var pos = ol.proj.transform([lng1, lat1], 'EPSG:4326', map.getView().getProjection().getCode());
    map.getView().setCenter(pos);
    map.getView().setZoom(10);
    var feat = new ol.Feature({
      geometry: new ol.geom.Point(pos),
    });
    feat.setStyle(geocodingStyle);
    geocodingSource.clear();
    geocodingSource.addFeature(feat);
    map.removeLayer(geocodingLayer);
    map.addLayer(geocodingLayer);
};

searchBoxKeyPressed = function(e){
    e = e || window.event;
    if (e.keyCode == 13){
        searchAddress();
    }
};

