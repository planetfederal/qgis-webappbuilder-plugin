@VARIABLES@

var map = new ol.Map({
  layers: layersList,
  view: view,
  controls: [@OL3CONTROLS@]
});


class TabbedApp extends React.Component {
  componentDidMount() {
    map.setTarget(document.getElementById('map'));
    map.getView().fit(originalExtent, map.getSize());
    @POSTTARGETSET@
  }
  _navigationFunc() {
    LayerActions.activateTool(null, 'navigation');
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
  render() {
    return (
      <article>
        <nav role='navigation'>
          <div className='toolbar'>
            @LOGO@
            <a className="navbar-brand" href="#">@TITLE@</a>
            @TOOLBAR@
          </div>
        </nav>
        <div id='content'>
          <div className='row full-height'>
            <div className='col-md-8 full-height' id='tabs-panel'>
              <UI.SimpleTabs defaultActiveKey={1}>
                @PANELS@
              </UI.SimpleTabs>
            </div>
            <div className='col-md-16 full-height'>
              <div id='map'>
                  @MAPPANELS@
                  <div id='popup' className='ol-popup'><InfoPopup map={map} hover={@POPUPEVENT@}/></div>
              </div>
              @CONTROLS@
            </div>
          </div>
        </div>
      </article>
    );
  }
}


React.render(<IntlProvider locale='en' >{() => (<TabbedApp />)}</IntlProvider>, document.body);



