# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_bookmarksdialog.ui'
#
# Created: Mon Apr 13 16:11:39 2015
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
        BookmarksDialog.resize(474, 475)
        self.verticalLayout = QtGui.QVBoxLayout(BookmarksDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(BookmarksDialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.bookmarks = QtGui.QWidget()
        self.bookmarks.setObjectName(_fromUtf8("bookmarks"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.bookmarks)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_2 = QtGui.QLabel(self.bookmarks)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.bookmarksList = QtGui.QListWidget(self.bookmarks)
        self.bookmarksList.setDragEnabled(True)
        self.bookmarksList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.bookmarksList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.bookmarksList.setObjectName(_fromUtf8("bookmarksList"))
        self.verticalLayout_4.addWidget(self.bookmarksList)
        self.showProjectOnlyCheck = QtGui.QCheckBox(self.bookmarks)
        self.showProjectOnlyCheck.setObjectName(_fromUtf8("showProjectOnlyCheck"))
        self.verticalLayout_4.addWidget(self.showProjectOnlyCheck)
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
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
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
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        spacerItem2 = QtGui.QSpacerItem(20, 330, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
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
        self.label_2.setText(_translate("BookmarksDialog", "<b>Select bookmarks to use. Drag and drop to reorder</b>", None))
        self.showProjectOnlyCheck.setText(_translate("BookmarksDialog", "Show only project bookmarks", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bookmarks), _translate("BookmarksDialog", "Bookmarks", None))
        self.showAsStoryPanelCheck.setText(_translate("BookmarksDialog", "Show as story panel", None))
        self.label.setText(_translate("BookmarksDialog", "Animation type:", None))
        self.animationTypeCombo.setItemText(0, _translate("BookmarksDialog", "Go to", None))
        self.animationTypeCombo.setItemText(1, _translate("BookmarksDialog", "Pan to", None))
        self.animationTypeCombo.setItemText(2, _translate("BookmarksDialog", "Fly to", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configuration), _translate("BookmarksDialog", "Configuration", None))

