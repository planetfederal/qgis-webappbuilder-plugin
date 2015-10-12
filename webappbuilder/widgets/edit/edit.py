from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("<ul className='pull-right' id='toolbar-edit'><UI.DefaultButton "
        + "onClick={this._toggleEdit.bind(this)}><Icon.Icon name='pencil' /> Edit</UI.DefaultButton></ul>")
        app.mappanels.append("<div id='edit-tool-panel'><Edit toggleGroup='navigation' map={map} /></div>")

    '''def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))'''

    def description(self):
        return "Edit"