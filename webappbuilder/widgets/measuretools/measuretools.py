import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class MeasureTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(Measure, {toggleGroup:'navigation', map:map})")
        self.addReactComponent(app, "Measure")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "measure-tool.png")

    def description(self):
        return "Measure"
