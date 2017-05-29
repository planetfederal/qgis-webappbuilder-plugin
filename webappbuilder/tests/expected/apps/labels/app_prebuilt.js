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


                    var textStyleCache_labelspointsup={}
                    var clusterStyleCache_labelspointsup={}
                    var style_labelspointsup = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsup'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(230,9,142,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsup'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsup[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "bottom",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsup[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsup[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelspointsup = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsup'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsup'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsup[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "bottom",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsup[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsup[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labelspointsright={}
                    var clusterStyleCache_labelspointsright={}
                    var style_labelspointsright = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsright'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(11,198,8,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsright'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsright[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsright[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsright[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelspointsright = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsright'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsright'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsright[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsright[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsright[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labelspointsleft={}
                    var clusterStyleCache_labelspointsleft={}
                    var style_labelspointsleft = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsleft'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(187,154,69,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsleft'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsleft[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "end",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsleft[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsleft[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelspointsleft = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsleft'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsleft'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsleft[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "end",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsleft[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsleft[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labelspointsdown={}
                    var clusterStyleCache_labelspointsdown={}
                    var style_labelspointsdown = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsdown'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(28,141,33,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsdown'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsdown[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "top",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsdown[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsdown[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelspointsdown = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelspointsdown'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelspointsdown'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelspointsdown[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "top",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelspointsdown[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelspointsdown[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labelslinefollowing={}
                    var clusterStyleCache_labelslinefollowing={}
                    var style_labelslinefollowing = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelslinefollowing'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(36,21,207,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelslinefollowing = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelslinefollowing'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labelsline={}
                    var clusterStyleCache_labelsline={}
                    var style_labelsline = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelsline'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(46,195,130,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelsline'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelsline[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelsline[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelsline[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labelsline = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labelsline'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labelsline'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labelsline[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_labelsline[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labelsline[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_mapunits={}
                    var clusterStyleCache_mapunits={}
                    var style_mapunits = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_mapunits'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(175,100,13,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_mapunits'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_mapunits[key]){
                var size = pixelsFromMapUnits(0.03 * 2);
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 15.0,
                      offsetY: 0.0 
                    });
                textStyleCache_mapunits[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_mapunits[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_mapunits = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_mapunits'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_mapunits'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_mapunits[key]){
                var size = pixelsFromMapUnits(0.03 * 2);
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 15.0,
                      offsetY: 0.0 
                    });
                textStyleCache_mapunits[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_mapunits[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_pointsrotated={}
                    var clusterStyleCache_pointsrotated={}
                    var style_pointsrotated = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_pointsrotated'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(182,246,102,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_pointsrotated'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_pointsrotated[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.872664625997,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_pointsrotated[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_pointsrotated[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_pointsrotated = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_pointsrotated'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_pointsrotated'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_pointsrotated[key]){
                var size = 8.25 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.872664625997,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_pointsrotated[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_pointsrotated[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_polygon={}
                    var clusterStyleCache_polygon={}
                    var style_polygon = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygon'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(83,158,134,1.0)"}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_polygon'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_polygon[key]){
                var size = 20.0 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(249, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 5 * 2
                  })
                    });
                textStyleCache_polygon[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_polygon[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_polygon = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_polygon'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                             stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.26)}),
                        fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_polygon'
            };
            if (feature.get("text") !== null) {
                var labelText = String(feature.get("text"));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_polygon[key]){
                var size = 20.0 * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(249, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "center",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 ,
                  stroke: new ol.style.Stroke({
                    color: "rgba(255, 255, 255, 255)",
                    width: 5 * 2
                  })
                    });
                textStyleCache_polygon[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_polygon[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_expression={}
                    var clusterStyleCache_expression={}
                    var style_expression = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_expression'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(109,248,204,1.0)"})}),
zIndex: 0
                        })
                        ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_expression'
            };
            if (label_expression_eval_expression(labelContext) !== null) {
                var labelText = String(label_expression_eval_expression(labelContext));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_expression[key]){
                var size = fontsize6474694455820877616_eval_expression(context) * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_expression[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_expression[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_expression = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_expression'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                        })
                        ]
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_expression'
            };
            if (label_expression_eval_expression(labelContext) !== null) {
                var labelText = String(label_expression_eval_expression(labelContext));
            } else {
                var labelText = "";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_expression[key]){
                var size = fontsize6474694455820877616_eval_expression(context) * 2;
                var font = 'normal normal ' + String(size) + 'px "MS Shell Dlg 2",sans-serif'
                var text = new ol.style.Text({
                      font: font,
                      text: labelText,
                      fill: new ol.style.Fill({
                        color: "rgba(0, 0, 0, 255)"
                      }),
                      textBaseline: "middle",
                      textAlign: "start",
                      rotation: -0.0,
                      offsetX: 0.0,
                      offsetY: 0.0 
                    });
                textStyleCache_expression[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_expression[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group',
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true,
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var lyr_labelspointsup = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsup,
                    selectedStyle: selectionStyle_labelspointsup,
                    title: "labels pointsup",
                    id: "labels_pointsup20170529115336758",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_labelspointsup_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsup});
labelspointsup_geojson_callback = function(geojson) {
                              lyr_labelspointsup.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelspointsup_overview.setSource(lyr_labelspointsup.getSource());
                        };
var lyr_labelspointsright = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsright,
                    selectedStyle: selectionStyle_labelspointsright,
                    title: "labels pointsright",
                    id: "labels_pointsright20170529115336750",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_labelspointsright_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsright});
labelspointsright_geojson_callback = function(geojson) {
                              lyr_labelspointsright.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelspointsright_overview.setSource(lyr_labelspointsright.getSource());
                        };
var lyr_labelspointsleft = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsleft,
                    selectedStyle: selectionStyle_labelspointsleft,
                    title: "labels pointsleft",
                    id: "labels_pointsleft20170529115336742",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_labelspointsleft_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsleft});
labelspointsleft_geojson_callback = function(geojson) {
                              lyr_labelspointsleft.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelspointsleft_overview.setSource(lyr_labelspointsleft.getSource());
                        };
var lyr_labelspointsdown = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsdown,
                    selectedStyle: selectionStyle_labelspointsdown,
                    title: "labels pointsdown",
                    id: "labels_pointsdown20170529115336733",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_labelspointsdown_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelspointsdown});
labelspointsdown_geojson_callback = function(geojson) {
                              lyr_labelspointsdown.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelspointsdown_overview.setSource(lyr_labelspointsdown.getSource());
                        };
var lyr_labelslinefollowing = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelslinefollowing,
                    selectedStyle: selectionStyle_labelslinefollowing,
                    title: "labels linefollowing",
                    id: "labels_linefollowing20170529115336724",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Line"
                });
var lyr_labelslinefollowing_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelslinefollowing});
labelslinefollowing_geojson_callback = function(geojson) {
                              lyr_labelslinefollowing.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelslinefollowing_overview.setSource(lyr_labelslinefollowing.getSource());
                        };
var lyr_labelsline = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labelsline,
                    selectedStyle: selectionStyle_labelsline,
                    title: "labels line",
                    id: "labels_line20170529115336713",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Line"
                });
var lyr_labelsline_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_labelsline});
labelsline_geojson_callback = function(geojson) {
                              lyr_labelsline.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_labelsline_overview.setSource(lyr_labelsline.getSource());
                        };
var lyr_mapunits = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_mapunits,
                    selectedStyle: selectionStyle_mapunits,
                    title: "mapunits",
                    id: "mapunits20170529120911854",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_mapunits_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_mapunits});
mapunits_geojson_callback = function(geojson) {
                              lyr_mapunits.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_mapunits_overview.setSource(lyr_mapunits.getSource());
                        };
var lyr_pointsrotated = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_pointsrotated,
                    selectedStyle: selectionStyle_pointsrotated,
                    title: "pointsrotated",
                    id: "pointsrotated20170529124812922",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
var lyr_pointsrotated_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_pointsrotated});
pointsrotated_geojson_callback = function(geojson) {
                              lyr_pointsrotated.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_pointsrotated_overview.setSource(lyr_pointsrotated.getSource());
                        };
var lyr_polygon = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_polygon,
                    selectedStyle: selectionStyle_polygon,
                    title: "polygon",
                    id: "polygon20170529125606417",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Polygon"
                });
var lyr_polygon_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_polygon});
polygon_geojson_callback = function(geojson) {
                              lyr_polygon.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_polygon_overview.setSource(lyr_polygon.getSource());
                        };
var lyr_expression = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_expression,
                    selectedStyle: selectionStyle_expression,
                    title: "expression",
                    id: "expression20170529132742373",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text", "size"],
                    geometryType: "Point"
                });
var lyr_expression_overview = new ol.layer.Vector({
                    source: new ol.source.Vector(),
                     
                    style: style_expression});
expression_geojson_callback = function(geojson) {
                              lyr_expression.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              lyr_expression_overview.setSource(lyr_expression.getSource());
                        };

lyr_labelspointsup.setVisible(true);
lyr_labelspointsright.setVisible(true);
lyr_labelspointsleft.setVisible(true);
lyr_labelspointsdown.setVisible(true);
lyr_labelslinefollowing.setVisible(true);
lyr_labelsline.setVisible(true);
lyr_mapunits.setVisible(true);
lyr_pointsrotated.setVisible(true);
lyr_polygon.setVisible(true);
lyr_expression.setVisible(true);
var layersList = [lyr_labelspointsup,lyr_labelspointsright,lyr_labelspointsleft,lyr_labelspointsdown,lyr_labelslinefollowing,lyr_labelsline,lyr_mapunits,lyr_pointsrotated,lyr_polygon,lyr_expression];
var layersMap  = {'lyr_labelspointsup':lyr_labelspointsup,'lyr_labelspointsright':lyr_labelspointsright,'lyr_labelspointsleft':lyr_labelspointsleft,'lyr_labelspointsdown':lyr_labelspointsdown,'lyr_labelslinefollowing':lyr_labelslinefollowing,'lyr_labelsline':lyr_labelsline,'lyr_mapunits':lyr_mapunits,'lyr_pointsrotated':lyr_pointsrotated,'lyr_polygon':lyr_polygon,'lyr_expression':lyr_expression};
var view = new ol.View({ maxZoom: 32, minZoom: 1, projection: 'EPSG:4326'});
var originalExtent = [3.076856, 3.560782, 7.186997, 6.298034];
var unitsConversion = 1.0;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});

function setTextPathStyle_labelslinefollowing(){
                lyr_labelslinefollowing.setTextPathStyle(function (feature){
                    var labelContext = {
                          feature: feature,
                          variables: {},
                          layer: 'lyr_$(layerName)s'
                      };
                    if (feature.get("text") !== null) {
                        var labelText = String(feature.get("text"));
                    } else {
                        var labelText = " ";
                    }
                    if (labelText == ""){
                        labelText = " ";
                    }
                    labelText = String(labelText);
                    var size = 8.25 * 2;
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
                            offsetX: 0.0,
                            offsetY: 0.0 
                        }),
                      })];
                },
                0);
              }
              setTextPathStyle_labelslinefollowing();

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
    var toolbarOptions = {title:"My Web App"};
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
