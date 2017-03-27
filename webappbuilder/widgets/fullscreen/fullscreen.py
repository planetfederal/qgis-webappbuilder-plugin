from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class FullScreen(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement("div", {id:'fullscreen-button'},
                                    React.createElement(Fullscreen, {map:map})
                                  )''')
        self.addReactComponent(app, "Fullscreen")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "full-screen.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "full-screen.png")

    def description(self):
        return "Full screen"
