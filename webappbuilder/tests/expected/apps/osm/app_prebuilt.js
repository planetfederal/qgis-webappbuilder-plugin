injectTapEventPlugin();

var defaultFill = new ol.style.Fill({
  color: 'rgba(255,255,255,0.4)'
});
var defaultStroke = new ol.style.Stroke({
  color: '#3399CC',
  width: 1.25
});
var defaultSelectionFill = new ol.style.Fill({
  color: 'rgba(255,255,0,0.4)'
});
var defaultSelectionStroke = new ol.style.Stroke({
  color: '#FFFF00',
  width: 1.25
});

var patternFill_1 = new ol.style.Fill({});
                    var patternImg_1 = new Image();
                    patternImg_1.src = './data/styles/pointPattern_1.png';
                    patternImg_1.onload = function(){
                      var canvas = document.createElement('canvas');
                      var context = canvas.getContext('2d');
                      var pattern = context.createPattern(patternImg_1, 'repeat');
                      patternFill_1 = new ol.style.Fill({
                            color: pattern
                          });
                      lyr_ocupacao_agueda.changed()
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
                          lyr_ocupacao_agueda.changed()
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
                          lyr_ocupacao_agueda.changed()
                        };

                    var textStyleCache_ocupacao_agueda={}
                    var clusterStyleCache_ocupacao_agueda={}
                    var style_ocupacao_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_ocupacao_agueda'
        };
                        
                        var value = '';
                        
                        function rules_ocupacao_agueda(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (ocupacao_aguedarule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(128,152,72,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(186,221,105,1.0)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            fill: patternFill_1,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            geometry: function(feature){
                                geom = feature.getGeometry().clone()
                                geom.translate(0.8, 0.8);
                                return geom;
                            },
 stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(117,130,122,1.0)"}),
zIndex: 1
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(102,143,79,1.0)"}),
zIndex: 2
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(175,179,138,0.0)", lineDash: null, width: pixelsFromMm(0.0)}),
                        fill: new ol.style.Fill({color: "rgba(241,244,199,1.0)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            fill: patternFill_2,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(241,244,199,1.0)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            fill: patternFill_3,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(100,118,187,1.0)"}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_ocupacao_agueda(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_ocupacao_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_ocupacao_agueda'
        };
                        var value = '';
                        
                        function rules_ocupacao_agueda(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (ocupacao_aguedarule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            geometry: function(feature){
                                geom = feature.getGeometry().clone()
                                geom.translate(0.8, 0.8);
                                return geom;
                            },
 stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 1
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 2
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                 fill: defaultSelectionFill,
                 stroke: defaultSelectionStroke
                 ,
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (ocupacao_aguedarule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_ocupacao_agueda(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_linhasdegua={}
                    var clusterStyleCache_linhasdegua={}
                    var style_linhasdegua = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_linhasdegua'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(35,115,201,1.0)", lineDash: null, width: pixelsFromMm(0.35)}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_linhasdegua = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_linhasdegua'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.35)}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var categories_espacos_verdes_agueda = function(){ return {"garden": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(128,152,72,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(186,221,105,1.0)"}),
zIndex: 0
                        })
                        ],
"park": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(175,179,138,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(241,244,199,1.0)"}),
zIndex: 0
                        })
                        ],
"playground": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(175,179,138,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(253,255,210,1.0)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]};};var categoriesSelected_espacos_verdes_agueda = {"garden": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ],
"park": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ],
"playground": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]};
                    var textStyleCache_espacos_verdes_agueda={}
                    var clusterStyleCache_espacos_verdes_agueda={}
                    var style_espacos_verdes_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_espacos_verdes_agueda'
        };
                        
                        var value = feature.get("leisure");
                        var style = categories_espacos_verdes_agueda()[value];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_espacos_verdes_agueda'
            };
            if (feature.get("name") !== null) {
                var labelText = String(feature.get("name"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_espacos_verdes_agueda[key]){
                var size = 8.0 * 2;
                var font = 'italic normal ' + String(size) + 'px "Ubuntu",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(25, 134, 19, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0,
                      offsetY: 0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_espacos_verdes_agueda[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_espacos_verdes_agueda[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_espacos_verdes_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_espacos_verdes_agueda'
        };
                        var value = feature.get("leisure");
                        var style = categoriesSelected_espacos_verdes_agueda[value]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_espacos_verdes_agueda'
            };
            if (feature.get("name") !== null) {
                var labelText = String(feature.get("name"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_espacos_verdes_agueda[key]){
                var size = 8.0 * 2;
                var font = 'italic normal ' + String(size) + 'px "Ubuntu",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(25, 134, 19, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0,
                      offsetY: 0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_espacos_verdes_agueda[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_espacos_verdes_agueda[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var categories_agueda_waterways = function(){ return {"riverbank": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(35,113,209,1.0)", lineDash: null, width: pixelsFromMm(0.35)}),
                        fill: new ol.style.Fill({color: "rgba(165,191,221,1.0)"}),
zIndex: 0
                        })
                        ],
"water_well": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(90,193,157,1.0)"}),
zIndex: 0
                        })
                        ],
"weir": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(35,113,209,1.0)", lineDash: null, width: pixelsFromMm(0.35)}),
                        fill: new ol.style.Fill({color: "rgba(165,191,221,1.0)"}),
zIndex: 1
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]};};var categoriesSelected_agueda_waterways = {"riverbank": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.35)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ],
"water_well": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ],
"weir": [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.35)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 1
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]};
                    var textStyleCache_agueda_waterways={}
                    var clusterStyleCache_agueda_waterways={}
                    var style_agueda_waterways = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_waterways'
        };
                        
                        var value = feature.get("waterway");
                        var style = categories_agueda_waterways()[value];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_agueda_waterways = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_waterways'
        };
                        var value = feature.get("waterway");
                        var style = categoriesSelected_agueda_waterways[value]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_caminho_de_ferro={}
                    var clusterStyleCache_caminho_de_ferro={}
                    var style_caminho_de_ferro = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_caminho_de_ferro'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255,255,255,1.0)", lineDash: [6], width: pixelsFromMm(0.8)}),
