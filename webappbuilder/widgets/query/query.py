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
            app.tabs.append("<Tab value={%i} label='Query'><div id='query-panel' className='query-panel'>" % idx
                              + "<QueryBuilder map={map} /></div></Tab>")
        else:
            app.tools.append("React.createElement(Button, {label: 'Query', onTouchTap: this._toggleQuery.bind(this)})")
            app.mappanels.append('''React.createElement("div", {id: 'query-panel', className:'query-panel'},
                                          React.createElement(QueryBuilder, {map: map})
                                        )''')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "query.png")

    def description(self):
        return "Query"
