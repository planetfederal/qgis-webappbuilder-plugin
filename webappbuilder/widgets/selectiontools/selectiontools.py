from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class SelectionTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("<ul className='pull-right' id='toolbar-select'><Select toggleGroup='navigation' map={map}/></ul>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "selection-tool.png"))

    def description(self):
        return "Selection"