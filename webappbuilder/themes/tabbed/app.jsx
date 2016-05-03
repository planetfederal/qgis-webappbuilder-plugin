import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import UI from 'pui-react-buttons';
import Icon from 'pui-react-iconography';
import enMessages from './node_modules/boundless-sdk/locale/en.js';
import InfoPopup from './node_modules/boundless-sdk/js/components/InfoPopup.jsx';
import Toolbar from './node_modules/boundless-sdk/js/components/Toolbar.jsx';
import App from './node_modules/boundless-sdk/js/components/App.js';
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


class TabbedApp extends App {
  componentDidMount() {
    super.componentDidMount();
    @POSTTARGETSET@
  }
  _navigationFunc() {
    ToolActions.activateTool(null, 'navigation');
  }
  _toggle(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  }
  _toggleEdit() {
    this._toggle(document.getElementById('edit-tool-panel'));
  }
  _toggleWFST() {
    this._toggle(document.getElementById('wfst'));
  }
  render() {
    var toolbarOptions = @TOOLBAROPTIONS@;
    return React.createElement("article", null,
       React.createElement(AppBar, toolbarOptions,
       @TOOLBAR@
       ),
       React.createElement("div", {id: 'content'},
         React.createElement("div", {className: 'row full-height'},
           React.createElement("div", {className: 'col-md-8 full-height', id: 'tabs-panel'},
             React.createElement(UI.SimpleTabs, {defaultActiveKey: 1}
                @TABS@
              )
            ),
           React.createElement("div", {className: 'col-md-16 full-height'},
              React.createElement("div", {id: 'content'},
                React.createElement("div", {id: 'map', ref: 'map'}
                  @MAPPANELS@
                )
                @PANELS@
              )
           )
        )
      )
    );
  }
}

ReactDOM.render(<IntlProvider locale='en' messages={enMessages}><TabbedApp map={map} extent={originalExtent} useHistory={@PERMALINK@} /></IntlProvider>, document.getElementById('main'));

