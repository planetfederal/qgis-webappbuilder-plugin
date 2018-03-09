from webappbuilder.webbappwidget import WebAppWidget
import os
from qgis.PyQt.QtGui import QIcon

class DrawFeature(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('''React.createElement(DrawFeature, {toggleGroup: 'navigation', map: map})''')
        app.panels.append('''React.createElement("div", {id: 'editpopup', className: 'ol-popup'},
                                React.createElement(EditPopup, {toggleGroup: 'navigation', map: map})
                            )''')
        self.addReactComponent(app, "DrawFeature")
        self.addReactComponent(app, "EditPopup")

        nav = '''React.createElement(Navigation, {toggleGroup: 'navigation', secondary: true})'''
        if nav not in app.tools:
            app.tools.append(nav)
            self.addReactComponent(app, "Navigation")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "edit.png")

    def description(self):
        return "Draw feature"
