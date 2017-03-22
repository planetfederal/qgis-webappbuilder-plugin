from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class SelectionTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('''React.createElement(Select, {toggleGroup: 'navigation', map:map})''')
        nav = '''React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})'''
        if nav not in app.tools:
            app.tools.append(nav)

        self.addReactComponent(app, "Select")
        self.addReactComponent(app, "Navigation")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "selection-tool.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "selection-tool.png")

    def description(self):
        return "Selection"
