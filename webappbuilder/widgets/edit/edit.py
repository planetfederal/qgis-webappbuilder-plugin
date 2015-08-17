from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Edit(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("query.js", folder, app)
        app.tools.append('<li><a onclick="showEditPanel()" href="#"><i class="glyphicon glyphicon-pencil"></i>Query</a></li>')
        app.mappanels.append('''<div class="edit-tool-panel" id="edit-tool-panel">
                                <form class="form-horizontal">
                                    <div style="margin-bottom: 25px" class="input-group">
                                        <span class="input-group-addon">Layer</span>
                                        <select id="query-layer" class="form-control"></select>
                                        <a id="btn-add-empty-layer" href="#" class="btn btn-primary">Add new empty layer</a>
                                        <a id="btn-edit-tool" href="#" class="btn btn-primary">Edit</a>
                                        <a id="btn-close-query" href="#" class="btn btn-default">Close</a>
                                    </div>
                                </form>
                            </div>''')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def description(self):
        return "Edit"