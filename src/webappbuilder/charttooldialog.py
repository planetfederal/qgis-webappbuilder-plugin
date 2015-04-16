from qgis.core import *
from PyQt4 import QtCore, QtGui
from ui_charttooldialog import Ui_ChartToolDialog

class ChartToolDialog(QtGui.QDialog, Ui_ChartToolDialog):
    def __init__(self, charts, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.charts = charts
        self._charts = charts
        self.populateList()
        self.populateLayers()
        if self.layers:
            self.populateFieldCombos(self.layers.keys()[0])
        self.layerCombo.currentIndexChanged.connect(self.layerComboChanged)
        self.displayModeCombo.currentIndexChanged.connect(self.displayModeComboChanged)
        self.addButton.clicked.connect(self.addChart)
        self.removeButton.clicked.connect(self.removeChart)
        self.chartsList.currentItemChanged.connect(self.selectionChanged)
        self.displayModeComboChanged()

    def displayModeComboChanged(self):
        visible = self.displayModeCombo.currentIndex() == 1
        self.operationCombo.setVisible(visible)
        self.operationLabel.setVisible(visible)
        visible = self.displayModeCombo.currentIndex() != 2
        self.valueFieldsCombo.setVisible(visible)
        self.valueFieldsLabel.setVisible(visible)

    def selectionChanged(self):
        try:
            name = self.chartsList.currentItem().text()
        except:
            return
        self.nameBox.setText(name)
        idx = self.layerCombo.findText(self._charts[name]["layer"])
        self.layerCombo.setCurrentIndex(idx)
        idx = self.categoryFieldCombo.findText(self._charts[name]["categoryField"])
        self.categoryFieldCombo.setCurrentIndex(idx)
        idx = self.displayMode.findText(self._charts[name]["displayMode"])
        self.displayMode.setCurrentIndex(idx)
        try:
            idx = self.operationCombo.findText(self._charts[name]["operation"])
            self.operationCombo.setCurrentIndex(idx)
        except:
            pass
        valueFields = self._charts[name]["valueFields"]
        for i in xrange(1, self.model.rowCount()):
            item = self.model.item(i)
            item.setData(QtCore.Qt.Checked if item.text() in valueFields else QtCore.Qt.Unchecked,
                         QtCore.Qt.CheckStateRole)

    def layerComboChanged(self):
        self.populateFieldCombos(self.layerCombo.currentText())

    def populateList(self):
        self.chartsList.clear()
        for chart in self._charts:
            item = QtGui.QListWidgetItem()
            item.setText(chart)
            self.chartsList.addItem(item)

    def populateLayers(self):
        skipType = [2]
        self.layers = {}
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup):
                for subchild in child.children():
                    if isinstance(subchild, QgsLayerTreeLayer):
                        if subchild.layer().type() not in skipType:
                            self.layers[subchild.layer().name()] = subchild.layer()
            elif isinstance(child, QgsLayerTreeLayer):
                self.layers[child.layer().name()] = child.layer()

        self.layerCombo.addItems(self.layers.keys())

    def populateFieldCombos(self, layerName):
        fields = [f.name() for f in self.layers[layerName].pendingFields()]
        self.categoryFieldCombo.clear()
        self.categoryFieldCombo.addItems(fields)
        self.model = QtGui.QStandardItemModel(len(fields), 1)
        item = QtGui.QStandardItem("Select fields")
        self.model.setItem(0, 0, item);
        for i, f in enumerate(fields):
            item = QtGui.QStandardItem(f)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole);
            self.model.setItem(i + 1, 0, item);
        self.valueFieldsCombo.setModel(self.model)

    def addChart(self):
        name = self.nameBox.text()
        if name.strip():
            self.nameBox.setStyleSheet("QLineEdit{background: white}")
        else:
            self.nameBox.setStyleSheet("QLineEdit{background: yellow}")
            return
        layer = self.layerCombo.currentText()
        displayMode = self.displayModeCombo.currentIndex()
        categoryField = self.categoryFieldCombo.currentText()
        operation = self.operationCombo.currentIndex()
        valueFields = []
        for i in xrange(self.model.rowCount()):
            item = self.model.item(i)
            checked = item.data(QtCore.Qt.CheckStateRole)
            if checked == QtCore.Qt.Checked:
                valueFields.append(item.text())
        self._charts[name] = {"layer": layer,
                              "categoryField": categoryField,
                              "valueFields": valueFields,
                              "displayMode": displayMode,
                              "operation": operation}
        self.populateList()

    def removeChart(self):
        try:
            name = self.chartsList.currentItem().text()
            del self._charts[name]
            self.populateList()
            self.nameBox.setText("")
            self.layerCombo.setCurrentIndex(0)
            self.populateFieldCombos(self.layerCombo.currentText())
        except:
            pass

    def okPressed(self):
        self.charts = self._charts
        self.close()

    def cancelPressed(self):
        self.close()