zIndex: 1
                        })
                        ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_caminho_de_ferro = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_caminho_de_ferro'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: pixelsFromMm(0.8)}),
zIndex: 1
                        })
                        ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_estradas_agueda={}
                    var clusterStyleCache_estradas_agueda={}
                    var style_estradas_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_estradas_agueda'
        };
                        
                        var value = '';
                        
                        function rules_estradas_agueda(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (estradas_aguedarule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(149,90,56,1.0)", lineDash: [6], width: pixelsFromMm(0.36)}),
zIndex: 1
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(141,70,0,1.0)", lineDash: null, width: pixelsFromMm(3.1)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255,206,128,1.0)", lineDash: null, width: pixelsFromMm(2.5)}),
zIndex: 16
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(202,202,202,1.0)", lineDash: null, width: pixelsFromMm(2.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(221,201,255,1.0)", lineDash: null, width: pixelsFromMm(1.26)}),
zIndex: 1
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(150,94,4,1.0)", lineDash: null, width: pixelsFromMm(2.5)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255,255,255,1.0)", lineDash: null, width: pixelsFromMm(1.9)}),
zIndex: 15
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            geometry: function(feature){
                              var start = feature.getGeometry().getFirstCoordinate();
                              var end = feature.getGeometry().getLastCoordinate();
                              var dx = end[0] - start[0];
                              var dy = end[1] - start[1];
                              var rotation = Math.atan2(dy, dx);
                              offset = -0.8;
                              x = Math.sin(rotation) * offset;
                              y = Math.cos(rotation) * offset;
                              geom = feature.getGeometry().clone()
                              geom.translate(x, y);
                              return geom;
                            }, stroke: new ol.style.Stroke({color: "rgba(149,149,149,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            geometry: function(feature){
                              var start = feature.getGeometry().getFirstCoordinate();
                              var end = feature.getGeometry().getLastCoordinate();
                              var dx = end[0] - start[0];
                              var dy = end[1] - start[1];
                              var rotation = Math.atan2(dy, dx);
                              offset = 0.8;
                              x = Math.sin(rotation) * offset;
                              y = Math.cos(rotation) * offset;
                              geom = feature.getGeometry().clone()
                              geom.translate(x, y);
                              return geom;
                            }, stroke: new ol.style.Stroke({color: "rgba(149,149,149,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(221,221,221,1.0)", lineDash: null, width: pixelsFromMm(1.66)}),
zIndex: 0
                        })
                        ];
                            }
                            return ruleStyles;
                        }
                        var style = rules_estradas_agueda(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_estradas_agueda = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_estradas_agueda'
        };
                        var value = '';
                        
                        function rules_estradas_agueda(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (estradas_aguedarule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: pixelsFromMm(0.36)}),
