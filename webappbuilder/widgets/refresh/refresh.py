from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4 import QtCore, QtGui
import json
from qgis.core import *
from webappbuilder.utils import findProjectLayerByName, findLayerByName, safeName

class Refresh(WebAppWidget):

    _parameters = {"layers":{}}

    def write(self, appdef, folder, app, progress):
        refresh = []
        for lyr, interval in self._parameters["layers"].iteritems():
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
        return QtGui.QIcon(os.path.join(os.path.dirname(__file__), "refresh.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "refresh.png")

    def description(self):
        return "Refresh layers"

    def configure(self):
        dlg = RefreshDialog(self._parameters["layers"])
        dlg.exec_()
        if dlg.ok:
            self._parameters["layers"] = dlg.layers

    def checkProblems(self, appdef, problems, forPreview):

        layers = self._parameters["layers"]
        if len(layers) == 0:
            problems.append("Refresh layers component added, but it has no layers configured to be refreshed.")
        for name, interval in layers.iteritems():
            layer = findLayerByName(name, appdef["Layers"])
            if layer is None:
                problems.append("Refresh layers  component is configured to refresh a layer (%s) that is not added to web app." % name)


class RefreshDialog(QtGui.QDialog):
    def __init__(self, layers):
        QtGui.QDialog.__init__(self, None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.layers = dict(layers)
        self.ok = False
        self.setupUi()

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Refresh layers")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setTableContent()
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.okPressed)
        QtCore.QMetaObject.connectSlotsByName(self)


    def setTableContent(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(["Layer", "Refresh interval (ms)"])
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        allLayers = QgsProject.instance().layerTreeRoot().findLayers()
        wmsLayers = [layer.layer() for layer in allLayers
                     if layer.layer().type() !=  QgsMapLayer.PluginLayer and layer.layer().dataProvider().name().lower() in ["wms", "wfs"]]
        self.table.setRowCount(len(wmsLayers))
        for i, layer in enumerate(wmsLayers):
            self.table.setRowHeight(i, 22)
            itemLayer = QtGui.QTableWidgetItem(layer.name())
            itemLayer.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            self.table.setItem(i, 0, itemLayer)
            itemInterval = QtGui.QTableWidgetItem("")
            itemInterval.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            if layer.name() in self.layers:
                value = str(self.layers[layer.name()])
                itemLayer.setCheckState(QtCore.Qt.Checked)
            else:
                value = "3000"
                itemLayer.setCheckState(QtCore.Qt.Unchecked)
            lineEdit = QtGui.QLineEdit()
            lineEdit.setText(value)
            self.table.setCellWidget(i, 1, lineEdit)

    def okPressed(self):
        self.layers = {}
        for i in xrange(self.table.rowCount()):
            item = self.table.item(i, 0)
            item.setBackground(QtCore.Qt.white)
            if item.checkState() == QtCore.Qt.Checked:
                try:
                    interval = int(self.table.cellWidget(i, 1).text())
                    self.layers[item.text()] = interval
                except:
                    item.setBackground(QtCore.Qt.yellow)
                    return
        self.ok = True
        self.close()
