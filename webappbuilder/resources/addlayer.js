
var addLayerFromFile = function(){

    var readFeatures = function(text){
        var formats = [new ol.format.GeoJSON(), new ol.format.KML(), new ol.format.GPX()]
        for(var i=0, len=formats.length; i< len; i++){
            var format = formats[i];
            try {
                var crs = format.readProjection(text);
                var features = format.readFeatures(text,
                        {dataProjection: crs.getCode(),
                        featureProjection: map.getView().getProjection().getCode()});
                return features;
            } catch (e) {}
        }
        return null;
    }

    var _addLayerFromFile = function(f){
        if (f) {
            var r = new FileReader();
            r.onload = function(e) {
                var contents = e.target.result;
                var features = readFeatures(contents);
                if (features){
                    var lyr = new ol.layer.Vector({
                        source:  new ol.source.Vector({
                                    features: features
                                }),
                        title: f.name,
                        isRemovable: true,
                        isSelectable: true
                    });
                    map.addLayer(lyr);
                }
                else{
                    $("html").css("cursor", "default");
                    alert("Failed to load file");
                }
            }
            r.readAsText(f);
        } else {
            alert("Failed to load file");
        }
    };

    var input = document.createElement('input');
    input.type = "file";
    input.accept=".geojson, .gpx, .kml"
    $(input).on("change", function(){
        var filename = input.files[0];
        busyProcess(function(){_addLayerFromFile(filename)}, 500);
        ;
    });
    $(input).trigger('click');

    return false;

};
