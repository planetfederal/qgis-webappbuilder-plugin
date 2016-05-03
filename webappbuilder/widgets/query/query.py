from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Query(WebAppWidget):

    order = 4

    def write(self, appdef, folder, app, progress):
        self.addReactComponent(app, "QueryBuilder")
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append("<UI.Tab eventKey={%i} title='Query'><div id='query-panel' className='query-panel'>" % idx
                              + "<QueryBuilder map={map} /></div></UI.Tab>")
        else:
            app.tools.append("React.createElement(RaisedButton, {label: 'Query', onTouchTap: this._toggleQuery})")
            app.mappanels.append('''React.createElement("div", {id: 'query-panel', className:'query-panel'},
                                          React.createElement(QueryBuilder, {map: map})
                                        )''')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def description(self):
        return "Query"