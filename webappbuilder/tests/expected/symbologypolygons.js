var categories_polygons = {"2": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: [6], width: 0}),
                        fill: new ol.style.Fill({color: "rgba(32,225,68,1.0)"})
                        })
                        ],
"3": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: 3}),
                        fill: new ol.style.Fill({color: "rgba(116,229,72,1.0)"})
                        })
                        ],
"4": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(0,0,0,0.0)"})
                        })
                        ],
"5": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(217,116,133,1.0)"})
                        })
                        ,new ol.style.Style({
                            
                        })
                        ],
"6": [ new ol.style.Style({
                            
                        })
                        ],
"7": [ new ol.style.Style({
                            
                        })
                        ],
"8": [ new ol.style.Style({
                            
                        })
                        ],
"9": [ new ol.style.Style({
                            
                        })
                        ],
"10": [ new ol.style.Style({
                            
                        })
                        ],
"11": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(244,0,0,1.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(110,181,234,1.0)"})
                        })
                        ],
"": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(29,37,130,1.0)"})
                        })
                        ]};var categoriesSelected_polygons = {"2": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"3": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 3}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"4": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"5": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ,new ol.style.Style({
                            
                        })
                        ],
"6": [ new ol.style.Style({
                            
                        })
                        ],
"7": [ new ol.style.Style({
                            
                        })
                        ],
"8": [ new ol.style.Style({
                            
                        })
                        ],
"9": [ new ol.style.Style({
                            
                        })
                        ],
"10": [ new ol.style.Style({
                            
                        })
                        ],
"11": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ],
"": [ new ol.style.Style({
                            stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})
                        })
                        ]};
                    var textStyleCache_polygons={}
                    var clusterStyleCache_polygons={}
                    var style_polygons = function(feature, resolution){
                        
                        var value = feature.get("n");
                        var style = categories_polygons[value];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_polygons = function(feature, resolution){
                        
                        var value = feature.get("n");
                        var style = categoriesSelected_polygons[value]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
