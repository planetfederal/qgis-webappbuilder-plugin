/*********Helper functions***************/


var getTurfGeoJsonFromOL3LayerName = function(name){

    features = getFeaturesFromLayerName(name);
    geoj =  new ol.format.GeoJSON().writeFeatures(features,
                        {featureProjection: map.getView().getProjection().getCode(),
                        dataProjection: EPSG4326})
    return JSON.parse(geoj);

};

var createAndAddLayer = function(layerData, title, epsg, isSelectable){

    crsid = epsg || map.getView().getProjection().getCode();
    if (typeof(isSelectable)==='undefined') isSelectable = true;
    if (!(layerData instanceof ol.source.Vector)){
        layerData = new ol.source.Vector({
            features: new ol.format.GeoJSON().readFeatures(layerData,
                {dataProjection: crsid,
                featureProjection: map.getView().getProjection().getCode()}),
        });
    }

    var lyr = new ol.layer.Vector({
        source: layerData,
        title: title,
        isRemovable: true,
        isSelectable: isSelectable
    });

    addLayer(lyr);
};

var addLayer = function(layer){

    map.addLayer(layer);

}


var runAlgorithm = function(alg){

    var params = alg.getParameters();
    var parametersHtml = '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal"> ';
    for (var paramName in params) {
        if (params.hasOwnProperty(paramName)) {
            paramProperties = params[paramName];

            parametersHtml += '<div class="form-inline"> ' +
                    '<label class="col-md-6 control-label"' +
                    '" for="' + paramName +'">' + paramProperties.description +'</label> '
            if (paramProperties.type == PARAMETER_LAYER){
                var options = "";
                var selectableLayersList = getSelectableLayers();
                for (var i = 0, l; i < selectableLayersList.length; i++) {
                    l = selectableLayersList[i];
                    var title = l.get('title')
                    if (title){
                        options += '<option>' + title + '</option>';
                    }
                }
                parametersHtml += '<div class="col-md-4"><select class="form-control" id="' +
                            paramName + '">' + options + '</select></div>'
            }
            else if (paramProperties.type == PARAMETER_FLOAT
                    || paramProperties.type == PARAMETER_INTEGER){
                parametersHtml += '<div class="col-md-4"> <input id="' + paramName +'" value="' +
                    paramProperties.defaultValue + '" name="' + paramName +
                    '" type="number" class="form-control input-md"> </div>'
            }
            else if (paramProperties.type == PARAMETER_FIELD){
                parametersHtml += '<div class="col-md-4"> <input id="' + paramName + '" name="' +
                    paramName +'" type="text" class="form-control input-md"> </div>'
            }
            else if (paramProperties.type == PARAMETER_BOOLEAN){
                parametersHtml += '<div class="col-md-4"> <input id="' + paramName + '" name="' +
                    paramName +'" type="checkbox" class="form-control input-md"> </div>'
            }
            else{
                parametersHtml += '<div class="col-md-4"> <input id="' + paramName +'" value="' +
                    paramProperties.defaultValue + '" name="' + paramName +
                    '" type="text" class="form-control input-md"> </div>';
            }
            parametersHtml += '</div> ';
        }
    }

    parametersHtml += '</form></div></div>';

    bootbox.dialog({
        title: alg.getName(),
        message: parametersHtml,
        buttons: {
            close: {
                label: "Close",
                className: "btn-default",
                callback: function () {
                }
            },
            success: {
                label: "Run",
                className: "btn-success",
                callback: function () {
                    values = {};
                    for (var paramName in params) {
                        if (params.hasOwnProperty(paramName)) {
                            var paramProperties = params[paramName];
                            if (paramProperties.type == PARAMETER_BOOLEAN){
                                values[paramName] = $("#" + paramName).is(":checked");
                            }
                            else{
                                values[paramName] = $("#" + paramName).val();
                            }
                        }
                    }
                    alg.run(values);
                }
            }
        }
    });

};

var showInfoDialog = function(title, body){

    bootbox.dialog({
        title: title,
        message: body,
        buttons: {
            close: {
                label: "Close",
                className: "btn-default",
                callback: function () {
                }
            }
        }
    });

};


