from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class HomeButton(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.panels.append('''React.createElement("div", {id:'home-button'},
                                    React.createElement(HomeButton, {tooltipPosition: 'bottom-right', map:map})
                                  )''')
        self.addReactComponent(app, "HomeButton")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "home.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "home.png")

    def description(self):
        return "Home"
