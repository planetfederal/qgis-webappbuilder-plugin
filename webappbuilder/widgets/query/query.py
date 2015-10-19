from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Query(WebAppWidget):

    order = 4

    def write(self, appdef, folder, app, progress):
        app.imports.append("import QueryBuilder from './components/QueryBuilder.jsx';")
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append("<UI.Tab eventKey={%i} title='Query'><div id='query-panel' className='query-panel'>" % idx
                              + "<QueryBuilder map={map} /></div></UI.Tab>")
        else:
            app.mappanels.append("<div id='query-panel' className='query-panel'><QueryBuilder map={map} /></div>")
            app.tools.append("<ul className='pull-right' id='toolbar-query'><BUTTON.DefaultButton onClick={this._toggleQuery.bind(this)}><ICON.Icon name='filter' /> Query</BUTTON.DefaultButton></ul>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def description(self):
        return "Query"