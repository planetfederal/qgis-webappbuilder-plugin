import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class AddLayer(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addReactComponent(app, "AddLayer")
        app.tools.append("React.createElement(AddLayer, {map:map})")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "add-layer.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "add-layer.png")

    def description(self):
        return "Add layer"
