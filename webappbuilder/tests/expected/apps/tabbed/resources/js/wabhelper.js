
function kilometersFromPixels(pixels){
    return pixels * map.getView().getResolution()
        * ol.proj.METERS_PER_UNIT[map.getView().getProjection().getUnits()] / 1000.0;
}

function pixelsFromMapUnits(size) {
    return size / map.getView().getResolution() * unitsConversion;
};

function pixelsFromMm(size) {
    return 96 / 25.4 * size;
};

function textPath(ctx, text, path){

    function dist2D(x1,y1,x2,y2){
        var dx = x2-x1;
        var dy = y2-y1;
        return Math.sqrt(dx*dx+dy*dy);
    }

    var di, dpos=0;
    var pos=2;
    function getPoint(path, dl){
        if (!di || dpos+di<dl){
            for (; pos<path.length; ){
                di = dist2D(path[pos-2],path[pos-1],path[pos],path[pos+1]);
                if (dpos+di>dl) break;
                pos += 2;
                if (pos>=path.length) break;
                dpos += di;
            }
        }

        var x, y, a, dt = dl-dpos;
        if (pos>=path.length){
            pos = path.length-2;
        }

        if (!dt){
            x = path[pos-2];
            y = path[pos-1];
            a = Math.atan2(path[pos+1]-path[pos-1], path[pos]-path[pos-2]);
        }
        else{
            x = path[pos-2]+ (path[pos]-path[pos-2])*dt/di;
            y = path[pos-1]+(path[pos+1]-path[pos-1])*dt/di;
            a = Math.atan2(path[pos+1]-path[pos-1], path[pos]-path[pos-2]);
        }
        return [x,y,a];
    }

    var letterPadding = ctx.measureText(" ").width *0.25;

    var start = 0;

    var d = 0;
    for (var i=2; i<path.length; i+=2){
        d += dist2D(path[i-2],path[i-1],path[i],path[i+1]);
    }
    var nbspace = text.split(" ").length -1;

    if (d < ctx.measureText(text).width + (text.length-1 + nbspace) * letterPadding) return;

    switch (ctx.textAlign){
        case "center":
        case "end":
        case "right":{
            start = d - ctx.measureText(text).width - (text.length + nbspace) * letterPadding;
            if (ctx.textAlign == "center") start /= 2;
            }
            break;
        default: break;
    }

    for (var t=0; t<text.length; t++){
        var letter = text[t];
        var wl = ctx.measureText(letter).width;

        var p = getPoint(path, start+wl/2);

        ctx.save();
        ctx.textAlign = "center";
        ctx.translate(p[0], p[1]);
        ctx.rotate(p[2]);
        if (ctx.lineWidth) ctx.strokeText(letter,0,0);
        ctx.fillText(letter,0,0);
        ctx.restore();
        start += wl+letterPadding*(letter==" "?2:1);
    }

}

function drawTextPath (e){
    var extent = e.frameState.extent;
    var c2p = e.frameState.coordinateToPixelTransform;

    // Get pixel path with coordinates
    function getPath(c, readable){
        var path1 = [];
        for (var k=0; k<c.length; k++){
            path1.push(c2p[0]*c[k][0]+c2p[1]*c[k][1]+c2p[4]);
            path1.push(c2p[2]*c[k][0]+c2p[3]*c[k][1]+c2p[5]);
        }
        // Revert line ?
        if (readable && path1[0]>path1[path1.length-2]){
            var path2 = [];
            for (var k=path1.length-2; k>=0; k-=2){
                path2.push(path1[k]);
                path2.push(path1[k+1]);
            }
            return path2;
        }
        else return path1;
    }

    var ctx = e.context;
    ctx.save();
    ctx.scale(e.frameState.pixelRatio,e.frameState.pixelRatio);

    var features = this.getSource().getFeaturesInExtent(extent);
    for (var i=0, f; f=features[i]; i++){
        var style = this.textPathStyle_(f,e.frameState.viewState.resolution);
        for (var s,j=0; s=style[j]; j++){
            var g = s.getGeometry() || f.getGeometry();
            var c;
            switch (g.getType()){
                case "LineString": c = g.getCoordinates(); break;
                case "MultiLineString": c = g.getLineString(0).getCoordinates(); break;
                default: continue;
            }

            var st = s.getText();
            var path = getPath(c, true);

            ctx.font = st.getFont();
            ctx.textBaseline = st.getTextBaseline();
            ctx.textAlign = st.getTextAlign();
            ctx.lineWidth = st.getStroke() ? (st.getStroke().getWidth()||0) : 0;
            ctx.strokeStyle = st.getStroke() ? (st.getStroke().getColor()||"#fff") : "#fff";
            ctx.fillStyle = st.getFill() ? st.getFill().getColor()||"#000" : "#000";
            // Draw textpath
            textPath(ctx, st.getText()||f.get("name"), path);
        }
    }

    ctx.restore();
}

