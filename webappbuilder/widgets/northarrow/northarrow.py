from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class NorthArrow(WebAppWidget):

    buttonIndex = 0
    buttonArea = WebAppWidget.BUTTON_AREA_LEFT
    cssName = "rotate-button"
    
    _parameters = {"autoHide": False}

    def write(self, appdef, folder, app, progress):
        def p(name):
            return str(self._parameters[name]).lower()
        app.panels.append('''React.createElement("div", {id:'rotate-button'},
                                    React.createElement(Rotate, {
                                    autoHide:%s,
                                    map: map,
                                    tooltipPosition: 'bottom-left'})
                                  )''' % (p("autoHide")))
        self.addReactComponent(app, "Rotate")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "north-arrow.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "north-arrow.png")

    def description(self):
        return "North"
