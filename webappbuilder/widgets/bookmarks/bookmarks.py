from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json
from ui_bookmarksdialog import Ui_BookmarksDialog

SHOW_BOOKMARKS_IN_PANEL_GO = 0
SHOW_BOOKMARKS_IN_PANEL_PAN = 1
SHOW_BOOKMARKS_IN_MENU = 3

class Bookmarks(WebAppWidget):

    _parameters = {"bookmarks": [],
                  "format": 3,
                  "interval": 3,
                  "introText": "",
                  "introTitle": "",
                  "showIndicators": True,
                  "width": "400px"}

    def write(self, appdef, folder, app, progress):
        params = self._parameters
        bookmarks = params["bookmarks"]
        introText = params["introText"].replace('\n', '<br>').replace('\r', '')
        if bookmarks:
            self.addReactComponent(app, "Bookmarks")
            autoPlayjs = ", autoplay:true, autoplaySpeed:%s" % str(params["interval"] * 1000) if params["interval"] else ""
            if params["format"] != SHOW_BOOKMARKS_IN_MENU:
                app.mappanels.append('''React.createElement("div", {id: 'bookmarks-panel'},
                                        React.createElement(Bookmarks, {introTitle:'%s', introDescription:'%s', dots:%s,
                                            animatePanZoom:%s, menu: false, map: map, bookmarks: bookmarks,
                                            width:'%s' %s})
                                      )''' % (params["introTitle"], introText, str(params["showIndicators"]).lower(),
                                             str(params["format"] == SHOW_BOOKMARKS_IN_PANEL_PAN).lower(), params["width"],
                                             autoPlayjs))

            else:
                app.tools.append('''React.createElement(Bookmarks, {introTitle:'%s', introDescription:'%s', dots:%s,
                                            animatePanZoom:%s, menu: true, map: map, bookmarks: bookmarks, width:'%s' %s})
                                      ''' % (params["introTitle"], introText, str(params["showIndicators"]).lower(),
                                             str(params["format"] == SHOW_BOOKMARKS_IN_PANEL_PAN).lower(), params["width"],
                                             autoPlayjs))
            def extentInViewCrs(b):
                rect = QgsRectangle(b[0], b[1], b[2], b[3])
                viewCrs = QgsCoordinateReferenceSystem(appdef["Settings"]["App view CRS"])
                transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:3857"), viewCrs)
                extent = transform.transform(rect)
                return [extent.xMinimum(), extent.yMinimum(),
                                extent.xMaximum(), extent.yMaximum()]
            bookmarksDict = [{"name":b[0], "extent":extentInViewCrs(b[1]), "description":b[2]} for b in bookmarks]
            app.variables.append("var bookmarks = " + json.dumps(bookmarksDict))


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "bookmarks.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "bookmarks.png")

    def description(self):
        return "Bookmarks"

    def configure(self):
        dlg = BookmarksEditorDialog(self._parameters["bookmarks"],
                                    self._parameters["format"],
                                    self._parameters["interval"],
                                    self._parameters["introTitle"],
                                    self._parameters["introText"],
                                    self._parameters["showIndicators"])
        dlg.exec_()
        if dlg.bookmarks:
            self._parameters["bookmarks"] = dlg.bookmarks
            self._parameters["format"] = dlg.format
            self._parameters["interval"] = dlg.interval
            self._parameters["introTitle"] = dlg.introTitle
            self._parameters["introText"] = dlg.introText
            self._parameters["showIndicators"] = dlg.showIndicators

    def checkProblems(self, appdef, problems, forPreview):
        if len(self._parameters["bookmarks"]) == 0:
            problems.append("Bookmarks widget added, but no bookmarks have been defined. "
                        "You should configure the bookmarks widget and define at least one bookmark")


from qgis.core import *
from PyQt4 import QtCore, QtGui
import sqlite3


