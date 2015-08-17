from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json
from ui_bookmarksdialog import Ui_BookmarksDialog

SHOW_BOOKMARKS_IN_PANEL_GO = 0
SHOW_BOOKMARKS_IN_PANEL_PAN = 1
SHOW_BOOKMARKS_IN_PANEL_FLY = 2
SHOW_BOOKMARKS_IN_MENU = 3

class Bookmarks(WebAppWidget):

    _parameters = {"bookmarks": [],
                  "format": 3,
                  "interval": 3,
                  "introText": "",
                  "introTitle": "",
                  "showIndicators": True}

    def write(self, appdef, folder, app, progress):
        params = self._parameters
        bookmarks = params["bookmarks"]
        if bookmarks:
            app.scriptsBottom.append('<script src="./bookmarks.js"></script>')
            self.addScript("bookmarks.js", folder, app)
            if params["format"] != SHOW_BOOKMARKS_IN_MENU:
                itemBase = '''<div class="item %s">
                              <div class="header-text hidden-xs">
                                  <div class="col-md-12 text-center">
                                      <h2>%s</h2>
                                      <p>%s</p>
                                  </div>
                              </div>
                            </div>'''
                bookmarkDivs = itemBase % ("active", params["introTitle"], params["introText"])
                bookmarkDivs += "\n".join([itemBase % ("", b[0], b[2]) for i,b in enumerate(bookmarks)])
                if params["showIndicators"]:
                    li = "\n".join(['<li data-target="#story-carousel" data-slide-to="%i"></li>' % (i+1) for i in xrange(len(bookmarks))])
                    indicators = '''<ol class="carousel-indicators">
                                        <li data-target="#story-carousel" data-slide-to="0" class="active"></li>
                                        %s
                                    </ol>''' % li
                else:
                    indicators = ""
                slide = "slide" if params["interval"] else ""
                interval = str(params["interval"] * 1000) if params["interval"] else "false"
                app.mappanels.append('''<div class="story-panel">
                      <div class="row">
                          <div id="story-carousel" class="carousel %s" data-interval="%s" data-ride="carousel">
                            %s
                            <div class="carousel-inner">
                                %s
                            </div>
                          </div>
                          <a class="left carousel-control" href="#story-carousel" data-slide="prev">
                              <span class="glyphicon glyphicon-chevron-left">&nbsp;</span>
                          </a>
                          <a class="right carousel-control" href="#story-carousel" data-slide="next">
                              <span class="glyphicon glyphicon-chevron-right">&nbsp;</span>
                          </a>
                      </div>
                    </div>
                    ''' % (slide, interval, indicators, bookmarkDivs))
                bookmarkEvents = '''\n$("#story-carousel").on('slide.bs.carousel', function(evt) {
                                          %sToBookmark($(evt.relatedTarget).index()-1)
                                    })''' % ["go", "pan", "fly"][params["format"]]
            else:
                li = "\n".join(["<li><a onclick=\"goToBookmarkByName('%s')\" href=\"#\">%s</a></li>" % (b[0],b[0]) for b in params["bookmarks"]])
                app.tools.append('''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Bookmarks <span class="caret"><span></a>
                    <ul class="dropdown-menu">
                      %s
                    </ul>
                  </li>''' % li)
            bookmarksFilepath = os.path.join(folder, "bookmarks.js")
            with open(bookmarksFilepath, "w") as f:
                bookmarksWithoutDescriptions = [b[:-1] for b in bookmarks]
                f.write("var bookmarks = " + json.dumps(bookmarksWithoutDescriptions))
                f.write(bookmarkEvents)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "bookmarks.png"))

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

    def checkProblems(self, appdef, problems):
        if len(self._parameters["bookmarks"]) == 0:
            problems.append("Bookmarks widget added, but no bookmarks have been defined"
                        "You should configure the bookmarks widget and define at least one bookmark")

widgetInstance = Bookmarks()

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