var PARAMETER_INTEGER = 0;
var PARAMETER_FLOAT = 1;
var PARAMETER_LAYER = 2;
var PARAMETER_STRING = 3;
var PARAMETER_FIELD = 4;
var PARAMETER_BOOLEAN = 5;

var EPSG4326 = "EPSG:4326"

/*******Algorithms************/

var addRandomLayer = function(){

    this.getName = function(){
        return "Add random layer";
    };

    this.getParameters = function(){
        return {count: {type:PARAMETER_INTEGER,
                        description: "Number of points",
                        defaultValue: 100
                        }
                };
    };

    this.run = function(params){
        bbox = map.getView().calculateExtent(map.getSize());
        var points = turf.random('points', params.count, {
          bbox: bbox
        });
        createAndAddLayer(points, "points")
    };


};

var buffer = function(){

    this.getName = function(){
        return "Buffer";
    };

    this.getParameters = function(){
        return {layer: {type:PARAMETER_LAYER,
                            description:"Buffer elements of layer",
                            },
                distance: {type:PARAMETER_FLOAT,
                            description: "Using a distance of (meters)",
                            defaultValue: 100}
                };
    };

    this.run = function(params){
        var input = getTurfGeoJsonFromOL3LayerName(params.layer);
        var buffered = turf.buffer(input, parseInt(params.distance), "meters");
        createAndAddLayer(buffered, "buffer", EPSG4326);
    };


};

var extractSelected = function(){

    this.getName = function(){
        return "Extract selected features from layer";
    };

    this.getParameters = function(){
        return {layer: {type:PARAMETER_LAYER,
                            description:"Layer to take selected features from",
                            },
                };
    };

    this.run = function(params){
        var source = new ol.source.Vector()
        var layer = getLayerFromLayerName(params.layer);
        var selectedFeatures = selectionManager.getSelection(layer);
        for (i = 0; i < selectedFeatures.length; i++) {
            source.addFeature(selectedFeatures[i]);
        }
        createAndAddLayer(source, "Selection from " + params.layer);
    };

}

var aggregatePoints = function(){

    this.getName = function(){
        return "Aggregate points";
    };

    this.getParameters = function(){
        return {points: {type:PARAMETER_LAYER,
                            description:"Points layer",
                            },
                polygons: {type:PARAMETER_LAYER,
                            description:"Polygons layer",
                            },
                attribute: {type: PARAMETER_STRING,
                            description: "Attribute to aggregate"}

                };
    };

    this.run = function(params){
        var points = getTurfGeoJsonFromOL3LayerName(params.points);
        var polygons = getTurfGeoJsonFromOL3LayerName(params.polygons);
        var attribute = params.attribute;
        var aggregations = [{
                                aggregation: 'sum',
                                inField: attribute,
                                outField: attribute + 'sum'
                              },
                              {
                                aggregation: 'average',
                                inField: attribute,
                                outField: attribute + 'avg'
                              },
                              {
                                aggregation: 'min',
                                inField: attribute,
                                outField: attribute + 'min'
                              },
                              {
                                aggregation: 'max',
                                inField: attribute,
                                outField: attribute + 'max'
                              },
                                {
                                aggregation: 'deviation',
                                inField: attribute,
                                outField: attribute + 'stddev'
                              },
                              {
                                aggregation: 'count',
                                inField: attribute,
                                outField: attribute + 'count'
                              }]
        var aggregated = turf.aggregate(polygons, points, aggregations);
        createAndAddLayer(aggregated, "Aggregated (" + params.points +
                                    " + " + params.polygons + ")", EPSG4326)
    };

}

var addDensityLayer = function(params){

    this.getName = function(){
        return "Density layer (heatmap)";
    };

    this.getParameters = function(){
        return {layer: {type:PARAMETER_LAYER,
                            description:"Vector layer",
                            },
                radius: {type: PARAMETER_INTEGER,
                            description: "Radius",
                            defaultValue: 5
                        }
                };
    };

    this.run = function(params){
        var heatmap = new ol.layer.Heatmap({
            source: getSourceFromLayerName(params.layer),
            radius: 5,
            title: "Density (" + params.layer + ")",
            isRemovable: true
        });
        map.addLayer(heatmap);
    };

}

