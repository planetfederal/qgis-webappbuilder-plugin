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
  componentDidMount() {
    map.setTarget(ReactDOM.findDOMNode(this.refs.map));
    view = map.getView();
    view.fit(originalExtent, map.getSize());
    if (window.location.hash !== '') {
      var hash = window.location.hash.replace('#map=', '');
      var parts = hash.split('/');
      if (parts.length === 4) {
        var zoom = parseInt(parts[0], 10);
        var center = [
          parseFloat(parts[1]),
          parseFloat(parts[2])
        ];
        var rotation = parseFloat(parts[3]);
        view.setZoom(zoom);
        view.setCenter(center);
        view.setRotation(rotation);
      }
    }
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
  render() {
     return React.createElement("article", null,
       React.createElement("nav", {role: 'navigation'},
         React.createElement("div", {className: 'toolbar'},
           @LOGO@
           React.createElement("a", {className: 'navbar-brand', href: '#'}, '@TITLE@')
           @TOOLBAR@
         )
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
});


ReactDOM.render(React.createElement(IntlProvider, {locale: 'en'}, React.createElement(TabbedApp)), document.getElementById('main'));


