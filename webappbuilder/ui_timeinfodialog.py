from builtins import object
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_timeinfodialog.ui'
#
# Created: Thu Jul 23 13:46:52 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui

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

class Ui_TimeInfoDialog(object):
    def setupUi(self, TimeInfoDialog):
        TimeInfoDialog.setObjectName(_fromUtf8("TimeInfoDialog"))
        TimeInfoDialog.resize(542, 334)
        self.verticalLayout = QtGui.QVBoxLayout(TimeInfoDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(TimeInfoDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.radioButtonNoTimeInfo = QtGui.QRadioButton(self.groupBox)
        self.radioButtonNoTimeInfo.setObjectName(_fromUtf8("radioButtonNoTimeInfo"))
        self.verticalLayout_2.addWidget(self.radioButtonNoTimeInfo)
        self.radioButtonLayerTimeInfo = QtGui.QRadioButton(self.groupBox)
        self.radioButtonLayerTimeInfo.setObjectName(_fromUtf8("radioButtonLayerTimeInfo"))
        self.verticalLayout_2.addWidget(self.radioButtonLayerTimeInfo)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.fromDateTimeEdit = QtGui.QDateTimeEdit(self.groupBox)
        self.fromDateTimeEdit.setObjectName(_fromUtf8("fromDateTimeEdit"))
        self.gridLayout.addWidget(self.fromDateTimeEdit, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.toDateTimeEdit = QtGui.QDateTimeEdit(self.groupBox)
        self.toDateTimeEdit.setObjectName(_fromUtf8("toDateTimeEdit"))
        self.gridLayout.addWidget(self.toDateTimeEdit, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.radioButtonFeatureTimeInfo = QtGui.QRadioButton(self.groupBox)
        self.radioButtonFeatureTimeInfo.setObjectName(_fromUtf8("radioButtonFeatureTimeInfo"))
        self.verticalLayout_2.addWidget(self.radioButtonFeatureTimeInfo)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 0, 1, 1, 1)
        self.fromDateAttributeComboBox = QtGui.QComboBox(self.groupBox)
        self.fromDateAttributeComboBox.setObjectName(_fromUtf8("fromDateAttributeComboBox"))
        self.gridLayout_2.addWidget(self.fromDateAttributeComboBox, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 0, 1, 1)
        self.toDateAttributeComboBox = QtGui.QComboBox(self.groupBox)
        self.toDateAttributeComboBox.setObjectName(_fromUtf8("toDateAttributeComboBox"))
        self.gridLayout_2.addWidget(self.toDateAttributeComboBox, 1, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.verticalLayout.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(TimeInfoDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(TimeInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(TimeInfoDialog)

    def retranslateUi(self, TimeInfoDialog):
        TimeInfoDialog.setWindowTitle(_translate("TimeInfoDialog", "Time info", None))
        self.groupBox.setTitle(_translate("TimeInfoDialog", "Time info configuration", None))
        self.radioButtonNoTimeInfo.setText(_translate("TimeInfoDialog", "No time info", None))
        self.radioButtonLayerTimeInfo.setText(_translate("TimeInfoDialog", "Single time info for the whole layer", None))
        self.label.setText(_translate("TimeInfoDialog", "From date", None))
        self.label_3.setText(_translate("TimeInfoDialog", "To date", None))
        self.radioButtonFeatureTimeInfo.setText(_translate("TimeInfoDialog", "Feature time info is stored in layer attribute", None))
        self.label_2.setText(_translate("TimeInfoDialog", "From date field", None))
        self.label_4.setText(_translate("TimeInfoDialog", "To date field", None))

