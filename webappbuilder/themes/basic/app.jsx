import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import UI from 'pui-react-buttons';
import Icon from 'pui-react-iconography';
import InfoPopup from './node_modules/boundless-sdk/js/components/InfoPopup.jsx';
import Toolbar from './node_modules/boundless-sdk/js/components/Toolbar.jsx';
import App from './node_modules/boundless-sdk/js/components/App.js';
@IMPORTS@

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



class BasicApp extends React.Component {
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
    this.refs.table.refs.wrappedElement.setDimensionsOnState();
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
    var options = [@TOOLBAR@];
    return React.createElement("article", null,
      React.createElement(Toolbar, {options: options}
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


ReactDOM.render(<IntlProvider locale='en'><BasicApp map={map} extent={originalExtent} useHistory={@PERMALINK@}/></IntlProvider>, document.getElementById('main'));



