# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
from qgis.PyQt import uic
from qgis.PyQt.QtCore import Qt, QDateTime


WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'ui_timeinfodialog.ui'))

class TimeInfoDialog(BASE, WIDGET):
    def __init__(self, timeInfo, layer):
        super(TimeInfoDialog, self).__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
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
        elif isinstance(timeInfo[0], str):
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
