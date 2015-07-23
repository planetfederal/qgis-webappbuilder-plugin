from qgis.core import *
from PyQt4 import QtCore, QtGui

from ui_timeinfodialog import Ui_TimeInfoDialog
from PyQt4.QtCore import QDateTime


class TimeInfoDialog(QtGui.QDialog, Ui_TimeInfoDialog):
    def __init__(self, timeInfo, layer):
        print timeInfo
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.timeInfo = timeInfo
        self.ok = False
        fields = [f.name() for f in layer.pendingFields()]
        self.toDateAttributeComboBox.addItems(fields)
        self.fromDateAttributeComboBox.addItems(fields)
        if timeInfo is None:
            self.radioButtonNoTimeInfo.setChecked(True)
        elif isinstance(timeInfo[0], basestring):
            self.fromDateAttributeComboBox.setCurrentIndex(self.fromDateAttributeComboBox.findText(timeInfo[0]))
            self.toDateAttributeComboBox.setCurrentIndex(self.toDateAttributeComboBox.findText(timeInfo[1]))
            self.radioButtonFeatureTimeInfo.setChecked(True)
        else:
            self.radioButtonLayerTimeInfo.setChecked(True)
            self.toDateTimeEdit.setDateTime(QDateTime.fromMSecsSinceEpoch(timeInfo[0]))
            self.fromDateTimeEdit.setDateTime(QDateTime.fromMSecsSinceEpoch(timeInfo[1]))

    def okPressed(self):
        if self.radioButtonFeatureTimeInfo.isChecked():
            self.timeInfo = [self.fromDateAttributeComboBox.currentText(), self.toDateAttributeComboBox.currentText()]
        elif self.radioButtonLayerTimeInfo.isChecked():
            self.timeInfo = [self.fromDateTimeEdit.dateTime().toMSecsSinceEpoch(), self.toDateTimeEdit.dateTime().toMSecsSinceEpoch()]
        else:
            self.timeInfo = None
        self.ok = True
        self.close()

    def cancelPressed(self):
        self.close()