from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Query(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append("<UI.Tab eventKey={3} title='Query'><div id='query-panel' className='query-panel'><QueryBuilder map={map} /></div></UI.Tab>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def description(self):
        return "Query"