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
  getInitialState() {
    return {value: 1};
  },
  componentDidMount() {
    @POSTTARGETSET@
  },
  _navigationFunc() {
    ToolActions.activateTool(null, 'navigation');
  },
  _toggle(el) {
    if (el.style.display === 'block') {
      el.style.display = 'none';
    } else {
      el.style.display = 'block';
    }
  },
  _toggleEdit() {
    this._toggle(document.getElementById('edit-tool-panel'));
  },
  _toggleWFST() {
    this._toggle(document.getElementById('wfst'));
  },
  handleChange(value) {
    if (value === parseInt(value, 10)) {
      this.setState({
        value: value,
      });
    }
  },
  render() {
    var toolbarOptions = @TOOLBAROPTIONS@;
    return React.createElement("div", {id: 'content'},
      React.createElement(AppBar, toolbarOptions
        @TOOLBAR@
      ),
      React.createElement("div", {className: 'row container'},
        React.createElement("div", {className: 'col tabs', id: 'tabs-panel'},
          React.createElement(Tabs, {value: this.state.value, onChange: this.handleChange}
            @TABS@
          )
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
