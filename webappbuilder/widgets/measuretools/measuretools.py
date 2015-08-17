from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class MeasureTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Measure <span class="caret"><span> </a>
                            <ul class="dropdown-menu">
                              <li><a onclick="measureTool('distance')" href="#">Distance</a></li>
                              <li><a onclick="measureTool('area')" href="#">Area</a></li>
                              <li><a onclick="measureTool(null)" href="#">Remove measurements</a></li>
                            </ul>
                          </li>''')
        self.addScript("measure.js", folder, app)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def description(self):
        return "Measure"