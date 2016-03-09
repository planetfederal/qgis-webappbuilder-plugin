from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
import json
from webappbuilder.utils import findLayerByName, findProjectLayerByName

class ChartTool(WebAppWidget):

    _parameters = {"charts": {}}

    order = 3

    def write(self, appdef, folder, app, progress):
        self.addReactComponent(app, "Chart")
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(UI.Tab,{eventKey:%i, title:"Charts"},
                                    React.createElement("div", {id:"charts-tab"},
                                        React.createElement(Chart, {combo:true, charts:charts})
                                    )
                                )''' % idx)
        else:
            app.tools.append('''{jsx: React.createElement(Chart, {container:'chart-panel', charts:charts})}''')
            app.panels.append('''React.createElement("div", {id: 'chart-panel', className: 'chart-panel'},
                                            React.createElement("a", {href:'#', id:'chart-panel-closer', className:'chart-panel-closer', onClick:this._toggleChartPanel.bind(this)},
                                                                  "X"
                                                            ),
                                            React.createElement("div", {id: 'chart'})
                                    )''' )
        charts = []
        for chartName, chart in self._parameters["charts"].iteritems():
            charts.append(copy.copy(chart))
            charts[-1]["title"] = chartName
            charts[-1]["layer"] = findProjectLayerByName(chart["layer"]).id()
        app.variables.append("var charts = %s;" % json.dumps(charts))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "chart-tool.png"))

    def description(self):
        return "Charts"

    def configure(self):
        dlg = ChartToolDialog(self._parameters["charts"])
        dlg.exec_()
        self._parameters["charts"] = dlg.charts

    def checkProblems(self, appdef, problems):
        widgetNames = [w.name() for w in appdef["Widgets"].values()]
        charts = self._parameters["charts"]
        if len(charts) == 0:
            problems.append("Chart tool added, but no charts have been defined. "
                        "You should configure the chart tool and define at least one chart")
        if "selectiontools" not in widgetNames:
            problems.append("Chart tool added, but the web app has no selection tools. "
                        "Charts are created based on selected features, so you should add selection "
                        "tools to the web app, to allow the user selecting features in the map")
        for name, chart in charts.iteritems():
            layer = findLayerByName(chart["layer"], appdef["Layers"])
            if layer is None:
                problems.append("Chart tool %s uses a layer (%s) that is not added to web app" % (name, chart["layer"]))
            elif not layer.allowSelection:
                problems.append(("Chart tool %s uses a layer (%s) that does not allow selection. " +
                            "Selection should be enabled for that layer.") % (name, chart["layer"]))

from qgis.core import *
from PyQt4 import QtCore, QtGui
from ui_charttooldialog import Ui_ChartToolDialog
import copy
import sys

class ChartToolDialog(QtGui.QDialog, Ui_ChartToolDialog):
    def __init__(self, charts):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.charts = charts
        self._charts = copy.deepcopy(charts)
        self.populateLayers()
        self.populateList()
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
        isMac = sys.platform in ['darwin', 'linux2']
        self.valueFieldsCombo.setVisible(visible and not isMac)
        self.valueFieldsList.setVisible(visible and isMac)
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
        self.displayModeCombo.setCurrentIndex(self._charts[name]["displayMode"])
        try:
            idx = self.operationCombo.findText()
            self.operationCombo.setCurrentIndex(self._charts[name]["operation"])
        except:
            pass
        try:
            offset = 0 if sys.platform in ['darwin', 'linux2'] else 1
            valueFields = self._charts[name]["valueFields"]
            for i in xrange(offset, self.model.rowCount()):
                item = self.model.item(i)
                item.setData(QtCore.Qt.Checked if item.text() in valueFields else QtCore.Qt.Unchecked,
                         QtCore.Qt.CheckStateRole)
        except:
            pass

    def layerComboChanged(self):
        self.populateFieldCombos(self.layerCombo.currentText())

    def populateList(self):
        self.chartsList.clear()
        toDelete = []
        for chartName, chart in self._charts.iteritems():
            if chart["layer"] in self.layers:
                fields = [f.name() for f in self.layers[chart["layer"]].pendingFields()]
                if chart["categoryField"] in fields:
                    item = QtGui.QListWidgetItem()
                    item.setText(chartName)
                    self.chartsList.addItem(item)
                else:
                    toDelete.append(chartName)
            else:
                toDelete.append(chartName)
        for d in toDelete:
            del self._charts[d]



    def populateLayers(self):
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

        self.layerCombo.addItems(self.layers.keys())

    def populateFieldCombos(self, layerName):
        fields = [f.name() for f in self.layers[layerName].pendingFields()]
        self.categoryFieldCombo.clear()
        self.categoryFieldCombo.addItems(fields)
        valueFieldsVisible = self.displayModeCombo.currentIndex() != 2
        if valueFieldsVisible:
            self.model = QtGui.QStandardItemModel(len(fields), 1)
            item = QtGui.QStandardItem("Select fields")
            if sys.platform in ['darwin', 'linux2']:
                self.valueFieldsCombo.setVisible(False)
                self.valueFieldsCombo.setVisible(True)
                toUse = self.valueFieldsList
                offset = 0
            else:
                self.valueFieldsCombo.setVisible(True)
                self.valueFieldsList.setVisible(False)
                toUse = self.valueFieldsCombo
                self.model.setItem(0, 0, item);
                offset = 1
            for i, f in enumerate(fields):
                item = QtGui.QStandardItem(f)
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setData(QtCore.Qt.Unchecked, QtCore.Qt.CheckStateRole);
                self.model.setItem(i + offset, 0, item);
            toUse.setModel(self.model)
        else:
            self.valueFieldsCombo.setVisible(False)
            self.valueFieldsCombo.setVisible(False)

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
        if valueFields or displayMode == 2:
            self._charts[name] = {"layer": layer,
                              "categoryField": categoryField,
                              "valueFields": valueFields,
                              "displayMode": displayMode,
                              "operation": operation}
        else:
            QtGui.QMessageBox.warning(self, "Cannot create chart", "At least one value field must be selected")
            return
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



