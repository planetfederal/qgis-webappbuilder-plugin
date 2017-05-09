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

var TabbedApp = React.createClass({
  childContextTypes: {
    muiTheme: React.PropTypes.object
  },
  getChildContext: function() {
    return {
      muiTheme: getMuiTheme()
    };
  },
  getInitialState: function() {
    return {leftNavOpen: true, addLayerOpen: false};
  },
  componentDidMount: function() {
    @POSTTARGETSET@
  },
  leftNavClose: function(value) {
    this.setState({
      leftNavOpen: false
    }, function() {
      map.updateSize();
    });
  },
  leftNavOpen: function(value) {
    this.setState({
      leftNavOpen: true
    }, function() {
      map.updateSize();
    });
  },
  layerListOpen: function(value) {
    this.setState({
      addLayerOpen: true
    });
  },
  layerListClose: function(value) {
    this.setState({
      addLayerOpen: false
    });
  },
  _toggle: function(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  },
  _toggleEdit: function() {
    this._toggle(document.getElementById('edit-tool-panel'));
  },
  _toggleWFST: function() {
    this._toggle(document.getElementById('wfst'));
  },
  render: function() {
    var toolbarOptions = Object.assign({onLeftIconTouchTap: this.leftNavOpen}, @TOOLBAROPTIONS@);
    return React.createElement("div", {id: 'content'},
      React.createElement(Header, toolbarOptions @TOOLBAR@
      ),
      React.createElement("div", {className: 'row container'},
        React.createElement("div", {className: 'col tabs', id: 'tabs-panel'},
          React.createElement(LeftNav, {tabList: [@TABS@], open: this.state.leftNavOpen, onRequestClose: this.leftNavClose})
        ),
        React.createElement("div", {className: 'col maps'},
          React.createElement(MapPanel, {id: 'map', useHistory: @PERMALINK@, extent: originalExtent, map: map}
            @MAPPANELS@
          )
          @PANELS@
        )
      )
    );
  }
});

ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(TabbedApp)), document.getElementById('main'));
