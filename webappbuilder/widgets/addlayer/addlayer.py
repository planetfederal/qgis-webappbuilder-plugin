from webappbuilder.webbappwidget import WebAppWidget
from PyQt4.QtGui import QIcon

class AddLayer(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append("<ul className='pull-right' id='toolbar-add-layer'><AddLayer map={map} /></ul>")

    '''def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "add-layer.png"))'''

    def description(self):
        return "Add layer"