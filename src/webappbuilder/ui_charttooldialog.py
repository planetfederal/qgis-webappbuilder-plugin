# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_charttooldialog.ui'
#
# Created: Tue Apr 14 11:20:32 2015
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

class Ui_ChartToolDialog(object):
    def setupUi(self, ChartToolDialog):
        ChartToolDialog.setObjectName(_fromUtf8("ChartToolDialog"))
        ChartToolDialog.resize(643, 385)
        self.verticalLayout_3 = QtGui.QVBoxLayout(ChartToolDialog)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(9, 9, 9, 0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(ChartToolDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.nameBox = QtGui.QLineEdit(ChartToolDialog)
        self.nameBox.setObjectName(_fromUtf8("nameBox"))
        self.verticalLayout.addWidget(self.nameBox)
        self.label_4 = QtGui.QLabel(ChartToolDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.layerCombo = QtGui.QComboBox(ChartToolDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerCombo.sizePolicy().hasHeightForWidth())
        self.layerCombo.setSizePolicy(sizePolicy)
        self.layerCombo.setMinimumSize(QtCore.QSize(300, 0))
        self.layerCombo.setObjectName(_fromUtf8("layerCombo"))
        self.verticalLayout.addWidget(self.layerCombo)
        self.label = QtGui.QLabel(ChartToolDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.categoryFieldCombo = QtGui.QComboBox(ChartToolDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.categoryFieldCombo.sizePolicy().hasHeightForWidth())
        self.categoryFieldCombo.setSizePolicy(sizePolicy)
        self.categoryFieldCombo.setObjectName(_fromUtf8("categoryFieldCombo"))
        self.verticalLayout.addWidget(self.categoryFieldCombo)
        self.label_3 = QtGui.QLabel(ChartToolDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.valueFieldsCombo = QtGui.QComboBox(ChartToolDialog)
        self.valueFieldsCombo.setObjectName(_fromUtf8("valueFieldsCombo"))
        self.verticalLayout.addWidget(self.valueFieldsCombo)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.addButton = QtGui.QPushButton(ChartToolDialog)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(ChartToolDialog)
        self.removeButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.horizontalLayout.addWidget(self.removeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.chartsList = QtGui.QListWidget(ChartToolDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartsList.sizePolicy().hasHeightForWidth())
        self.chartsList.setSizePolicy(sizePolicy)
        self.chartsList.setMinimumSize(QtCore.QSize(300, 0))
        self.chartsList.setMaximumSize(QtCore.QSize(11111111, 16777215))
        self.chartsList.setObjectName(_fromUtf8("chartsList"))
        self.verticalLayout_2.addWidget(self.chartsList)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.buttonBox = QtGui.QDialogButtonBox(ChartToolDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(ChartToolDialog)
        QtCore.QMetaObject.connectSlotsByName(ChartToolDialog)

    def retranslateUi(self, ChartToolDialog):
        ChartToolDialog.setWindowTitle(_translate("ChartToolDialog", "Chart Tool", None))
        self.label_2.setText(_translate("ChartToolDialog", "Chart name", None))
        self.label_4.setText(_translate("ChartToolDialog", "Layer", None))
        self.label.setText(_translate("ChartToolDialog", "Category field", None))
        self.label_3.setText(_translate("ChartToolDialog", "Value fields", None))
        self.addButton.setText(_translate("ChartToolDialog", "Add", None))
        self.removeButton.setText(_translate("ChartToolDialog", "Remove", None))

