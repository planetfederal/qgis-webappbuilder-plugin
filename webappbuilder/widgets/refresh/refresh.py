from builtins import str
from builtins import range
from webappbuilder.webbappwidget import WebAppWidget
import os
import json
from webappbuilder.utils import findProjectLayerByName, findLayerByName, safeName

from qgis.PyQt.QtCore import Qt, QMetaObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog, QHBoxLayout, QDialogButtonBox, QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from qgis.core import QgsProject, QgsMapLayer

from webappbuilder.webbappwidget import WebAppWidget
class Refresh(WebAppWidget):

    _parameters = {"layers":{}}

    def write(self, appdef, folder, app, progress):
        refresh = []
        for lyr, interval in self._parameters["layers"].items():
            layer = findProjectLayerByName(lyr)
            if layer.dataProvider().name().lower() == "wms":
                refresh.append('''window.setInterval(function(){
                                lyr_%s.getSource().updateParams({'dummy': Math.random()});
                                }, %s);''' % (safeName(lyr), interval))
            else:
                refresh.append('''window.setInterval(function(){
                                lyr_%s.getSource().clear();
                                }, %s);''' % (safeName(lyr), interval))

        if refresh:
            app.posttarget.append('''map.once("postcompose", function(){
                                        %s
                                });''' % "\n".join(refresh))


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "refresh.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "refresh.png")

    def description(self):
        return "Refresh layers"

    def configure(self):
        dlg = RefreshDialog(self._parameters["layers"])
        dlg.exec_()
        if dlg.ok:
            self._parameters["layers"] = dlg.layers

    def checkProblems(self, appdef, problems):

        layers = self._parameters["layers"]
        if len(layers) == 0:
            problems.append("Refresh layers component added, but it has no layers configured to be refreshed.")
        for name, interval in layers.items():
            layer = findLayerByName(name, appdef["Layers"])
            if layer is None:
                problems.append("Refresh layers  component is configured to refresh a layer (%s) that is not added to web app." % name)


class RefreshDialog(QDialog):
    def __init__(self, layers):
        QDialog.__init__(self, None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.layers = dict(layers)
        self.ok = False
        self.setupUi()

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Refresh layers")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setTableContent()
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.okPressed)
        QMetaObject.connectSlotsByName(self)


    def setTableContent(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(["Layer", "Refresh interval (ms)"])
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        allLayers = QgsProject.instance().layerTreeRoot().findLayers()
        wmsLayers = [layer.layer() for layer in allLayers
                     if layer.layer().type() !=  QgsMapLayer.PluginLayer and layer.layer().dataProvider().name().lower() in ["wms", "wfs"]]
        self.table.setRowCount(len(wmsLayers))
        for i, layer in enumerate(wmsLayers):
            self.table.setRowHeight(i, 22)
            itemLayer = QTableWidgetItem(layer.name())
            itemLayer.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            self.table.setItem(i, 0, itemLayer)
            itemInterval = QTableWidgetItem("")
            itemInterval.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)
            if layer.name() in self.layers:
                value = str(self.layers[layer.name()])
                itemLayer.setCheckState(Qt.Checked)
            else:
                value = "3000"
                itemLayer.setCheckState(Qt.Unchecked)
            lineEdit = QLineEdit()
            lineEdit.setText(value)
            self.table.setCellWidget(i, 1, lineEdit)

    def okPressed(self):
        self.layers = {}
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            item.setBackground(Qt.white)
            if item.checkState() == Qt.Checked:
                try:
                    interval = int(self.table.cellWidget(i, 1).text())
                    self.layers[item.text()] = interval
                except:
                    item.setBackground(Qt.yellow)
                    return
        self.ok = True
        self.close()
