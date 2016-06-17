from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("React.createElement(RaisedButton, {label: 'Edit', onTouchTap: this._toggleEdit})")
        app.mappanels.append(''' React.createElement("div", {id: 'edit-tool-panel'},
                                      React.createElement(Edit, {map: map, toggleGroup:'navigation'})
                                    )''')
        self.addReactComponent(app, "Edit")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "edit.png")

    def description(self):
        return "Edit"
