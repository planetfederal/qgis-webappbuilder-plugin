from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("edit.js", folder, app)
        self.addCss("edit.css", folder, app)
        app.tools.append('<li><a onclick="showEditPanel()" href="#"><i class="glyphicon glyphicon-pencil"></i>Edit</a></li>')
        app.mappanels.append('''<div class="edit-tool-panel" id="edit-tool-panel">
                                 <form class="form-inline">
                                  <div class="input-group" style="">
                                   <span class="input-group-addon">
                                    Layer
                                   </span>
                                   <select class="form-control" id="edit-layer">
                                   </select>
                                   </div>
                                   <a class="btn btn-primary" href="#" id="btn-add-empty-layer">
                                    Create new empty layer
                                   </a>
                                   <a class="btn btn-default" href="#" id="btn-edit-tool">
                                    <i class="glyphicon glyphicon-edit"></i>
                                   </a>
                                   <a class="btn btn-default" href="#" id="btn-close-edit">
                                    Close
                                   </a>
                                 </form>
                            </div>''')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def description(self):
        return "Edit"