function setTextPathStyle (layer, style){
    if (!layer.textPath_){
        layer.textPath_ = layer.on('postcompose', drawTextPath, layer);
    }
    layer.textPathStyle_ = style;
    layer.changed();
}

function geojsonFromGeometry(geom){
    return {"type": "Feature",
            "properties": {},
            "geometry": new ol.format.GeoJSON().writeGeometryObject(geom,
                        {featureProjection: map.getView().getProjection().getCode(),
                        dataProjection: "EPSG:4326"})
            };
};

function geometryFromGeojson(geoj) {
    if (geoj === undefined){
        return undefined;
    }
    return new ol.format.GeoJSON().readFeature(geoj,
                        {featureProjection: map.getView().getProjection().getCode(),
                        dataProjection: "EPSG:4326"}).getGeometry();
};

function bezier(line){
    var geom = geojsonFromGeometry(line);
    return geometryFromGeojson(turf.bezier(geom));
};

function arrowPolygon(curve,width,length, thickness){
    try{
        if (width > 0){
            var turfCurve = geojsonFromGeometry(curve);
            var dist = turf.lineDistance(turfCurve) - length / 1000.0;
            var shortCurve = geometryFromGeojson(turf.lineSliceAlong(turfCurve, 0, dist))
            var center = shortCurve.getLastCoordinate();
            var last = shortCurve.getCoordinates()[shortCurve.getCoordinates().length - 2]
            var tip = curve.getLastCoordinate();
            var dx = center[0] - last[0];
            var dy = center[1] - last[1];
            var angle = Math.atan2(dy, dx) - (Math.PI / 2.0);
            var p1 = [center[0] + Math.cos(angle) * thickness,  center[1] + Math.sin(angle) * thickness];
            var p2 = [center[0] - Math.cos(angle) * thickness,  center[1] - Math.sin(angle) * thickness];
            var arrow = new ol.geom.Polygon([[tip, p1, p2, tip]]);
            var buffer = fnc_buffer([shortCurve, width], {});
            var union = fnc_union([arrow, buffer], {});
            return union;
        }
        else{
            return null;
        }
    }
    catch(e){
        return null;
    }
}

function getRGBAColor(color, alpha){
    if (color == null){
        return "rgba(0,0,0,0.0)";
    }
    tokens = color.split(",")
    var r,g,b,a;
    if (tokens.length == 4){
        r = tokens[0];
        g = tokens[1];
        b = tokens[2];
        a = tokens[3];
    }
    else{
        var bigint = parseInt(color.replace("#", ""), 16);
        r = (bigint >> 16) & 255;
        g = (bigint >> 8) & 255;
        b = bigint & 255;
        a = 255.0;
    }
    a = parseFloat(a) / 255.0;
    a = (alpha * a).toString();
    return "rgba(" +  [r, g, b, a].join(",") + ")";

}

function getFeatureAttribute(feature, attr){
    var value = feature.get(attr);
    if (value == null){
        return null;
    }
    else{
        return value;
    }
}