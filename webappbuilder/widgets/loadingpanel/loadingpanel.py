from webappbuilder.webbappwidget import WebAppWidget
from qgis.PyQt.QtGui import QIcon
import os

class LoadingPanel(WebAppWidget):

    _parameters = {}

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement(LoadingPanel, {map:map})''')
        self.addReactComponent(app, "LoadingPanel")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "refresh.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "refresh.png")

    def description(self):
        return "Loading panel"
