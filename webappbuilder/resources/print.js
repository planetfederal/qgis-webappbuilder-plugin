var printMap = function(layoutName){

    var html = '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal"> '

    var layout = printLayouts[layoutName].elements;

    for (var i = 0; i < layout.length; i++) {
        if (layout[i].type === "label"){
            html += '<div class="form-inline"> ' +
                    '<label class="col-md-6 control-label"' +
                    '" for="layout-label-' + layout[i].name +'">' + layout[i].name +'</label> ' +
                    '<div class="col-md-4"> <input id="layout-label-' + layout[i].name +'" name="' + layout[i].name +
                    '" type="text" class="form-control input-md"> </div></div>';
        }
    }

    html += '<div class="form-inline"> ' +
            '<label class="col-md-6 control-label" for="resolution-dropdown"> Resolution</label> ' +
            '<div class="col-md-4">' +
            '<select class="form-control" id="resolution-dropdown">'+
            '<option>72</option>'+
            '<option>150</option>'+
            '<option>300</option>'+
            '</select></div></div>'

    html += '</form></div></div>';
    bootbox.dialog({
        title: "Print map",
        message: html,
        buttons: {
            success: {
                label: "Print",
                className: "btn-success",
                callback: function () {
                    var resolution = $("#resolution-dropdown").val();
                    var labels = {};
                    for (var i = 0; i < layout.length; i++) {
                        if (layout[i].type === "label"){
                            labels[layout[i].name] = $("#layout-label-" + layout[i].name).val();
                        }
                    }
                    createMap(layoutName, resolution, labels)
                }
            }
        }
    });

}

var createMap = function(layoutName, resolution, labels){
    var layout = printLayouts[layoutName];
    var layoutSafeName = layoutName.replace(/[^a-z0-9]/gi,'').toLowerCase();
    var elements = layout.elements;
    var pdf = new jsPDF('landscape', "mm", [layout.width, layout.height]);
    var images = [];
    var elementsLoaded = 0;
    var elementLoaded = function(){
        elementsLoaded++;
        if (elementsLoaded == elements.length){
            pdf.save('map.pdf');
        }
    };
    var size = (map.getSize());
    var extent = map.getView().calculateExtent(size);
    var tileLayers = getTileLayers();
    var tiledLayersLoaded = 0;
    var mapElement = null;
    var _canvas = null;
    var paintMapInPdf = function(){
        var data = _canvas.toDataURL('image/jpeg');
        pdf.rect(mapElement.x, mapElement.y, mapElement.width, mapElement.height);
        pdf.addImage(data, 'JPEG', mapElement.x, mapElement.y, mapElement.width, mapElement.height);
        map.setSize(size);
        map.getView().fit(extent, size);
        map.renderSync();
        elementLoaded();
    };
    var tileLayerLoaded= function(){
        tiledLayersLoaded++;
        if (tiledLayersLoaded == tileLayers.length){
           paintMapInPdf();
        }
    };
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        if (element.type === "label"){
            var labelElement = element;
            pdf.setFontSize(labelElement.size)
            pdf.text(labelElement.x, labelElement.y + labelElement.size / 25.4, labels[labelElement.name])
            elementLoaded();
        }
        else if (element.type === "map"){
            mapElement = element;
            var width = Math.round(mapElement.width * resolution / 25.4);
            var height = Math.round(mapElement.height * resolution / 25.4);
            map.once('postcompose', function(event) {
                _canvas = event.context.canvas;
                var sources = [];
                var loaded = [];
                var loading = [];
                for (var j = 0; j < tileLayers.length; j++){
                    (function(idx){
                        source[idx] = tileLayers[idx].getSource();
                        loading[idx] = 0;
                        loaded[idx] = 0;
                        sources[idx].on('tileloadstart', function() {
                            ++loading;
                        });
                        sources[idx].on('tileloadend', function() {
                            ++loaded;
                            if (loading === loaded) {
                                tileLayerLoaded();
                            }
                        });
                        sources[idx].on('tileloaderror', function() {
                            ++loaded;
                        });
                    })(j);
                }
            });
            map.setSize([width, height]);
            map.getView().fit(extent, (map.getSize()));
            map.renderSync();
            if (tileLayers.length == 0){
               paintMapInPdf();
            }
        }
        else if (element.type === "shape" || element.type === "arrow" ||
                    element.type === "legend" || element.type === "scalebar"){
            (function(el){
                images[el.id] = new Image();
                images[el.id].crossOrigin = "anonymous";
                images[el.id].addEventListener('load', function() {
                    pdf.addImage(images[el.id], 'png', el.x, el.y, el.width, el.height);
                    elementLoaded();
                });
                images[el.id].src = "print/" + layoutSafeName + "_" + el.id + "_" +
                                    resolution.toString() + ".png";
            })(element);
        }
        else if (element.type === "picture"){
            (function(el){
                images[el.id] = new Image();
                images[el.id].crossOrigin = "anonymous";
                images[el.id].addEventListener('load', function() {
                    pdf.addImage(images[el.id], 'png', el.x, el.y, el.width, el.height);
                    elementLoaded();
                });
                images[el.id].src = "print/" + el.file;
            })(element);
        }
        else{
            elementLoaded();
        }

    }
};