zIndex: 1
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(3.1)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(2.5)}),
zIndex: 16
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(2.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.26)}),
zIndex: 1
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(2.5)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.9)}),
zIndex: 15
                        })
                        ]);
                      matchFound = true;
                    }
                    if (estradas_aguedarule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            geometry: function(feature){
                              var start = feature.getGeometry().getFirstCoordinate();
                              var end = feature.getGeometry().getLastCoordinate();
                              var dx = end[0] - start[0];
                              var dy = end[1] - start[1];
                              var rotation = Math.atan2(dy, dx);
                              offset = -0.8;
                              x = Math.sin(rotation) * offset;
                              y = Math.cos(rotation) * offset;
                              geom = feature.getGeometry().clone()
                              geom.translate(x, y);
                              return geom;
                            }, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            geometry: function(feature){
                              var start = feature.getGeometry().getFirstCoordinate();
                              var end = feature.getGeometry().getLastCoordinate();
                              var dx = end[0] - start[0];
                              var dy = end[1] - start[1];
                              var rotation = Math.atan2(dy, dx);
                              offset = 0.8;
                              x = Math.sin(rotation) * offset;
                              y = Math.cos(rotation) * offset;
                              geom = feature.getGeometry().clone()
                              geom.translate(x, y);
                              return geom;
                            }, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ,new ol.style.Style({
                            
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.66)}),
zIndex: 0
                        })
                        ];
                            }
                            return ruleStyles;
                        }
                        var style = rules_estradas_agueda(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_agueda_edificios={}
                    var clusterStyleCache_agueda_edificios={}
                    var style_agueda_edificios = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_edificios'
        };
                        
                        var value = '';
                        
                        function rules_agueda_edificios(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (agueda_edificiosrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(216,150,85,1.0)"}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(159,123,15,1.0)"}),
zIndex: 0
                        })
                        ];
                            }
                            return ruleStyles;
                        }
                        var style = rules_agueda_edificios(value);
                        
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_agueda_edificios'
            };
            if (label_agueda_edificios_eval_expression(labelContext) !== null) {
                var labelText = String(label_agueda_edificios_eval_expression(labelContext));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_agueda_edificios[key]){
                var size = 9.0 * 2;
                var font = 'italic normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0,
                      offsetY: 0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_agueda_edificios[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_agueda_edificios[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_agueda_edificios = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_edificios'
        };
                        var value = '';
                        
                        function rules_agueda_edificios(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (agueda_edificiosrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ];
                            }
                            return ruleStyles;
                        }
                        var style = rules_agueda_edificios(value);
                        
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_agueda_edificios'
            };
            if (label_agueda_edificios_eval_expression(labelContext) !== null) {
                var labelText = String(label_agueda_edificios_eval_expression(labelContext));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_agueda_edificios[key]){
                var size = 9.0 * 2;
                var font = 'italic normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0,
                      offsetY: 0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 1 * 2
                  })
                    });
                textStyleCache_agueda_edificios[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_agueda_edificios[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_agueda_points={}
                    var clusterStyleCache_agueda_points={}
                    var style_agueda_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_points'
        };
                        
                        var value = '';
                        
                        function rules_agueda_points(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (agueda_pointsrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/education_university.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/money_currency_exchange.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food_bar.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/highway=bus_stop.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/tourist_cinema2.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food_fastfood.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule6_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=parking.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule7_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/health_doctors.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule8_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=place_of_worship.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule9_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_police2.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule10_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_post_office.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule11_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule12_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/svg.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule13_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=taxi.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule14_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=telephone.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule15_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_toilets.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_agueda_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_agueda_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_agueda_points'
        };
                        var value = '';
                        
                        function rules_agueda_points(value) {
                            ruleStyles = [];
                            // Start of if blocks and style check logic
                            matchFound = false;
                            if (agueda_pointsrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/education_university.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/money_currency_exchange.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food_bar.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/highway=bus_stop.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/tourist_cinema2.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food_fastfood.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule6_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=parking.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule7_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/health_doctors.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule8_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=place_of_worship.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule9_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_police2.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule10_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_post_office.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule11_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/food.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule12_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/svg.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule13_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=taxi.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule14_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=telephone.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                    if (agueda_pointsrule15_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(4.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity_toilets.png",
            }),
zIndex: 0
                        })
                        ]);
                      matchFound = true;
                    }
                            if (!matchFound) {
                                ruleStyles = [];
                            }
                            return ruleStyles;
                        }
                        var style = rules_agueda_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group',
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true,
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var lyr_ocupacao_agueda = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_ocupacao_agueda,
                    selectedStyle: selectionStyle_ocupacao_agueda,
                    title: "ocupacao_agueda",
                    id: "ocupacao_agueda20140527225336940",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "landuse", "surface"],
                    geometryType: "Polygon"
                });