var selectWithin = function(params){

    this.getName = function(){
        return "Select within";
    };

    this.getParameters = function(){
        return {points: {type:PARAMETER_LAYER,
                            description:"Points layer",
                            },
                polygons: {type:PARAMETER_LAYER,
                            description:"Polygons layer",
                            }
                };
    };

    this.run = function(params){
        var points = getTurfGeoJsonFromOL3LayerName(params.points);
        var polygons = getTurfGeoJsonFromOL3LayerName(params.polygons);
        var selection = turf.within(points, polygons);
        createAndAddLayer(selection, "within (" + params.points +
                                    " in " + params.polygons + ")", EPSG4326)
    };

}

var countFeatures = function(params){

    this.getName = function(){
        return "Count features";
    };

    this.getParameters = function(){
        return {layer: {type: PARAMETER_LAYER,
                        description: "Layer",
                        }
                };
    };

    this.run = function(params){
        var count = getFeaturesFromLayerName(params.layer).length;
        html = "<p><b>Number of features: </b>" + count + "</p>";
        showInfoDialog(this.getName(), html)
    };

}

var lineLength = function(params){

    this.getName = function(){
        return "Compute line length";
    };

    this.getParameters = function(){
        return {lines: {type: PARAMETER_LAYER,
                        description: "Lines Layer",
                        }
                };
    };

    this.run = function(params){
        var length = 0;
        var layerFeatures = getFeaturesFromLayerName(params.lines);
        var format = ol.format.GeoJSON();
        for (var i = 0; i < layerFeatures.length; i++) {
            var line = JSON.parse(format.writeFeature(layerFeatures[i]));
            length += turf.lineDistance(line, "kilometers");
        }

        html = "<p><b>Total length (km): </b>" + lengthcount + "</p>";
        showInfoDialog(this.getName(), html)
    };

}

var nearestPoint = function(params){

    this.getName = function(){
        return "Nearest point";
    };

    this.getParameters = function(){
        return {origin: {type: PARAMETER_LAYER,
                        description: "Origin layer",
                        },
                destination: {type: PARAMETER_LAYER,
                        description: "Destination points",
                        },
                field: {type: PARAMETER_FIELD,
                        description: "Attribute to identify desination points",
                        parent: "origin"
                        },
                addLines: {type: PARAMETER_BOOLEAN,
                        description:"Create origin-destination lines"}
                };
    };

    this.run = function(params){
        var destination = getTurfGeoJsonFromOL3LayerName(params.destination);
        var layerFeatures = getFeaturesFromLayerName(params.origin);
        var format = new ol.format.GeoJSON();
        var source = new ol.source.Vector();
        var linesSource = new ol.source.Vector();
        for (var i = 0; i < layerFeatures.length; i++) {
            var feature = JSON.parse(format.writeFeature(layerFeatures[i],
                        {dataProjection: EPSG4326,
                        featureProjection: map.getView().getProjection().getCode()}));
            var nearest = turf.nearest(feature, destination);
            var nearestFeature = format.readFeature(nearest, {dataProjection: EPSG4326,
                                    featureProjection: map.getView().getProjection().getCode()});
            feature = layerFeatures[i].clone();
            feature.setProperties({"nearest": nearestFeature.get(params.field)});
            source.addFeature(feature);
            if (params.addLines){
                c1 = layerFeatures[i].getGeometry().getFirstCoordinate();
                c2 = nearestFeature.getGeometry().getFirstCoordinate();
                var line = new ol.geom.LineString([c1, c2]);
                var lineFeature = new ol.Feature(line);
                linesSource.addFeature(lineFeature);
            }
        }
        createAndAddLayer(source, params.origin + "(nearest)");
        if (params.addLines){
            createAndAddLayer(linesSource, "Connection lines");
        }

    };

};

