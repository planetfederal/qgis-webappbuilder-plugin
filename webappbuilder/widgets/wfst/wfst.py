from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Wfst(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(RaisedButton, {label: 'WFS-T', onTouchTap: this._toggleWFST})")
        app.panels.append(''' React.createElement("div", {id: 'wfst', ref: 'wfstPanel'},
                                      React.createElement(WFST, {map: map})
                                    )''')
        self.addReactComponent(app, "Edit")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "edit.png")

    def description(self):
        return "WFS-T"
