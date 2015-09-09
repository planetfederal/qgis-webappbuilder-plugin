
                        var textStyleCache_simplelabels={}
                        var clusterStyleCache_simplelabels={}
                        var selectedClusterStyleCache_simplelabels={}
                        var style_simplelabels = function(feature, resolution){
                        var selected = lyr_simplelabels.selectedFeatures;
                        
                        if (feature.hide === true){
                return null;
            }
            
                        
                        var value = ""
                        var style = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: 3.8, stroke: new ol.style.Stroke({color: "rgba(0,0,0,0.0)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(46,62,165,0.0)"})})
                        })
                        ];
                        var selectionStyle = [ new ol.style.Style({
                            image: new ol.style.Circle({radius: 3.8, stroke: new ol.style.Stroke({color: "rgba(255, 204, 0, 1)", lineDash: null, width: 0}), fill: new ol.style.Fill({color: "rgba(255, 204, 0, 1)"})})
                        })
                        ];
                        allStyles = [];
                        
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
        
                        if (selected && selected.indexOf(feature) != -1){
                            allStyles.push.apply(allStyles, selectionStyle);
                        }
                        else{
                            allStyles.push.apply(allStyles, style);
                        }
                        return allStyles;
                    };