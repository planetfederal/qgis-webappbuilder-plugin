from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
from qgis.core import *
from popupeditor import PopupEditorDialog
from utils import *
from settings import WrongValueException
from qgis.utils import iface

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
        self.combos = []
        QTreeWidgetItem.__init__(self)
        self.layer = layer
        self.setText(0, layer.name())
        if layer.type() == layer.VectorLayer:
            if layer.geometryType() == QGis.Point:
                icon = pointIcon
            elif layer.geometryType() == QGis.Line:
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
            if layer.geometryType() == QGis.Point:
                self.clusterItem = QTreeWidgetItem(self)
                self.clusterItem.setCheckState(0, Qt.Unchecked)
                self.clusterItem.setText(0, "Cluster points")
                self.clusterDistanceItem = QTreeWidgetItem(self.clusterItem)
                self.clusterDistanceItem.setText(0, "Cluster distance")
                self.clusterDistanceItem.setText(1, "40")
                self.clusterDistanceItem.setFlags(self.flags() | Qt.ItemIsEditable)
                self.clusterItem.addChild(self.clusterDistanceItem)
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
            def edit():
                fields = ([f.name() for f in self.layer.pendingFields()]
                                if layer.type() == layer.VectorLayer else [])
                dlg = PopupEditorDialog(self.popup, fields)
                dlg.exec_()
                self.popup = dlg.text.strip()
            self.popupLabel.connect(self.popupLabel, SIGNAL("linkActivated(QString)"), edit)
            self.addChild(self.popupItem)

        if isInGroup:
            self.timeInfoItem = QTreeWidgetItem(self)
            self.timeInfoItem.setText(0, "Layer time info")
            self.calendar = NullableDateWidget()
            self.calendar.setCalendarPopup(True)
            self.calendar.setDateTime(QDateTime())
            self.calendar.setStyleSheet(self.dateTimeEditStyle)
            tree.setItemWidget(self.timeInfoItem, 1, self.calendar)
            self.addChild(self.timeInfoItem)

        if layer.providerType().lower() in ["wms"]:
            self.refreshItem = QTreeWidgetItem(self)
            self.refreshItem.setCheckState(0, Qt.Unchecked)
            self.refreshItem.setText(0, "Refresh layer automatically")
            self.refreshIntervalItem = QTreeWidgetItem(self.refreshItem)
            self.refreshIntervalItem.setText(0, "Refresh interval (millisecs)")
            self.refreshIntervalItem.setText(1, "3000")
            self.refreshIntervalItem.setFlags(self.flags() | Qt.ItemIsEditable)
            self.refreshItem.addChild(self.refreshIntervalItem)
            self.addChild(self.refreshItem)


    def connTypeChanged(self):
        try:
            current = self.connTypeCombo.currentIndex()
            disable = current in [METHOD_WMS, METHOD_WMS_POSTGIS]
            self.popupItem.setDisabled(disable)
            self.popupLabel.setDisabled(disable)
            self.allowSelectionItem.setDisabled(disable)
            self.clusterItem.setDisabled(disable)
            self.clusterDistanceItem.setDisabled(disable)
        except:
            pass

    def toggleChildren(self):
        disabled = self.checkState(0) == Qt.Unchecked
        for i in xrange(self.childCount()):
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

    @property
    def refreshInterval(self):
        try:
            if self.refreshItem.checkState(0) == Qt.Checked:
                t = self.refreshIntervalItem.text(1)
            else:
                return 0
        except:
            return 0
        try:
            interval = int(t)
            return interval
        except:
            raise WrongValueException()

    @property
    def timeInfo(self):
        try:
            return self.calendar.nullDateTime()
        except:
            return None


    def setValues(self, visible, popup, method, clusterDistance, allowSelection,
                  refreshInterval, showInOverview, timeInfo):
        if clusterDistance:
            self.clusterItem.setCheckState(0, Qt.Checked)
            self.clusterDistanceItem.setText(1, str(clusterDistance))
        else:
            try:
                self.clusterItem.setCheckState(0, Qt.Unchecked)
                self.clusterDistanceItem.setText(1, "40")
            except AttributeError:
                pass # raster layers wont have this clusterItem

        try:
            self.calendar.setDateTime(QDateTime.fromMSecsSinceEpoch(timeInfo))
        except:
            pass

        if refreshInterval:
            self.refreshItem.setCheckState(0, Qt.Checked)
            self.refreshIntervalItem.setText(1, str(refreshInterval))
        else:
            try:
                self.refreshItem.setCheckState(0, Qt.Unchecked)
                self.refreshIntervalItem.setText(1, "3000")
            except AttributeError:
                pass
        try:
            self.allowSelectionItem.setCheckState(0, Qt.Checked if allowSelection else Qt.Unchecked)
        except:
            pass
        self.visibleItem.setCheckState(0, Qt.Checked if visible else Qt.Unchecked)
        try:
            self.connTypeCombo.setCurrentIndex(method)
        except:
            pass
        self.popup = popup
        self.showInOverviewItem.setCheckState(0, Qt.Checked if showInOverview else Qt.Unchecked)

    def appLayer(self):
        return Layer(self.layer, self.visible, self.popup, self.method,
                     self.clusterDistance, self.allowSelection, self.refreshInterval,
                     self.showInOverview, self.timeInfo)

class TreeGroupItem(QTreeWidgetItem):

    def __init__(self, name, layers, layersTree):
        visibleLayers = iface.mapCanvas().layers()
        QTreeWidgetItem.__init__(self)
        skipType = [2]
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

class NullableDateWidget(QDateTimeEdit):

    def __init__(self):
        QDateEdit.__init__(self)
        self._date = None
        self.setSpecialValueText("Not set");

    def clear(self):
        self.setDate(self.minimumDate())

    def nullDateTime(self):
        if self.dateTime() == self.minimumDateTime():
            return None;
        return self.dateTime().toMSecsSinceEpoch();

    def setDateTime(self, date):
        if (date.isNull() or not date.isValid()):
            QDateEdit.setDateTime(self, self.minimumDateTime())
        else:
            QDateEdit.setDateTime(self, date)




