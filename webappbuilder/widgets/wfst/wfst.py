import os
from qgis.PyQt.QtGui import QIcon
from webappbuilder.webbappwidget import WebAppWidget

class Wfst(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(Button, {label: 'WFS-T', onTouchTap: this._toggleWFST.bind(this)})")
        app.panels.append(''' React.createElement("div", {id: 'wfst', ref: 'wfstPanel'},
                                      React.createElement(WFST, {map: map})
                                    )''')
        self.addReactComponent(app, "WFST")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "edit.png")

    def description(self):
        return "WFS-T"
