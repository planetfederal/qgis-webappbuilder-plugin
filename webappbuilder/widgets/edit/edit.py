from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("<ul className='pull-right' id='toolbar-edit'><BUTTON.DefaultButton "
                         + "onClick={this._toggleEdit.bind(this)}><ICON.Icon name='pencil' /> "
                         + "Edit</BUTTON.DefaultButton></ul>")
        app.mappanels.append("<div id='edit-tool-panel'><Edit toggleGroup='navigation' map={map} /></div>")
        self.addReactComponent(app, "Edit")

    '''def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))'''

    def description(self):
        return "Edit"