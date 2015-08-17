from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Query(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.addScript("filtrex.js", folder, app)
        self.addScript("query.js", folder, app)
        self.addCss("query.css", folder, app)
        app.tools.append('<li><a onclick="showQueryPanel()" href="#"><i class="glyphicon glyphicon-filter"></i>Query</a></li>')
        app.mappanels.append('''<div class="query-panel" id="query-panel">
                                <form class="form-horizontal">
                                    <div style="margin-bottom: 25px" class="input-group">
                                        <span class="input-group-addon">Layer</span>
                                        <select id="query-layer" class="form-control"></select>
                                    </div>
                                    <div style="margin-bottom: 25px" class="input-group">
                                        <span class="input-group-addon">Filter </span>
                                        <input id="query-expression" type="text" class="form-control" placeholder="Type expression...">
                                        <span class="input-group-addon">
                                        <a href="https://github.com/joewalnes/filtrex#expressions" target="_blank">
                                            Help
                                        </a></span>
                                    </div>
                                   <div style="margin-top:10px" class="form-group">
                                        <div class="col-sm-12 controls">
                                          <a id="btn-query-new" href="#" class="btn btn-primary">New selection</a>
                                          <a id="btn-query-add" href="#" class="btn btn-primary">Add to current selection</a>
                                          <a id="btn-query-in" href="#" class="btn btn-primary">Select in current selection</a>
                                          <a id="btn-close-query" href="#" class="btn btn-default">Close</a>
                                        </div>
                                    </div>
                                </form>
                            </div>''')


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "query.png"))

    def description(self):
        return "Query"