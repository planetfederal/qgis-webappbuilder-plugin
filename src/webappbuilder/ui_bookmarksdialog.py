# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_bookmarksdialog.ui'
#
# Created: Thu Apr 16 14:27:44 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BookmarksDialog(object):
    def setupUi(self, BookmarksDialog):
        BookmarksDialog.setObjectName(_fromUtf8("BookmarksDialog"))
        BookmarksDialog.resize(854, 652)
        self.verticalLayout = QtGui.QVBoxLayout(BookmarksDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(BookmarksDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.bookmarks = QtGui.QWidget()
        self.bookmarks.setObjectName(_fromUtf8("bookmarks"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.bookmarks)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_4 = QtGui.QLabel(self.bookmarks)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_2.addWidget(self.label_4)
        self.availableBookmarksList = QtGui.QListWidget(self.bookmarks)
        self.availableBookmarksList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.availableBookmarksList.setObjectName(_fromUtf8("availableBookmarksList"))
        self.verticalLayout_2.addWidget(self.availableBookmarksList)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.addButton = QtGui.QPushButton(self.bookmarks)
        self.addButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.verticalLayout_5.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(self.bookmarks)
        self.removeButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.verticalLayout_5.addWidget(self.removeButton)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_5 = QtGui.QLabel(self.bookmarks)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_4.addWidget(self.label_5)
        self.bookmarksToUseList = QtGui.QListWidget(self.bookmarks)
        self.bookmarksToUseList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.bookmarksToUseList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.bookmarksToUseList.setObjectName(_fromUtf8("bookmarksToUseList"))
        self.verticalLayout_4.addWidget(self.bookmarksToUseList)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.label_3 = QtGui.QLabel(self.bookmarks)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_6.addWidget(self.label_3)
        self.descriptionBox = QtGui.QTextEdit(self.bookmarks)
        self.descriptionBox.setObjectName(_fromUtf8("descriptionBox"))
        self.verticalLayout_6.addWidget(self.descriptionBox)
        self.tabWidget.addTab(self.bookmarks, _fromUtf8(""))
        self.configuration = QtGui.QWidget()
        self.configuration.setObjectName(_fromUtf8("configuration"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.configuration)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.showAsStoryPanelCheck = QtGui.QCheckBox(self.configuration)
        self.showAsStoryPanelCheck.setObjectName(_fromUtf8("showAsStoryPanelCheck"))
        self.verticalLayout_3.addWidget(self.showAsStoryPanelCheck)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.label = QtGui.QLabel(self.configuration)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.animationTypeCombo = QtGui.QComboBox(self.configuration)
        self.animationTypeCombo.setMinimumSize(QtCore.QSize(200, 0))
        self.animationTypeCombo.setObjectName(_fromUtf8("animationTypeCombo"))
        self.animationTypeCombo.addItem(_fromUtf8(""))
        self.animationTypeCombo.addItem(_fromUtf8(""))
        self.animationTypeCombo.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.animationTypeCombo)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem4 = QtGui.QSpacerItem(20, 330, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem4)
        self.tabWidget.addTab(self.configuration, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(BookmarksDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(BookmarksDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BookmarksDialog)

    def retranslateUi(self, BookmarksDialog):
        BookmarksDialog.setWindowTitle(_translate("BookmarksDialog", "Bookmarks", None))
        self.label_4.setText(_translate("BookmarksDialog", "Available bookmarks", None))
        self.addButton.setText(_translate("BookmarksDialog", "->", None))
        self.removeButton.setText(_translate("BookmarksDialog", "<-", None))
        self.label_5.setText(_translate("BookmarksDialog", "Bookmarks to use (drag to reorder, select to edit description)", None))
        self.label_3.setText(_translate("BookmarksDialog", "Bookmark text", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarks), _translate("BookmarksDialog", "Bookmarks", None))
        self.showAsStoryPanelCheck.setText(_translate("BookmarksDialog", "Show as story panel", None))
        self.label.setText(_translate("BookmarksDialog", "Animation type:", None))
        self.animationTypeCombo.setItemText(0, _translate("BookmarksDialog", "Go to", None))
        self.animationTypeCombo.setItemText(1, _translate("BookmarksDialog", "Pan to", None))
        self.animationTypeCombo.setItemText(2, _translate("BookmarksDialog", "Fly to", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configuration), _translate("BookmarksDialog", "Configuration", None))