var lyr_ocupacao_agueda_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_ocupacao_agueda});
ocupacao_agueda_geojson_callback = function(geojson) {
                              lyr_ocupacao_agueda.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_ocupacao_agueda_overview.setSource(lyr_ocupacao_agueda.getSource());
                        };
var lyr_linhasdegua = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_linhasdegua,
                    selectedStyle: selectionStyle_linhasdegua,
                    title: "linhas de água",
                    id: "linhas_de_água20140529224009280",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "waterway"],
                    geometryType: "Line"
                });
var lyr_linhasdegua_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_linhasdegua});
linhasdegua_geojson_callback = function(geojson) {
                              lyr_linhasdegua.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_linhasdegua_overview.setSource(lyr_linhasdegua.getSource());
                        };
var lyr_espacos_verdes_agueda = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_espacos_verdes_agueda,
                    selectedStyle: selectionStyle_espacos_verdes_agueda,
                    title: "espacos_verdes_agueda",
                    id: "espacos_verdes_agueda20140527224934372",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "leisure"],
                    geometryType: "Polygon"
                });
var lyr_espacos_verdes_agueda_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_espacos_verdes_agueda});
espacos_verdes_agueda_geojson_callback = function(geojson) {
                              lyr_espacos_verdes_agueda.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_espacos_verdes_agueda_overview.setSource(lyr_espacos_verdes_agueda.getSource());
                        };
var lyr_agueda_waterways = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_waterways,
                    selectedStyle: selectionStyle_agueda_waterways,
                    title: "agueda_waterways",
                    id: "agueda_waterways20140529225453968",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "waterway"],
                    geometryType: "Polygon"
                });
var lyr_agueda_waterways_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_waterways});
agueda_waterways_geojson_callback = function(geojson) {
                              lyr_agueda_waterways.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_agueda_waterways_overview.setSource(lyr_agueda_waterways.getSource());
                        };
var lyr_caminho_de_ferro = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_caminho_de_ferro,
                    selectedStyle: selectionStyle_caminho_de_ferro,
                    title: "caminho_de_ferro",
                    id: "caminho_de_ferro20140529215518653",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "railway"],
                    geometryType: "Line"
                });
var lyr_caminho_de_ferro_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_caminho_de_ferro});
caminho_de_ferro_geojson_callback = function(geojson) {
                              lyr_caminho_de_ferro.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_caminho_de_ferro_overview.setSource(lyr_caminho_de_ferro.getSource());
                        };
var lyr_estradas_agueda = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_estradas_agueda,
                    selectedStyle: selectionStyle_estradas_agueda,
                    title: "estradas_agueda",
                    id: "estradas_agueda20140527224736172",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "ref", "highway"],
                    geometryType: "Line"
                });
