import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
import Button from '@boundlessgeo/sdk/components/Button';
import Header from '@boundlessgeo/sdk/components/Header';
import enMessages from '@boundlessgeo/sdk/locale/en';
import InfoPopup from '@boundlessgeo/sdk/components/InfoPopup';
import MapPanel from '@boundlessgeo/sdk/components/MapPanel';
import {ToolbarGroup, ToolbarSeparator} from 'material-ui/Toolbar';

@IMPORTS@
import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// Can go away when react 1.0 release
// Check this repo:
// https://github.com/zilverline/react-tap-event-plugin
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


@VARIABLES@

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: [@OL3CONTROLS@]
});

@AFTERMAP@

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

class BasicApp extends React.Component {
  getChildContext() {
    return {
      muiTheme: getMuiTheme()
    };
  }
  componentDidMount() {
    @POSTTARGETSET@
  }
  _toggle(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  }
  _toggleTable() {
    this._toggle(document.getElementById('table-panel'));
    this.refs.table.getWrappedInstance().setDimensionsOnState();
  }
  _toggleWFST() {
    this._toggle(document.getElementById('wfst'));
  }
  _toggleQuery() {
    this._toggle(document.getElementById('query-panel'));
  }
  _toggleEdit() {
    this._toggle(document.getElementById('edit-tool-panel'));
  }
  _hideAboutPanel(evt) {
    evt.preventDefault();
    document.getElementById('about-panel').style.display = 'none';
  }
  _toggleChartPanel(evt) {
    evt.preventDefault();
    this._toggle(document.getElementById('chart-panel'));
  }
  render() {
    var toolbarOptions = @TOOLBAROPTIONS@;
    return React.createElement("article", null,
      React.createElement(Header, toolbarOptions @TOOLBAR@),
      React.createElement("div", {id: 'content'},
        React.createElement(MapPanel, {id: 'map', map: map, extent: originalExtent, useHistory: @PERMALINK@}
          @MAPPANELS@
        )
        @PANELS@
      )
    );
  }
}

BasicApp.childContextTypes = {
  muiTheme: React.PropTypes.object
};

ReactDOM.render(<IntlProvider locale='en' messages={enMessages}><BasicApp /></IntlProvider>, document.getElementById('main'));
