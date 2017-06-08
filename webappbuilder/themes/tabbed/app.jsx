import React from 'react';
import ReactDOM from 'react-dom';
import ol from 'openlayers';
import {IntlProvider} from 'react-intl';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import Header from '@boundlessgeo/sdk/components/Header';
import Button from '@boundlessgeo/sdk/components/Button';
import {Tab} from 'material-ui/Tabs';
import LeftNav from '@boundlessgeo/sdk/components/LeftNav';
import IconMenu from 'material-ui/IconMenu';
import MenuItem from 'material-ui/MenuItem';
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

class TabbedApp extends React.Component {
  getChildContext() {
    return {
      muiTheme: getMuiTheme()
    };
  }
  constructor(props) {
    super(props);
    this.state = {
      leftNavOpen: false,
      addLayerOpen: false
    };
  }
  componentDidMount() {
    @POSTTARGETSET@
  }
  leftNavClose(value) {
    this.setState({
      leftNavOpen: false
    }, function() {
      map.updateSize();
    });
  }
  leftNavOpen(value) {
    this.setState({
      leftNavOpen: true
    }, function() {
      map.updateSize();
    });
  }
  layerListOpen(value) {
    this.setState({
      addLayerOpen: true
    });
  }
  layerListClose(value) {
    this.setState({
      addLayerOpen: false
    });
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
    var leftNavWidth = 360;
    var toolbarOptions = Object.assign({
      style: {left: this.state.leftNavOpen ? leftNavWidth : 0, width: this.state.leftNavOpen ? 'calc(100% - ' + leftNavWidth + 'px)' : '100%'},
      showLeftIcon: !this.state.leftNavOpen,
      onLeftIconTouchTap: this.leftNavOpen.bind(this)
    }, @TOOLBAROPTIONS@);
    return React.createElement("div", {id: 'content'},
      React.createElement(LeftNav, {tabList: [@TABS@], open: this.state.leftNavOpen, onRequestClose: this.leftNavClose.bind(this)}),
      React.createElement("div", undefined,
        React.createElement(Header, toolbarOptions @TOOLBAR@),
        React.createElement("div", {className: 'map', style: {left: this.state.leftNavOpen ? leftNavWidth : 0, width: this.state.leftNavOpen ? 'calc(100% - ' + leftNavWidth + 'px)' : '100%'}},
          React.createElement(MapPanel, {id: 'map', useHistory: @PERMALINK@, extent: originalExtent, map: map}
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