var lyr_estradas_agueda_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_estradas_agueda});
estradas_agueda_geojson_callback = function(geojson) {
                              lyr_estradas_agueda.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_estradas_agueda_overview.setSource(lyr_estradas_agueda.getSource());
                        };
var lyr_agueda_edificios = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_edificios,
                    selectedStyle: selectionStyle_agueda_edificios,
                    title: "agueda_edificios",
                    id: "agueda_edificios20140527224548231",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "name", "leisure", "amenity", "addr_house"],
                    geometryType: "Polygon"
                });
var lyr_agueda_edificios_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_edificios});
agueda_edificios_geojson_callback = function(geojson) {
                              lyr_agueda_edificios.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_agueda_edificios_overview.setSource(lyr_agueda_edificios.getSource());
                        };
var lyr_agueda_points = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_points,
                    selectedStyle: selectionStyle_agueda_points,
                    title: "agueda_points",
                    id: "agueda_points20140527224113246",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["id", "addr_city", "addr_count", "addr_house", "addr_hou_1", "addr_postc", "addr_state", "addr_stree", "aeroway", "alt_name", "amenity", "atm", "atm_networ", "barrier", "bench", "bicycle", "brand", "building", "communicat", "communic_1", "communic_2", "communic_3", "communic_4", "communic_5", "communic_6", "contacto", "craft", "crossing", "crossing_r", "cuisine", "denominati", "designatio", "email", "emergency", "fax", "fee", "fire_hydra", "fire_hyd_1", "foot", "fuel_diese", "fuel_octan", "fuel_oct_1", "genus", "highway", "historic", "horse", "indoor", "internet_a", "is_in_coun", "lamp_numbe", "landuse", "leisure", "man_made", "material", "motorcar", "motorcycle", "name", "name_botan", "name_en", "name_pt", "natural", "network", "nif", "noexit", "note", "notes", "office", "oneway", "opening_ho", "operator", "organic", "parking", "phone", "phone_pt", "place", "power", "public_tra", "railway", "recycling_", "recyclin_1", "recyclin_2", "recyclin_3", "recyclin_4", "recyclin_5", "recyclin_6", "recyclin_7", "recyclin_8", "recyclin_9", "recyclin10", "recyclin11", "recyclin12", "recyclin13", "recyclin14", "ref", "religion", "seats", "shelter", "shop", "site", "smoking", "source", "species", "sport", "surveillan", "tactile_pa", "taxon", "tourism", "tower_type", "train", "transforme", "type", "waste", "website", "wheelchair", "wifi", "wikipedia", "LblSize", "LblColor", "LblBold", "LblItalic", "LblUnderl", "LblStrike", "LblFont", "LblX", "LblY", "LblSclMin", "LblSclMax", "LblAlignH", "LblAlignV", "LblRot", "symbX", "symbY"],
                    geometryType: "Point"
                });
var lyr_agueda_points_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_agueda_points});
agueda_points_geojson_callback = function(geojson) {
                              lyr_agueda_points.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_agueda_points_overview.setSource(lyr_agueda_points.getSource());
                        };

lyr_ocupacao_agueda.setVisible(true);
lyr_linhasdegua.setVisible(true);
lyr_espacos_verdes_agueda.setVisible(true);
lyr_agueda_waterways.setVisible(true);
lyr_caminho_de_ferro.setVisible(true);
lyr_estradas_agueda.setVisible(true);
lyr_agueda_edificios.setVisible(true);
lyr_agueda_points.setVisible(true);
var layersList = [lyr_ocupacao_agueda,lyr_linhasdegua,lyr_espacos_verdes_agueda,lyr_agueda_waterways,lyr_caminho_de_ferro,lyr_estradas_agueda,lyr_agueda_edificios,lyr_agueda_points];
var layersMap  = {'lyr_ocupacao_agueda':lyr_ocupacao_agueda,'lyr_linhasdegua':lyr_linhasdegua,'lyr_espacos_verdes_agueda':lyr_espacos_verdes_agueda,'lyr_agueda_waterways':lyr_agueda_waterways,'lyr_caminho_de_ferro':lyr_caminho_de_ferro,'lyr_estradas_agueda':lyr_estradas_agueda,'lyr_agueda_edificios':lyr_agueda_edificios,'lyr_agueda_points':lyr_agueda_points};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:3857'});
var originalExtent = [-940697.206087, 4949272.569534, -938414.656583, 4950214.651148];
var unitsConversion = 1;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});