class BookmarksEditorDialog(QtGui.QDialog, Ui_BookmarksDialog):
    def __init__(self, bookmarks, format, interval, introTitle, introText, showIndicators):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.addFromQgisButton.clicked.connect(self.addFromQgis)

        self.layers = {}
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup):
                for subchild in child.children():
                    if isinstance(subchild, QgsLayerTreeLayer):
                        if isinstance(subchild.layer(), QgsVectorLayer):
                            self.layers[subchild.layer().name()] = subchild.layer()
            elif isinstance(child, QgsLayerTreeLayer):
                if isinstance(child.layer(), QgsVectorLayer):
                    self.layers[child.layer().name()] = child.layer()
        if self.layers:
            self.addFromLayerButton.clicked.connect(self.addFromLayer)
        else:
            self.addFromLayerButton.setEnabled(False)
        self.removeButton.clicked.connect(self.removeBookmark)
        self.removeAllButton.clicked.connect(self.removeAllBookmarks)
        self.bookmarksList.currentItemChanged.connect(self.selectionChanged)
        self.bookmarks = bookmarks
        self.format = format
        self.lastBookmarkItem = None
        self.storyPanelGroup.setChecked(self.format != SHOW_BOOKMARKS_IN_MENU)
        if self.format != SHOW_BOOKMARKS_IN_MENU:
            self.animationTypeCombo.setCurrentIndex(self.format)
            if interval:
                self.transitionTimeBox.setValue(interval)
                self.moveAutomaticallyCheck.setChecked(True)
            else:
                self.moveAutomaticallyCheck.setChecked(False)
        self.populateList()
        self.descriptionBox.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.introDescriptionBox.setPlainText(introText)
        self.introTitleBox.setText(introTitle)
        self.showIndicatorsCheck.setChecked(showIndicators)

    def addFromLayer(self):
        dlg = BookmarksFromLayerDialog(self.layers, self)
        dlg.exec_()
        if dlg.bookmarks:
            for b in dlg.bookmarks:
                item = BookmarkItem(b[0], b[1], b[2])
                self.bookmarksList.addItem(item)

    def addFromQgis(self):
        dbPath = QgsApplication.qgisUserDbFilePath()
        db = sqlite3.connect(dbPath)
        cursor = db.cursor()
        cursor.execute ("SELECT * FROM tbl_bookmarks")
        allBookmarks = cursor.fetchall()
        usedBookmarks = [self.bookmarksList.item(i).name for i in xrange(self.bookmarksList.count())]
        qgisBookmarks = {b[1]: b for b in allBookmarks if b[1] not in usedBookmarks}
        dlg = ListSelectorDialog(qgisBookmarks.keys(), self)
        dlg.exec_()
        if dlg.selected:
            for name in dlg.selected:
                b = qgisBookmarks[name]
                rect = QgsRectangle(b[3], b[4], b[5], b[6])
                crs = QgsCoordinateReferenceSystem()
                crs.createFromSrsId(int(b[7]))
                transform = QgsCoordinateTransform(crs, QgsCoordinateReferenceSystem("EPSG:3857"))
                extent = transform.transform(rect)
                item = BookmarkItem(b[1],  [extent.xMinimum(), extent.yMinimum(),
                                          extent.xMaximum(), extent.yMaximum()], "")
                self.bookmarksList.addItem(item)


    def selectionChanged(self):
        item = self.bookmarksList.currentItem()
        if item:
            self.descriptionBox.setEnabled(True)
            self.removeButton.setEnabled(True)
            if self.lastBookmarkItem:
                self.lastBookmarkItem.description = self.descriptionBox.toPlainText()
            self.descriptionBox.setPlainText(item.description)
            self.lastBookmarkItem = item
        else:
            self.descriptionBox.setEnabled(False)
            self.removeButton.setEnabled(False)

    def populateList(self):
        for bookmark in self.bookmarks:
            item = BookmarkItem(bookmark[0], bookmark[1], bookmark[2])
            self.bookmarksList.addItem(item)
        self.bookmarks = []

    def removeAllBookmarks(self):
        self.bookmarksList.clear()
        self.descriptionBox.setEnabled(False)
        self.removeButton.setEnabled(False)
        self.descriptionBox.setText("")

    def removeBookmark(self):
        item = self.bookmarksList.currentItem()
        if item:
            idx = self.bookmarksList.currentIndex().row()
            self.bookmarksList.takeItem(idx)
            self.bookmarksList.setCurrentItem(None)
            self.descriptionBox.setEnabled(False)
            self.removeButton.setEnabled(False)

    def okPressed(self):
        bookmarks = []
        self.selectionChanged()
        for i in xrange(self.bookmarksList.count()):
            item = self.bookmarksList.item(i)
            bookmarks.append([item.name, item.extent, item.description])
        self.bookmarks = bookmarks
        if self.storyPanelGroup.isChecked():
            self.format = self.animationTypeCombo.currentIndex()
            if self.moveAutomaticallyCheck.isChecked():
                self.interval = self.transitionTimeBox.value()
            else:
                self.interval = 0
        else:
            self.format = SHOW_BOOKMARKS_IN_MENU
            self.interval = 0;
        self.introText = self.introDescriptionBox.toPlainText()
        self.introTitle = self.introTitleBox.text()
        self.showIndicators = self.showIndicatorsCheck.isChecked()
        self.close()

    def cancelPressed(self):
        self.bookmarks = []
        self.close()


