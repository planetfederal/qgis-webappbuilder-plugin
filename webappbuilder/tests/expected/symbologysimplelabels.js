var textStyleCache_simplelabels={}
                    var clusterStyleCache_simplelabels={}
                    var style_simplelabels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_simplelabels'
        };
                        
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(46,62,165,0.0)"})})
                        })
                        ];
                        var allStyles = [];
                        
        var labelContext = {
            feature: feature,
            variables: {},
            layer: 'lyr_simplelabels'
        };
        if (feature.get("n") !== null) {
            var labelText = String(feature.get("n"));
        } else {
            var labelText = "";
        }
        var key = value + "_" + labelText + "_" + String(resolution);
        if (!textStyleCache_simplelabels[key]){
            var size = 10;
            var font = String(size) + 'px Calibri,sans-serif'
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
                  offsetY: 0 
                });
            textStyleCache_simplelabels[key] = new ol.style.Style({zIndex: 1000, text: text});
        }
        allStyles.push(textStyleCache_simplelabels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };
                    var selectionStyle_simplelabels = function(feature, resolution){
                        var context = {
            feature: feature,
            variables: {},
            layer: 'lyr_simplelabels'
        };
                        var value = "";
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: pixelsFromMm(2), stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: pixelsFromMm(0.0)}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ]
                        var allStyles = [];
                        
        var labelContext = {
            feature: feature,
            variables: {},
            layer: 'lyr_simplelabels'
        };
        if (feature.get("n") !== null) {
            var labelText = String(feature.get("n"));
        } else {
            var labelText = "";
        }
        var key = value + "_" + labelText + "_" + String(resolution);
        if (!textStyleCache_simplelabels[key]){
            var size = 10;
            var font = String(size) + 'px Calibri,sans-serif'
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
                  offsetY: 0 
                });
            textStyleCache_simplelabels[key] = new ol.style.Style({zIndex: 1000, text: text});
        }
        allStyles.push(textStyleCache_simplelabels[key]);
        
                        allStyles.push.apply(allStyles, style);
                        return allStyles;
                    };