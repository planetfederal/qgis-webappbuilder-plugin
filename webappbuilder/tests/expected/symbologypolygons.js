
var patternFill_1 = new ol.style.Fill({});
                        var patternImg_1 = new Image();
                        patternImg_1.src = './data/styles/patternFill_1.svg';
                        patternImg_1.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_1, 'repeat');
                          patternFill_1 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_2 = new ol.style.Fill({});
                        var patternImg_2 = new Image();
                        patternImg_2.src = './data/styles/patternFill_2.svg';
                        patternImg_2.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_2, 'repeat');
                          patternFill_2 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_3 = new ol.style.Fill({});
                        var patternImg_3 = new Image();
                        patternImg_3.src = './data/styles/patternFill_3.svg';
                        patternImg_3.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_3, 'repeat');
                          patternFill_3 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var patternFill_4 = new ol.style.Fill({});
                        var patternImg_4 = new Image();
                        patternImg_4.src = './data/styles/patternFill_4.svg';
                        patternImg_4.onload = function(){
                          var canvas = document.createElement('canvas');
                          var context = canvas.getContext('2d');
                          var pattern = context.createPattern(patternImg_4, 'repeat');
                          patternFill_4 = new ol.style.Fill({
                                color: pattern
                              });
                          lyr_polygons.changed()
                        };
var categories_polygons = function(){ return {"2": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: [6], width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(32,225,68,1.0)"})
                        })
                        ],
"3": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.0)}),
                        fill: new ol.style.Fill({color: "rgba(116,229,72,1.0)"})
                        })
                        ],
"4": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(0,0,0,0.0)"})
                        })
                        ],
"5": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(217,116,133,1.0)"})
                        })
                        ,new ol.style.Style({
                            fill: patternFill_1
                        })
                        ],
"6": [ new ol.style.Style({
                            fill: patternFill_2
                        })
                        ],
"7": [ new ol.style.Style({
                            fill: patternFill_3
                        })
                        ],
"8": [ new ol.style.Style({
                            fill: patternFill_4
                        })
                        ],
"9": [ new ol.style.Style({
                            
                        })
                        ],
"10": [ new ol.style.Style({
                            
                        })
                        ],
"11": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(244,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(110,181,234,1.0)"})
                        })
                        ],
"": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(29,37,130,1.0)"})
                        })
                        ]};};var categoriesSelected_polygons = {"2": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"3": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"4": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"5": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ,new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 
                        })
                        ],
"6": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 
                        })
                        ],
"7": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 
                        })
                        ],
"8": [ new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 
                        })
                        ],
"9": [ new ol.style.Style({
                            
                        })
                        ],
"10": [ new ol.style.Style({
                            
                        })
                        ],
"11": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ]};
                    var textStyleCache_polygons={}
                    var clusterStyleCache_polygons={}
                    var style_polygons = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons'
        };
                        
                        var value = feature.get("n");
                        var style = categories_polygons()[value];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_polygons = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygons'
        };
                        var value = feature.get("n");
                        var style = categoriesSelected_polygons[value]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };