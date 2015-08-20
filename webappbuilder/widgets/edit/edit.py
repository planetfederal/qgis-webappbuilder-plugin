from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import shutil

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("edit.js", folder, app)
        self.addCss("edit.css", folder, app)
        app.scripts.append('<script src="./resources/colorpicker/js/bootstrap-colorpicker.min.js"></script>')
        app.scripts.append('<link href="./resources/colorpicker/css/bootstrap-colorpicker.min.css" rel="stylesheet" type="text/css"/>')
        dst = os.path.join(folder, "resources", "colorpicker")
        colorpickerFolder = os.path.join(os.path.dirname(__file__), "colorpicker")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(colorpickerFolder, dst)
        app.tools.append('<li><a onclick="showEditPanel()" href="#"><i class="glyphicon glyphicon-pencil"></i>Edit</a></li>')
        app.mappanels.append('''<div class="edit-tool-panel" id="edit-tool-panel">
                                  <form class="form-inline">
                                   <div class="input-group">
                                    <div class="input-group-addon">
                                     Layer
                                    </div>
                                    <select class="form-control" id="edit-layer">
                                    </select>
                                    <div class="input-group-addon">
                                     <a href="#" id="btn-add-empty-layer">
                                      <i class="glyphicon glyphicon-plus">
                                      </i>
                                     </a>
                                    </div>
                                   </div>
                                   <a class="btn btn-primary" href="#" id="btn-edit-tool">
                                    Enable edit mode
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