function setTextPathStyle_linhasdegua(){
                lyr_linhasdegua.setTextPathStyle(function (feature){
                    var labelContext = {
                          feature: feature,
                          variables: {},
                          layer: 'lyr_$(layerName)s'
                      };
                    var labelText = String(feature.get("name"));
                    if (labelText == null || labelText == "") {
                        var labelText = " ";
                    }
                    var size = 9.0 * 2;
                    var font = 'italic bold ' + String(size) + 'px "Ubuntu",sans-serif'
                    return [ new ol.style.Style({
                        text: new ol.style.TextPath({
                            font: font,
                            text: labelText,
                            fill: new ol.style.Fill({
                                color: "rgba(48, 59, 203, 255)"
                            }),
                            textBaseline: "middle",
                            textAlign: "center",
                            rotation: -0.0,
                            offsetX: 0,
                            offsetY: 0 
                        }),
                      })];
                },
                0);
              }
              setTextPathStyle_linhasdegua();
function setTextPathStyle_estradas_agueda(){
                lyr_estradas_agueda.setTextPathStyle(function (feature){
                    var labelContext = {
                          feature: feature,
                          variables: {},
                          layer: 'lyr_$(layerName)s'
                      };
                    var labelText = String(label_estradas_agueda_eval_expression(labelContext));
                    if (labelText == null || labelText == "") {
                        var labelText = " ";
                    }
                    var size = 6.0 * 2;
                    var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                    return [ new ol.style.Style({
                        text: new ol.style.TextPath({
                            font: font,
                            text: labelText,
                            fill: new ol.style.Fill({
                                color: "rgba(0, 0, 0, 255)"
                            }),
                            textBaseline: "middle",
                            textAlign: "center",
                            rotation: -0.0,
                            offsetX: 0,
                            offsetY: 0 
                        }),
                      })];
                },
                0);
              }
              setTextPathStyle_estradas_agueda();

function pixelsFromMapUnits(size) {
    return size / map.getView().getResolution() * unitsConversion;
};

function pixelsFromMm(size) {
    return 96 / 25.4 * size;
};

var BasicApp = React.createClass({
  childContextTypes: {
    muiTheme: React.PropTypes.object
  },
  getChildContext: function() {
    return {
      muiTheme: getMuiTheme()
    };
  },
  componentDidMount: function() {
    
  },
  _toggle: function(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  },
  _toggleTable: function() {
    this._toggle(document.getElementById('table-panel'));
    this.refs.table.getWrappedInstance().setDimensionsOnState();
  },
  _toggleWFST: function() {
    this._toggle(document.getElementById('wfst'));
  },
  _toggleQuery: function() {
    this._toggle(document.getElementById('query-panel'));
  },
  _toggleEdit: function() {
    this._toggle(document.getElementById('edit-tool-panel'));
  },
  _hideAboutPanel: function(evt) {
    evt.preventDefault();
    document.getElementById('about-panel').style.display = 'none';
  },
  _toggleChartPanel: function(evt) {
    evt.preventDefault();
    this._toggle(document.getElementById('chart-panel'));
  },
  render: function() {
    var toolbarOptions = {showMenuIconButton: false, title:"My Web App"};
    return React.createElement("div", {id: 'content'},
      React.createElement(Header, toolbarOptions ),
      React.createElement(MapPanel, {useHistory: true, extent: originalExtent, id: 'map', map: map}
        ,
React.createElement("div", {id: 'popup', className: 'ol-popup'},
                                    React.createElement(InfoPopup, {toggleGroup: 'navigation', map: map, hover: false})
                                  )
      )
      
    );
  }
});

ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(BasicApp)), document.getElementById('main'));
