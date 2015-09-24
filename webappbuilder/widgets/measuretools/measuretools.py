from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class MeasureTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("<ul className='pull-right' id='toolbar-measure'><Measure toggleGroup='navigation' map={map}/></ul>")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def description(self):
        return "Measure"