class BookmarkItem(QtGui.QListWidgetItem):

    def __init__(self, name, extent, description):
        QtGui.QListWidgetItem.__init__(self)
        self.description = description
        self.extent = extent
        self.name = name
        self.setText(name)


class BookmarksFromLayerDialog(QtGui.QDialog):

    def __init__(self, layers, parent=None):
        super(BookmarksFromLayerDialog, self).__init__(parent)
        self.bookmarks = []
        self.setWindowTitle("Bookmarks from layer")
        layout = QtGui.QVBoxLayout()
        self.layers = layers
        label = QtGui.QLabel()
        label.setText("Layer")
        layout.addWidget(label)
        self.layerCombo = QtGui.QComboBox()
        self.layerCombo.addItems(self.layers.keys())
        layout.addWidget(self.layerCombo)
        self.layerCombo.currentIndexChanged.connect(self.layerComboChanged)
        label = QtGui.QLabel()
        label.setText("Name field")
        layout.addWidget(label)
        self.nameCombo = QtGui.QComboBox()
        layout.addWidget(self.nameCombo)
        label = QtGui.QLabel()
        label.setText("Description field")
        layout.addWidget(label)
        self.descriptionCombo = QtGui.QComboBox()
        layout.addWidget(self.descriptionCombo)
        self.layerComboChanged()
        spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok
                                                | QtGui.QDialogButtonBox.Cancel)
        layout.addItem(spacer)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.resize(500, 400)

    def layerComboChanged(self):
        layerName = self.layerCombo.currentText()
        fields = [f.name() for f in self.layers[layerName].pendingFields()]
        self.nameCombo.clear()
        self.nameCombo.addItems(fields)
        self.descriptionCombo.clear()
        self.descriptionCombo.addItems(fields)

    def okPressed(self):
        self.bookmarks = []
        layerName = self.layerCombo.currentText()
        nameField = self.nameCombo.currentText()
        descriptionField = self.descriptionCombo.currentText()
        layer = self.layers[layerName]
        transform = QgsCoordinateTransform(layer.crs(),
                                            QgsCoordinateReferenceSystem("EPSG:3857"))
        for feature in layer.getFeatures():
            geom = feature.geometry()
            extent = transform.transform(geom.boundingBox())
            name = unicode(feature[nameField])
            description = unicode(feature[descriptionField])
            self.bookmarks.append([name, [extent.xMinimum(), extent.yMinimum(),
                                extent.xMaximum(), extent.yMaximum()], description])
        self.close()

    def cancelPressed(self):
        self.bookmarks = []
        self.close()

class ListSelectorDialog(QtGui.QDialog):

    def __init__(self, options, parent=None):
        super(ListSelectorDialog, self).__init__(parent)
        self.selected = []
        self.setWindowTitle("Select bookmarks")
        layout = QtGui.QVBoxLayout()

        self.optionsList = QtGui.QListWidget()
        for b in options:
            item = QtGui.QListWidgetItem()
            item.setText(b)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.optionsList.addItem(item)
        layout.addWidget(self.optionsList)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.resize(500, 400)

    def okPressed(self):
        self.selected = []
        for i in xrange(self.optionsList.count()):
            item = self.optionsList.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                self.selected.append(item.text())
        self.close()

    def cancelPressed(self):
        self.selected = []
        self.close()
