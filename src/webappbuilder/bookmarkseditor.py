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
        self.addButton.clicked.connect(self.addBookmark)
        self.removeButton.clicked.connect(self.removeBookmark)
        self.bookmarksToUseList.currentItemChanged.connect(self.selectionChanged)
        self.bookmarks = bookmarks
        self.format = format
        self.lastBookmark = None
        dbPath = QgsApplication.qgisUserDbFilePath()
        db = sqlite3.connect(dbPath)
        cursor = db.cursor()
        cursor.execute ("SELECT * FROM tbl_bookmarks")
        allBookmarks = cursor.fetchall()
        self.allBookmarks = {b[1]: b for b in allBookmarks}
        self.descriptions = {b[1]: "" for b in allBookmarks}
        self.bookmarkAsDict = {b[0]:b for b in bookmarks}
        self.descriptions.update({b[0]: b[2] for b in bookmarks})
        self.populateList()
        if self.format != SHOW_BOOKMARKS_IN_MENU:
            self.animationTypeCombo.setCurrentIndex(self.format)
        self.showAsStoryPanelCheck.setChecked(self.format != SHOW_BOOKMARKS_IN_MENU)

    def selectionChanged(self):
        item = self.bookmarksToUseList.currentItem()
        if item:
            if self.lastBookmark:
                self.descriptions[self.lastBookmark] = self.descriptionBox.toPlainText()
            self.descriptionBox.setPlainText(self.descriptions[item.text()])
            self.lastBookmark = item.text()

    def populateList(self):
        for bookmark in self.bookmarks:
            item = QtGui.QListWidgetItem()
            item.setText(bookmark[0])
            self.bookmarksToUseList.addItem(item)
        for name in self.allBookmarks:
            if name not in self.bookmarkAsDict:
                item = QtGui.QListWidgetItem()
                item.setText(name)
                self.availableBookmarksList.addItem(item)

    def addBookmark(self):
        items = self.availableBookmarksList.selectedItems()
        for item in items:
            idx = self.availableBookmarksList.indexFromItem(item).row()
            self.availableBookmarksList.takeItem(idx)
            self.bookmarksToUseList.addItem(item)

    def removeBookmark(self):
        item = self.bookmarksToUseList.currentItem()
        idx = self.bookmarksToUseList.currentIndex().row()
        if item:
            self.bookmarksToUseList.takeItem(idx)
            self.availableBookmarksList.addItem(item)

    def okPressed(self):
        bookmarks = []
        self.selectionChanged()
        for i in xrange(self.bookmarksToUseList.count()):
            item = self.bookmarksToUseList.item(i)
            name = item.text()
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




