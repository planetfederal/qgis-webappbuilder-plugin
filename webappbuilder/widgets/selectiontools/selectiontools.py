from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class SelectionTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('''React.createElement(Select, {toggleGroup: 'navigation', map:map})''')
        app.tools.append('''React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})''')

        self.addReactComponent(app, "Select")
        self.addReactComponent(app, "Navigation")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "selection-tool.png"))

    def description(self):
        return "Selection"
