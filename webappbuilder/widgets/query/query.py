from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Query(WebAppWidget):

    order = 4

    def write(self, appdef, folder, app, progress):
        idx = len(app.panels) + 1
        app.panels.append("<UI.Tab eventKey={%i} title='Query'><div id='query-panel' className='query-panel'>" % idx
                          + "<QueryBuilder map={map} /></div></UI.Tab>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def description(self):
        return "Query"