from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import shutil

class AddLayer(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('<li><a onclick="addLayerFromFile()" href="#"><i class="glyphicon glyphicon-open"></i>Add layer</a></li>')
        self.addScript("addlayer.js", folder, app)
        self.addScript("bootbox.min.js", folder, app)
        app.scripts.append('<script src="./resources/colorpicker/js/bootstrap-colorpicker.min.js"></script>')
        app.scripts.append('<link href="./resources/colorpicker/css/bootstrap-colorpicker.min.css" rel="stylesheet" type="text/css"/>')
        dst = os.path.join(folder, "resources", "colorpicker")
        colorpickerFolder = os.path.join(os.path.dirname(__file__), "colorpicker")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(colorpickerFolder, dst)

    '''def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "add-layer.png"))'''

    def description(self):
        return "Add layer"