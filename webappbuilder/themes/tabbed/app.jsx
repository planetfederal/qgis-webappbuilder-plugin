import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import AppBar from 'material-ui/AppBar';
import Button from 'boundless-sdk/js/components/Button.jsx';
import {Tabs, Tab} from 'material-ui/Tabs';
import enMessages from 'boundless-sdk/locale/en.js';
import InfoPopup from 'boundless-sdk/js/components/InfoPopup.jsx';
import MapPanel from 'boundless-sdk/js/components/MapPanel.jsx';
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


class TabbedApp extends React.Component {
  getChildContext() {
    return {
      muiTheme: getMuiTheme()
    };
  }
  constructor(props) {
    super(props);
    this.state = {
      value: 1
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
  _toggleEdit() {
    this._toggle(document.getElementById('edit-tool-panel'));
  }
  _toggleWFST() {
    this._toggle(document.getElementById('wfst'));
  }
  handleChange(value) {
    if (value === parseInt(value, 10)) {
      this.setState({
        value: value,
      });
    }
  }
  render() {
    var toolbarOptions = @TOOLBAROPTIONS@;
    return React.createElement("div", {id: 'content'},
      React.createElement(AppBar, toolbarOptions @TOOLBAR@
      ),
      React.createElement("div", {className: 'row container'},
        React.createElement("div", {className: 'col tabs', id: 'tabs-panel'},
          React.createElement(Tabs, {value: this.state.value, onChange: this.handleChange.bind(this)}
            @TABS@
          )
        ),
        React.createElement("div", {className: 'col maps'},
          React.createElement(MapPanel, {id: 'map', map: map, extent: originalExtent, useHistory: @PERMALINK@}
            @MAPPANELS@
          )
          @PANELS@
        )
      )
    );
  }
}

TabbedApp.childContextTypes = {
  muiTheme: React.PropTypes.object
};

ReactDOM.render(<IntlProvider locale='en' messages={enMessages}><TabbedApp /></IntlProvider>, document.getElementById('main'));
