from builtins import str
import os
from qgis.PyQt.QtCore import QDir, QSize, Qt
from qgis.PyQt.QtGui import QIcon, QImage, QPainter
from qgis.core import (QgsLayoutItemLegend,
                       QgsLayoutItemShape,
                       QgsLayoutItemScaleBar,
                       QgsLayoutItemLabel,
                       QgsLayoutItemMap,
                       QgsLayoutItemPicture
                      )
from qgis.utils import iface
from webappbuilder.webbappwidget import WebAppWidget
from webappbuilder.utils import safeName
import json
import shutil
import uuid

class Print(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.writePrintFiles(appdef, folder, app, progress)
        app.tools.append("React.createElement(QGISPrint, {map:map, layouts:printLayouts, thumbnailPath: './resources/print/',})")
        self.addReactComponent(app, "QGISPrint")

    def description(self):
        return "Print"

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "print.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "print.png")

    def writePrintFiles(self, appdef, folder, app, progress):
        progress.setText("Writing print layout files")
        progress.setProgress(0)
        printFolder = os.path.join(folder, "resources", "print")
        if not QDir(printFolder).exists():
            QDir().mkpath(printFolder)
        dpis = [72, 150, 300]
        layoutDefs = []
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
            layoutDef["thumbnail"] = "%s_thumbnail.png" % layoutSafeName
            layoutDef["name"] = name
            layoutDef["elements"] = elements
            for item in list(composition.items()):
                element = None
                if isinstance(item, (QgsLayoutItemLegend, QgsLayoutItemShape, QgsLayoutItemScaleBar)):
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
                elif isinstance(item, QgsLayoutItemLabel):
                    element = getBasicInfo(item)
                    element["name"] = item.text()
                    element["size"] = item.font().pointSize()
                    element["font"] = item.font().rawName()
                elif isinstance(item, QgsLayoutItemMap):
                    element = getBasicInfo(item)
                    grid = item.grid()
                    if grid is not None:
                        element["grid"] = {}
                        element["grid"]["intervalX"] = grid.intervalX()
                        element["grid"]["intervalY"] = grid.intervalY()
                        element["grid"]["crs"] = grid.crs().authid()
                        element["grid"]["annotationEnabled"] = grid.annotationEnabled()
                elif isinstance(item, QgsLayoutItemPicture):
                    filename = os.path.basename(item.picturePath())
                    if os.path.exists(filename):
                        element = getBasicInfo(item)
                        shutil.copy(item.pictureFile(), os.path.join(printFolder, filename))
                        element["file"] = filename
                if element is not None:
                    element["type"] = item.__class__.__name__[11:].lower()
                    elements.append(element)

            layoutDefs.append(layoutDef)
            progress.setProgress(int((i+1)*100.0/len(composers)))

        app.variables.append("var printLayouts = %s;" % json.dumps(layoutDefs))

    def checkProblems(self, appdef, problems):
        composers = iface.activeComposers()
        if len(composers) == 0:
            problems.append("Print widget has been added to the web app, but no print composer is defined in the current project")
