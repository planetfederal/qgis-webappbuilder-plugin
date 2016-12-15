# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from builtins import str
from builtins import range

import os

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QTreeWidgetItem, QComboBox, QLabel, QColorDialog
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsWkbTypes
from qgis.utils import iface

from webappbuilder.popupeditor import PopupEditorDialog
from webappbuilder.exceptions import WrongValueException
from webappbuilder.timeinfodialog import TimeInfoDialog
from webappbuilder.utils import (METHOD_WMS,
                                 METHOD_WMS_POSTGIS,
                                 METHOD_WFS,
                                 METHOD_WFS_POSTGIS,
                                 METHOD_DIRECT,
                                 Layer
                                )

groupIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "group.gif"))
layerIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer.png"))
pointIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_point.png"))
lineIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_line.png"))
polygonIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_polygon.png"))
rasterIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_raster.jpg"))

class TreeLayerItem(QTreeWidgetItem):

    comboStyle = '''QComboBox {
                     border: 1px solid gray;
                     border-radius: 3px;
                     padding: 1px 18px 1px 3px;
                     min-width: 6em;
                 }

                 QComboBox::drop-down {
                     subcontrol-origin: padding;
                     subcontrol-position: top right;
                     width: 15px;
                     border-left-width: 1px;
                     border-left-color: darkgray;
                     border-left-style: solid;
                     border-top-right-radius: 3px;
                     border-bottom-right-radius: 3px;
                 }
                '''
    dateTimeEditStyle = '''QDateTimeEdit {
                     border: 1px solid gray;
                     border-radius: 3px;
                     padding: 1px 18px 1px 3px;
                     min-width: 6em;
                 }

                 QDateTimeEdit::drop-down {
                     subcontrol-origin: padding;
                     subcontrol-position: top right;
                     width: 15px;
                     border-left-width: 1px;
                     border-left-color: darkgray;
                     border-left-style: solid;
                     border-top-right-radius: 3px;
                     border-bottom-right-radius: 3px;
                 }
                '''

    def __init__(self, layer, tree, isInGroup = False):
        self.popup = ""
        self.clusterColor = "#3399CC"
        self.timeInfo = None
        self.combos = []
        QTreeWidgetItem.__init__(self)
        self.layer = layer
        self.setText(0, layer.name())
        if layer.type() == layer.VectorLayer:
            if layer.geometryType() == QgsWkbTypes.PointGeometry:
                icon = pointIcon
            elif layer.geometryType() == QgsWkbTypes.LineGeometry:
                icon = lineIcon
            else:
                icon = polygonIcon
        elif layer.type() == layer.RasterLayer:
            icon = rasterIcon
        else:
            icon = layerIcon
        self.setIcon(0, icon)
        self.setCheckState(0, Qt.Checked)
        self.visibleItem = QTreeWidgetItem(self)
        self.visibleItem.setCheckState(0, Qt.Checked)
        self.visibleItem.setText(0, "Visible on startup")
        self.showInOverviewItem = QTreeWidgetItem(self)
        self.showInOverviewItem.setCheckState(0, Qt.Checked)
        self.showInOverviewItem.setText(0, "Show in overview map")
        self.showInControlsItem = QTreeWidgetItem(self)
        self.showInControlsItem.setCheckState(0, Qt.Checked)
        self.showInControlsItem.setText(0, "Show in controls")
        self.addChild(self.visibleItem)
        if layer.type() == layer.VectorLayer:
            if layer.providerType().lower() != "wfs":
                self.connTypeItem = QTreeWidgetItem(self)
                self.connTypeItem.setText(0, "Connect to this layer using")
                self.addChild(self.connTypeItem)
                self.connTypeCombo = QComboBox()
                self.connTypeCombo.setStyleSheet(self.comboStyle)
                options = ["Use file directly", "GeoServer->WMS", "GeoServer->WFS",
                           "PostGIS->GeoServer->WMS", "PostGIS->GeoServer->WFS"]
                for option in options:
                    self.connTypeCombo.addItem(option)
                tree.setItemWidget(self.connTypeItem, 1, self.connTypeCombo)
                self.connTypeCombo.currentIndexChanged.connect(self.connTypeChanged)
            self.allowSelectionItem = QTreeWidgetItem(self)
            self.allowSelectionItem.setCheckState(0, Qt.Checked)
            self.allowSelectionItem.setText(0, "Allow selection on this layer")
            self.addChild(self.allowSelectionItem)
            if layer.geometryType() == QgsWkbTypes.PointGeometry:
                self.clusterItem = QTreeWidgetItem(self)
                self.clusterItem.setCheckState(0, Qt.Unchecked)
                self.clusterItem.setText(0, "Cluster points")
                self.clusterDistanceItem = QTreeWidgetItem(self.clusterItem)
                self.clusterDistanceItem.setText(0, "Cluster distance")
                self.clusterDistanceItem.setText(1, "40")
                self.clusterDistanceItem.setFlags(self.flags() | Qt.ItemIsEditable)
                self.clusterItem.addChild(self.clusterDistanceItem)

                self.clusterColorItem = QTreeWidgetItem(self.clusterItem)
                self.clusterColorItem.setText(0, "Cluster color")
                self.clusterColorLabel = QLabel()
                self.clusterColorLabel.setText("<font style='background-color:%s; color:%s'>dummy</font> <a href='#'>Edit</a>"
                                               % (self.clusterColor, self.clusterColor))
                tree.setItemWidget(self.clusterColorItem, 1, self.clusterColorLabel)
                def editColor():
                    color = QColorDialog.getColor()
                    if color.isValid():
                        self.clusterColor = color.name()
                        self.clusterColorLabel.setText("<font style='background-color:%s; color:%s'>dummy</font> <a href='#'>Edit</a>"
                                               % (self.clusterColor, self.clusterColor))
                self.clusterColorLabel.linkActivated.connect(editColor)

                self.addChild(self.clusterItem)
        elif layer.providerType().lower() != "wms":
                self.connTypeItem = QTreeWidgetItem(self)
                self.connTypeItem.setText(0, "Connect to this layer using")
                self.addChild(self.connTypeItem)
                self.connTypeCombo = QComboBox()
                self.connTypeCombo.setStyleSheet(self.comboStyle)
                options = ["Use file directly", "GeoServer->WMS"]
                for option in options:
                    self.connTypeCombo.addItem(option)
                tree.setItemWidget(self.connTypeItem, 1, self.connTypeCombo)

        if layer.providerType().lower() == "wms" or layer.type() == layer.VectorLayer:
            self.popupItem = QTreeWidgetItem(self)
            self.popupItem.setText(0, "Info popup content")
            self.popupLabel = QLabel()
            self.popupLabel.setText("<a href='#'>Edit</a>")
            tree.setItemWidget(self.popupItem, 1, self.popupLabel)
            def editPopup():
                fields = ([f.name() for f in layer.pendingFields()]
                                if layer.type() == layer.VectorLayer else [])
                dlg = PopupEditorDialog(self.popup, fields)
                dlg.exec_()
                self.popup = dlg.text.strip()
            self.popupLabel.linkActivated.connect(editPopup)
            self.addChild(self.popupItem)
        if layer.type() == layer.VectorLayer:
            self.timeInfoItem = QTreeWidgetItem(self)
            self.timeInfoItem.setText(0, "Layer time info")
            self.timeInfoLabel = QLabel()
            self.timeInfoLabel.setText("<a href='#'>Edit</a>")
            tree.setItemWidget(self.timeInfoItem, 1, self.timeInfoLabel)
            def editTimeInfo():
                dlg = TimeInfoDialog(self.timeInfo, layer)
                dlg.exec_()
                if dlg.ok:
                    self.timeInfo = dlg.timeInfo
            self.timeInfoLabel.linkActivated.connect(editTimeInfo)
            self.addChild(self.timeInfoItem)

        self.singleTileItem = QTreeWidgetItem(self)
        self.singleTileItem.setCheckState(0, Qt.Unchecked)
        self.singleTileItem.setText(0, "Do not consume as tiled layer")
        self.addChild(self.singleTileItem)
        self.singleTileItem.setDisabled(layer.providerType().lower() not in ["wms", "wfs"])

    def connTypeChanged(self):
        try:
            current = self.connTypeCombo.currentIndex()
            disable = current in [METHOD_WMS, METHOD_WMS_POSTGIS]
            if self.layer.type() == self.layer.VectorLayer:
                if self.layer.geometryType() == QgsWkbTypes.PointGeometry:
                    self.clusterItem.setDisabled(disable)
                    self.clusterDistanceItem.setDisabled(disable)
                    self.clusterColorItem.setDisabled(disable)
                self.popupItem.setDisabled(disable)
                self.popupLabel.setDisabled(disable)
                self.allowSelectionItem.setDisabled(disable)
            try:
                disable = (self. layer.providerType().lower() not in ["wms", "wfs"]
                            and current not in
                            [METHOD_WMS, METHOD_WMS_POSTGIS, METHOD_WFS, METHOD_WFS_POSTGIS])
                self.singleTileItem.setDisabled(disable)
            except:
                pass
        except:
            try:
                self.singleTileItem.setDisabled(False)
            except:
                pass

    def toggleChildren(self):
        disabled = self.checkState(0) == Qt.Unchecked
        for i in range(self.childCount()):
            subitem = self.child(i)
            subitem.setDisabled(disabled)
        try:
            self.connTypeCombo.setDisabled(disabled)
        except:
            pass
        try:
            self.popupLabel.setDisabled(disabled)
        except:
            pass
        try:
            self.clusterDistanceItem.setDisabled(disabled)
        except:
            pass
        if not disabled:
            self.connTypeChanged()

    @property
    def allowSelection(self):
        try:
            return self.allowSelectionItem.checkState(0) == Qt.Checked
        except:
            return False

    @property
    def visible(self):
        return self.visibleItem.checkState(0) == Qt.Checked

    @property
    def showInOverview(self):
        return self.showInOverviewItem.checkState(0) == Qt.Checked

    @property
    def showInControls(self):
        return self.showInControlsItem.checkState(0) == Qt.Checked

    @property
    def singleTile(self):
        try:
            return self.singleTileItem.checkState(0) == Qt.Checked
        except:
            return False

    @property
    def method(self):
        try:
            return self.connTypeCombo.currentIndex()
        except:
            return METHOD_DIRECT

    @property
    def clusterDistance(self):
        try:
            if self.clusterItem.checkState(0) == Qt.Checked:
                dist = self.clusterDistanceItem.text(1)
            else:
                return 0
        except:
            return 0
        try:
            f =  float(dist)
            return f
        except:
            raise WrongValueException()

    def setValues(self, visible, popup, method, clusterDistance, clusterColor,
                  allowSelection, showInOverview, timeInfo,
                  showInControls, singleTile):
        self.timeInfo = timeInfo

        if clusterDistance:
            self.clusterItem.setCheckState(0, Qt.Checked)
            self.clusterDistanceItem.setText(1, str(clusterDistance))
            self.clusterColor = clusterColor
            self.clusterColorLabel.setText("<font style='background-color:%s; color:%s'>dummy</font> <a href='#'>Edit</a>"
                                               % (self.clusterColor, self.clusterColor))
        else:
            try:
                self.clusterItem.setCheckState(0, Qt.Unchecked)
                self.clusterDistanceItem.setText(1, "40")
            except AttributeError:
                pass # raster layers wont have this clusterItem

        try:
            self.allowSelectionItem.setCheckState(0, Qt.Checked if allowSelection else Qt.Unchecked)
        except:
            pass
        try:
            self.singleTileItem.setCheckState(0, Qt.Checked if singleTile else Qt.Unchecked)
        except:
            pass
        self.visibleItem.setCheckState(0, Qt.Checked if visible else Qt.Unchecked)
        try:
            self.connTypeCombo.setCurrentIndex(method)
        except:
            pass
        self.popup = popup
        self.showInOverviewItem.setCheckState(0, Qt.Checked if showInOverview else Qt.Unchecked)
        self.showInControlsItem.setCheckState(0, Qt.Checked if showInControls else Qt.Unchecked)

    def appLayer(self):
        return Layer(self.layer, self.visible, self.popup, self.method,
                     self.clusterDistance, self.clusterColor,self.allowSelection,
                     self.showInOverview, self.timeInfo,self.showInControls, self.singleTile)


class TreeGroupItem(QTreeWidgetItem):

    def __init__(self, name, layers, layersTree):
        visibleLayers = iface.mapCanvas().layers()
        QTreeWidgetItem.__init__(self)
        skipType = [2]
        self.showContentItem = QTreeWidgetItem(self)
        self.showContentItem.setCheckState(0, Qt.Checked)
        self.showContentItem.setText(0, "Show group content in layers list")
        self.layers = layers
        self.name = name
        self.setText(0, name)
        self.setIcon(0, groupIcon)
        for layer in layers:
            if layer.type() not in skipType:
                item = TreeLayerItem(layer, layersTree, True)
                item.setCheckState(0, Qt.Checked if layer in visibleLayers else Qt.Unchecked)
                item.toggleChildren()
                self.addChild(item)

    def showContent(self):
        return self.showContentItem.checkState(0) == Qt.Checked

    def setShowContent(self, showContent):
        return self.showContentItem.setCheckState(0, Qt.Checked if showContent else Qt.Unchecked)
