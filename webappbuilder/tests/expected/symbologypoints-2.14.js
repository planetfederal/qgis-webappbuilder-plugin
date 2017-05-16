
var categories_points = function(){ return {"2": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(5.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/plane.png",
            })
                        })
                        ],
"3": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(30.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=airport.png",
            })
                        })
                        ],
"4": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(5.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/landuse_coniferous.png",
            })
                        })
                        ],
"5": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(10), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255,0,0,1.0)"}), angle: 0})
                        })
                        ,new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(0,0,0,1.0)"})})
                        })
                        ],
"6": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(154,25,240,1.0)"})})
                        })
                        ],
"7": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(4), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(227,26,28,1.0)"}), angle: 0.7853975})
                        })
                        ],
"8": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(202,109,108,1.0)"}), angle: 0})
                        })
                        ],
"9": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(43,86,228,1.0)"}), angle: 0})
                        })
                        ],
"10": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(211,236,141,1.0)"}), angle: 0.7853975})
                        })
                        ],
"11": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(224,126,165,1.0)"}), angle: 0})
                        })
                        ],
"12": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(4), radius2: pixelsFromMm(pixelsFromMm(4)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(227,26,28,1.0)"}), angle: 0})
                        })
                        ],
"13": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(20), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(70,205,171,1.0)"})})
                        })
                        ],
"14": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(5), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(3.0)}), fill: new ol.style.Fill({color: "rgba(47,219,56,1.0)"})})
                        })
                        ],
"15": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(11), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(173,30,216,1.0)"})})
                        })
                        ],
"16": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,38,241,1.0)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(32,217,19,1.0)"})})
                        })
                        ],
"": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,1.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(213,84,175,1.0)"})})
                        })
                        ]};};var categoriesSelected_points = {"2": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(5.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/plane.png",
            })
                        })
                        ],
"3": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(30.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/amenity=airport.png",
            })
                        })
                        ],
"4": [ new ol.style.Style({
                            image: new ol.style.Icon({
                  scale: pixelsFromMm(5.0) / 100.0,
                  anchorOrigin: 'top-left',
                  anchorXUnits: 'fraction',
                  anchorYUnits: 'fraction',
                  anchor: [0.5, 0.5],
                  size:[100,100],
                  src: "./data/styles/landuse_coniferous.png",
            })
                        })
                        ],
"5": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(10), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ,new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"6": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"7": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(4), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0.7853975})
                        })
                        ],
"8": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ],
"9": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ],
"10": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 4, radius1: pixelsFromMm(2), radius2: 0, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0.7853975})
                        })
                        ],
"11": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 3, radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ],
"12": [ new ol.style.Style({
                            image: new ol.style.RegularShape({points: 5, radius1: pixelsFromMm(4), radius2: pixelsFromMm(pixelsFromMm(4)/ 2.0), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"}), angle: 0})
                        })
                        ],
"13": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(20), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"14": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(5), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(3.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"15": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(11), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"16": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(1.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ],
"": [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ]};
                    var textStyleCache_points={}
                    var clusterStyleCache_points={}
                    var style_points = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_points'
        };

                        var value = feature.get("n");
                        var style = categories_points()[value];
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
                        var value = feature.get("n");
                        var style = categoriesSelected_points[value]
                        var allStyles = [];

                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };