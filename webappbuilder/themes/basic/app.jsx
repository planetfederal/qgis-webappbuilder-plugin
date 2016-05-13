import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import AppBar from 'material-ui/lib/app-bar';
import RaisedButton from 'material-ui/lib/raised-button';
import enMessages from 'boundless-sdk/locale/en.js';
import InfoPopup from 'boundless-sdk/js/components/InfoPopup.jsx';
import App from 'boundless-sdk/js/components/App.js';
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



class BasicApp extends App {
  componentDidMount() {
    super.componentDidMount();
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
  _toggleAboutPanel() {
    this._toggle(document.getElementById('about-panel'));
  }
  _toggleChartPanel(evt) {
    evt.preventDefault();
    this._toggle(document.getElementById('chart-panel'));
  }
  _navigationFunc() {
    ToolActions.activateTool(null, 'navigation');
  }
  render() {
    var toolbarOptions = @TOOLBAROPTIONS@;
    return React.createElement("article", null,
       React.createElement(AppBar, toolbarOptions
       @TOOLBAR@
       ),
      React.createElement("div", {id: 'content'},
        React.createElement("div", {id: 'map', ref: 'map'}
          @MAPPANELS@
        )
        @PANELS@
      )
    );
  }
}


ReactDOM.render(<IntlProvider locale='en' messages={enMessages}><BasicApp map={map} extent={originalExtent} useHistory={@PERMALINK@}/></IntlProvider>, document.getElementById('main'));



