from qgis.core import *
from PyQt4 import QtCore, QtGui
import os
from ui_bookmarksdialog import Ui_BookmarksDialog
import sqlite3
from utils import SHOW_BOOKMARKS_IN_MENU



class BookmarksEditorDialog(QtGui.QDialog, Ui_BookmarksDialog):
    def __init__(self, parent, bookmarks, format):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.showProjectOnlyCheck.stateChanged.connect(self.setVisibility)
        self.bookmarks = bookmarks
        self.format = format
        dbPath = QgsApplication.qgisUserDbFilePath()
        db = sqlite3.connect(dbPath)
        cursor = db.cursor()
        cursor.execute ("SELECT * FROM tbl_bookmarks")
        allBookmarks = cursor.fetchall()
        self.allBookmarks = {b[1]: b for b in allBookmarks}
        self.descriptions = {}
        self.bookmarkAsDict = {b[0]:b for b in bookmarks}
        self.populateList()
        self.setVisibility()
        if self.format != SHOW_BOOKMARKS_IN_MENU:
            self.animationTypeCombo.setCurrentIndex(self.format)
        self.showAsStoryPanelCheck.setChecked(self.format != SHOW_BOOKMARKS_IN_MENU)

    def populateList(self):
        self.bookmarksList.clear()
        for bookmark in self.bookmarks:
            item = QtGui.QListWidgetItem()
            self.bookmarksList.addItem(item)
            widget = QtGui.QCheckBox()
            widget.setText(bookmark[0])
            widget.setChecked(True)
            self.bookmarksList.setItemWidget(item, widget)
        for name in self.allBookmarks:
            if name not in self.bookmarkAsDict:
                item = QtGui.QListWidgetItem()
                self.bookmarksList.addItem(item)
                widget = QtGui.QCheckBox()
                widget.setText(name)
                widget.setChecked(False)
                self.bookmarksList.setItemWidget(item, widget)

    def setVisibility(self):
        projectName = os.path.basename(QgsProject.instance().fileName())
        for i in xrange(self.bookmarksList.count()):
            item = self.bookmarksList.item(i)
            check = self.bookmarksList.itemWidget(item)
            name = check.text()
            print name
            if name in self.bookmarkAsDict:
                item.setHidden(False)
            else:
                item.setHidden(self.showProjectOnlyCheck and self.allBookmarks[name][2] != projectName)

    def okPressed(self):
        bookmarks = []
        for i in xrange(self.bookmarksList.count()):
            check = self.bookmarksList.itemWidget(self.bookmarksList.item(i))
            if check.isChecked():
                name = check.text()
                if name in self.bookmarkAsDict:
                    bookmarks.append([name, self.bookmarkAsDict[name][1], self.descriptions.get(name, "")])
                else:
                    b = self.allBookmarks[name]
                    rect = QgsRectangle(b[3], b[4], b[5], b[6])
                    transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem(int(b[7])),
                                                       QgsCoordinateReferenceSystem("EPSG:3857"))
                    extent = transform.transform(rect)
                    bookmarks.append([name,  [extent.xMinimum(), extent.yMinimum(),
                                              extent.xMaximum(), extent.yMaximum()],
                                      self.descriptions.get(name, "")])
        self.bookmarks = bookmarks
        if self.showAsStoryPanelCheck.isChecked():
            self.format = self.animationTypeCombo.currentIndex()
        else:
            self.format = SHOW_BOOKMARKS_IN_MENU
        self.close()

    def cancelPressed(self):
        self.close()

class ItemWidget(QtGui.QWidget):

    def __init__(self, name, checked):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QHBoxLayout()
        self.check = QtGui.QCheckBox()
        self.check.setChecked(True)
        layout.addWidget(self.check)
        self.label = QtGui.QLabel()
        self.label.setText(name + " <a href='edit'>Edit text</a>")
        layout.addWidget(self.label)
        self.setLayout(layout)


