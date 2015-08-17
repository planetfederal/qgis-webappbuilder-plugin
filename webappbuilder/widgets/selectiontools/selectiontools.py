from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class SelectionTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        selectTools = []
        selectTools.append(["removeSelectionTool()", "No selection tool (zoom/pan)"])
        selectTools.append(["selectByPolygon()", "Select by polygon"])
        selectTools.append(["selectByRectangle()", "Select by rectangle"])
        li = "\n".join(['<li><a onclick="%s" href="#">%s</a></li>' % (sel[0], sel[1]) for sel in selectTools])
        app.tools.append('''<li class="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        Selection <span class="caret"><span></a>
                        <ul class="dropdown-menu">
                          %s
                        </ul>
                      </li>''' % li)
        self.addScript("selectiontools.js", folder, app)


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "selection-tool.png"))

    def description(self):
        return "Selection"