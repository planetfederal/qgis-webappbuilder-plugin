                    var textStyleCache_simplelabels={}
                    var clusterStyleCache_simplelabels={}
                    var style_simplelabels = function(feature, resolution){
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: 3.8, stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(46,62,165,0.0)"})})
                        })
                        ];
                        var allStyles = [];
                        
        var labelText = feature.get("n");
        
        var key = value + "_" + labelText;
        if (!textStyleCache_simplelabels[key]){
            var text = new ol.style.Text({
                  font: '28.0px Calibri,sans-serif',
                  text: labelText,
                  fill: new ol.style.Fill({
                    color: "rgba(0, 0, 0, 255)"
                  }),
                  textBaseline: "middle",
                  textAlign: "center",
                  rotation: -0.0,
                  offsetX: 0,
                  offsetY: 0 
                });
            textStyleCache_simplelabels[key] = new ol.style.Style({"text": text});
        }
        allStyles.push(textStyleCache_simplelabels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_simplelabels = function(feature, resolution){
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: 3.8, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ]
                        var allStyles = [];
                        
        var labelText = feature.get("n");
        
        var key = value + "_" + labelText;
        if (!textStyleCache_simplelabels[key]){
            var text = new ol.style.Text({
                  font: '28.0px Calibri,sans-serif',
                  text: labelText,
                  fill: new ol.style.Fill({
                    color: "rgba(0, 0, 0, 255)"
                  }),
                  textBaseline: "middle",
                  textAlign: "center",
                  rotation: -0.0,
                  offsetX: 0,
                  offsetY: 0 
                });
            textStyleCache_simplelabels[key] = new ol.style.Style({"text": text});
        }
        allStyles.push(textStyleCache_simplelabels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
