from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class MeasureTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("{jsx: React.createElement(Measure, {toggleGroup:'navigation', map:map})}")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def description(self):
        return "Measure"