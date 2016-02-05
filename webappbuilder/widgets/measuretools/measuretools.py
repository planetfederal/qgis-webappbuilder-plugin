from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class MeasureTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        pullRight = "" if len(app.tools) else "pullRight"
        app.tools.append("<ul className='pull-right' id='toolbar-measure'><Measure toggleGroup='navigation' map={map} %s/></ul>" % pullRight)
        app.toolsjs.append('''React.createElement("ul", {id:'toolbar-measure', className:'pull-right'},
                                    React.createElement(Measure, {toggleGroup:'navigation', map:map})
                                  )''')
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "measure-tool.png"))

    def description(self):
        return "Measure"