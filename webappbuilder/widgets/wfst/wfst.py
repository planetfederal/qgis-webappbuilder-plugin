from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Wfst(WebAppWidget):

    _parameters = {"showEditForm": False}

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(Button, {label: 'WFS-T', onTouchTap: this._toggleWFST.bind(this)})")
        app.panels.append(''' React.createElement("div", {id: 'wfst', ref: 'wfstPanel'},
                                      React.createElement(WFST, {showEditForm: %s, map: map})
                                    )''' % str(self._parameters["showEditForm"]).lower())
        self.addReactComponent(app, "WFST")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "edit.png")

    def description(self):
        return "WFS-T"
