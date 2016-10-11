var categories_lines = function(){ return {"2": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(84,229,181,1.0)", lineDash: null, width: 0})
                        })
                        ],
"3": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(59,37,41,1.0)", lineDash: [6], width: 0})
                        })
                        ],
"4": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(122,245,0,1.0)", lineDash: null, width: 5})
                        })
                        ,new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(170,48,0,1.0)", lineDash: [6], width: 5})
                        })
                        ],
"5": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(143,135,230,1.0)", lineDash: null, width: 7})
                        })
                        ],
"6": [ new ol.style.Style({

                        })
                        ],
"7": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255,255,255,1.0)", lineDash: null, width: 4})
                        })
                        ,new ol.style.Style({

                        })
                        ],
"8": [ new ol.style.Style({

                        })
                        ]};};var categoriesSelected_lines = {"2": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0})
                        })
                        ],
"3": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: 0})
                        })
                        ],
"4": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 5})
                        })
                        ,new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: 5})
                        })
                        ],
"5": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 7})
                        })
                        ],
"6": [ new ol.style.Style({

                        })
                        ],
"7": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 4})
                        })
                        ,new ol.style.Style({

                        })
                        ],
"8": [ new ol.style.Style({

                        })
                        ]};
                    var textStyleCache_lines={}
                    var clusterStyleCache_lines={}
                    var style_lines = function(feature, resolution){

                        var value = feature.get("n");
                        var style = categories_lines()[value];
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_lines = function(feature, resolution){

                        var value = feature.get("n");
                        var style = categoriesSelected_lines[value]
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
