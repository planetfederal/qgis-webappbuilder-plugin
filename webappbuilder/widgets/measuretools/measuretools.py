from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class MeasureTools(WebAppWidget):

    _parameters = {"geodesic": True}

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(Measure, {toggleGroup:'navigation', map:map, geodesic:%s})"
                         % str(self.parameters["geodesic"]).lower())
        self.addReactComponent(app, "Measure")

        nav = '''React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})'''
        if nav not in app.tools:
            app.tools.append(nav)
            self.addReactComponent(app, "Navigation")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "measure-tool.png")

    def description(self):
        return "Measure"
