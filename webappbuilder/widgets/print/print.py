from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon, QImage, QPainter
from PyQt4.Qt import QDir, QSize, Qt
from qgis.core import *
import json
from qgis.utils import iface
import shutil
from webappbuilder.utils import safeName
import uuid

class Print(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.writePrintFiles(appdef, folder, progress)
        li = "\n".join(['''<li><img style=" border:1px solid #333333;" src="print/%(safename)s_thumbnail.png"/>
                            <a onclick="printMap('%(name)s')" href="#">%(name)s</a></li>
                            <li class="nav-divider"></li>'''
                        % {"name": c.composerWindow().windowTitle(),
                           "safename": safeName(c.composerWindow().windowTitle())}
                                for c in iface.activeComposers()])
        app.tools.append('''<li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <i class="glyphicon glyphicon-print"></i> Print
            <span class="caret"><span></a>
            <ul class="dropdown-menu" style="text-align:center;">
              %s
            </ul>
          </li>''' % li)
        app.scriptsBottom.append('<script src="print/layouts.js"></script>')
        self.addScript("bootbox.min.js", folder, app)
        self.addScript("jspdf.min.js", folder, app)
        self.addScript("print.js", folder, app)


    def description(self):
        return "Print"

    def writePrintFiles(self, appdef, folder, progress):
        progress.setText("Writing print layout files")
        progress.setProgress(0)
        printFolder = os.path.join(folder, "print")
        if not QDir(printFolder).exists():
            QDir().mkpath(printFolder)
        dpis = [72, 150, 300]
        layoutDefs = {}
        def getBasicInfo(item):
            coords = {}
            pos = item.pos()
            coords["x"] = pos.x()
            coords["y"] = pos.y()
            rect = item.rect()
            coords["width"] = rect.width()
            coords["height"] = rect.height()
            coords["id"] = str(uuid.uuid4())
            return coords
        composers = iface.activeComposers()
        for i, composer in enumerate(composers):
            name = composer.composerWindow().windowTitle()
            layoutSafeName = safeName(name)
            layoutDef = {}
            composition = composer.composition()
            img = composition.printPageAsRaster(0)
            img = img.scaledToHeight(100, Qt.SmoothTransformation)
            img.save(os.path.join(printFolder, "%s_thumbnail.png" % layoutSafeName))
            layoutDef["width"] = composition.paperWidth()
            layoutDef["height"] = composition.paperHeight()
            elements = []
            layoutDef["elements"] = elements
            for item in composition.items():
                element = None
                if isinstance(item, (QgsComposerLegend, QgsComposerShape, QgsComposerScaleBar, QgsComposerArrow)):
                    element = getBasicInfo(item)
                    for dpi in dpis:
                        dpmm = dpi / 25.4
                        s = QSize(item.rect().width() * dpmm, item.rect().height() * dpmm)
                        img = QImage(s, QImage.Format_ARGB32_Premultiplied)
                        img.fill(Qt.transparent)
                        painter = QPainter(img)
                        painter.scale(dpmm, dpmm)
                        item.paint(painter, None, None)
                        painter.end()
                        img.save(os.path.join(printFolder, "%s_%s_%s.png" %
                                (layoutSafeName, element["id"], str(dpi))))
                elif isinstance(item, QgsComposerLabel):
                    element = getBasicInfo(item)
                    element["name"] = item.text()
                    element["size"] = item.font().pointSize()
                    element["font"] = item.font().rawName()
                elif isinstance(item, QgsComposerMap):
                    element = getBasicInfo(item)
                    grid = item.grid()
                    if grid is not None:
                        element["grid"] = {}
                        element["grid"]["intervalX"] = grid.intervalX()
                        element["grid"]["intervalY"] = grid.intervalY()
                        element["grid"]["crs"] = grid.crs().authid()
                        element["grid"]["annotationEnabled"] = grid.annotationEnabled()
                elif isinstance(item, QgsComposerPicture):
                    element = getBasicInfo(item)
                    filename = os.path.basename(item.picturePath())
                    shutil.copy(item.pictureFile(), os.path.join(printFolder, filename))
                    element["file"] = filename
                if element is not None:
                    element["type"] = item.__class__.__name__[11:].lower()
                    elements.append(element)

            layoutDefs[name] = layoutDef
            progress.setProgress(int((i+1)*100.0/len(composers)))

        with open(os.path.join(printFolder, "layouts.js"), "w") as f:
            f.write("var printLayouts = %s;" % json.dumps(layoutDefs))
