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


                    var textStyleCache_points={}
                    var clusterStyleCache_points={}
                    var style_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points'
        };
                        
                        var value = '';
                        
                        function rules_points(value) {
                            var ruleStyles = [];
                            // Start of if blocks and style check logic
                            var matchFound = false;
                            if (pointsrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(5) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/plane.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(30) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=airport.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(5) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/landuse_coniferous.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(10/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255,0,0,1.0)"}), angle: 0}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(0,0,0,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(154,25,240,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(4/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(227,26,28,1.0)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule6_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(202,109,108,1.0)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule7_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2/ 2.0), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(43,86,228,1.0)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule8_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2/ 2.0), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(211,236,141,1.0)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule9_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(224,126,165,1.0)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule10_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(4/ 2.0), radius2: pixelsFromMm(4/ 4.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(227,26,28,1.0)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule11_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(20/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(70,205,171,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule12_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(5/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(3.0)}), fill: new ol.style.Fill({color: "rgba(47,219,56,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule13_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(11/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: [6], width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(173,30,216,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule14_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,38,241,1.0)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(32,217,19,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule16_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: size_dd_expression90346134269221763423_eval_expression(context)/ 2.0, stroke: new ol.style.Stroke({color: "rgba(80,149,51,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(80,149,51,1.0)"})}),
zIndex: 1
                            })
                            ,new ol.style.Style({
                                image: new ol.style.Circle({radius: size_dd_expression19925148205611244_eval_expression(context)/ 2.0, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(2.0)}), fill: new ol.style.Fill({color: "rgba(255,0,0,0.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule17_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(size_dd_expression694735488896353489_eval_expression(context)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(147,235,224,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule18_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMapUnits(1/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(192,81,229,1.0)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule19_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMapUnits(2) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/accommodation_camping.png",
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
                        var style = rules_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points'
        };
                        var value = '';
                        
                        function rules_points(value) {
                            var ruleStyles = [];
                            // Start of if blocks and style check logic
                            var matchFound = false;
                            if (pointsrule0_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(5) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/plane_selected.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule1_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(30) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=airport_selected.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule2_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMm(5) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/landuse_coniferous_selected.png",
            }),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule3_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(10/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0}),
zIndex: 0
                            })
                            ,new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule4_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule5_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(4/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule6_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule7_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2/ 2.0), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule8_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2/ 2.0), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0.7853975}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule9_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule10_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(4/ 2.0), radius2: pixelsFromMm(4/ 4.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule11_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(20/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule12_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(5/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(3.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule13_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(11/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: [6], width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule14_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(2/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule16_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: size_dd_expression18973520488091312255_eval_expression(context)/ 2.0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 1
                            })
                            ,new ol.style.Style({
                                image: new ol.style.Circle({radius: size_dd_expression207058114704911206593_eval_expression(context)/ 2.0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(2.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule17_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMm(size_dd_expression5290362403639304656_eval_expression(context)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule18_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Circle({radius: pixelsFromMapUnits(1/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})}),
zIndex: 0
                            })
                            ]);
                      matchFound = true;
                    }
                    if (pointsrule19_eval_expression(context)) {
                      ruleStyles.push.apply(ruleStyles, [ new ol.style.Style({
                                image: new ol.style.Icon({
                  scale: pixelsFromMapUnits(2) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/accommodation_camping_selected.png",
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
                        var style = rules_points(value);
                        
                        var allStyles = [];
                        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };

                    var textStyleCache_labels={}
                    var clusterStyleCache_labels={}
                    var style_labels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labels'
        };
                        
                        var value = '';
                        var style = [
                                   new ol.style.Style({})
                                 ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labels'
            };
            if (getFeatureAttribute(feature, "text") !== null) {
                var labelText = String(getFeatureAttribute(feature, "text"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labels[key]){
                var size = 12.0 * 2;
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
                textStyleCache_labels[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labels[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_labels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_labels'
        };
                        var value = '';
                        var style = [
                                   new ol.style.Style({})
                                 ];
                        var allStyles = [];
                        
            var labelContext = {
                feature: feature,
                variables: {},
                layer: 'lyr_labels'
            };
            if (getFeatureAttribute(feature, "text") !== null) {
                var labelText = String(getFeatureAttribute(feature, "text"));
            } else {
                var labelText = " ";
            }
            var key = value + "_" + labelText + "_" + String(resolution);
            if (!textStyleCache_labels[key]){
                var size = 12.0 * 2;
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
                textStyleCache_labels[key] = new ol.style.Style({zIndex: 1000, text: text});
            }
            allStyles.push(textStyleCache_labels[key]);
            
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
var baseLayers = [];var baseLayersGroup = new ol.layer.Group({showContent: true,
                    'isGroupExpanded': false, 'type': 'base-group',
                    'title': 'Base maps', layers: baseLayers});
var overlayLayers = [];var overlaysGroup = new ol.layer.Group({showContent: true,
                        'isGroupExpanded': false, 'title': 'Overlays', layers: overlayLayers});
var lyr_points = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_points,
                    selectedStyle: selectionStyle_points,
                    title: "points",
                    id: "points_shp20150708141950508",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["n"],
                    geometryType: "Point"
                });
points_geojson_callback = function(geojson) {
                              lyr_points.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };
var lyr_labels = new ol.layer.Vector({
                    opacity: 1.0,
                    source: new ol.source.Vector(),
                     
                    style: style_labels,
                    selectedStyle: selectionStyle_labels,
                    title: "labels",
                    id: "points_labels20170518142414900",
                    filters: [],
                    timeInfo: null,
                    isSelectable: true,
                    popupInfo: "",
                    attributes: ["fid", "text"],
                    geometryType: "Point"
                });
labels_geojson_callback = function(geojson) {
                              lyr_labels.getSource().addFeatures(new ol.format.GeoJSON().readFeatures(geojson));
                              
                        };

lyr_points.setVisible(true);
lyr_labels.setVisible(true);
var layersList = [lyr_points,lyr_labels];
var layersMap  = {'lyr_points':lyr_points,'lyr_labels':lyr_labels};
var view = new ol.View({extent: [-17.871984, -1.376469, 30.018694, 8.073531], maxZoom: 32, minZoom: 1, projection: 'EPSG:4326'});
var originalExtent = [-17.871984, -1.376469, 30.018694, 8.073531];
var unitsConversion = 1.0;

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: []
});



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
    var toolbarOptions = {title:"Points"};
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
