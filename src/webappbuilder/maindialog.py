import os
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from ui_maindialog import Ui_MainDialog
import utils
from collections import defaultdict
from olwriter import writeOL
from qgis.utils import iface
from appcreator import createApp
from settings import *
from types import MethodType
from texteditor import *
import webbrowser
from parameditor import ParametersEditorDialog
from treesettingsitem import TreeSettingItem
from utils import METHOD_WMS, METHOD_WMS_POSTGIS


class Layer():

    def __init__(self, layer, visible, popup, method, clusterDistance):
        self.layer = layer
        self.visible = visible
        self.popup = popup
        self.method = method
        self.clusterDistance = clusterDistance

groupIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "group.gif"))
layerIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer.png"))
pointIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_point.png"))
lineIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_line.png"))
polygonIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_polygon.png"))
rasterIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_raster.jpg"))

class WrongValueException(Exception):
    pass

class MainDialog(QDialog, Ui_MainDialog):

    items = {}

    def __init__(self, appdef):
        QDialog.__init__(self)
        self.setupUi(self)
        self.populateLayers()
        self.populateConfigParams()
        self.buttonPreview.clicked.connect(self.updatePreview)
        self.buttonCustomBaseLayers.clicked.connect(self.customBaseLayers)
        self.buttonCreateApp.clicked.connect(self.createApp)
        self.buttonSelectImgFilepath.clicked.connect(self.selectImgFilepath)
        self.checkBoxDeployData.stateChanged.connect(self.deployCheckChanged)
        self.connect(self.labelEditHeaderCss, SIGNAL("linkActivated(QString)"),
                     self.editHeaderCss)
        self.connect(self.labelEditFooterCss, SIGNAL("linkActivated(QString)"),
                     self.editFooterCss)
        self.connect(self.labelEditPopupCss, SIGNAL("linkActivated(QString)"),
                     self.editPopupCss)
        self.currentBaseLayerItem = self.mapQuestAerialButton
        self.mapQuestAerialButton.setChecked(True)
        self.baseLayerButtons = [self.mapQuestButton, self.mapQuestAerialButton, self.stamenTonerButton, self.stamenWatercolorButton, self.osmButton]
        self.baseLayers = {self.mapQuestButton: "MapQuest roads",
                            self.mapQuestAerialButton: "MapQuest aerial",
                            self.stamenTonerButton: "Stamen toner",
                            self.stamenWatercolorButton: "Stamen watercolor",
                            self.osmButton: "OSM"}

        widgetButtons = {self.attributesTableButton: "Attributes table",
                        self.attributionButton: "Attribution",
                        self.fullScreenButton: "Full screen",
                        self.layersListButton: "Layers list",
                        self.legendButton: "Legend",
                        self.mousePositionButton: "Mouse position",
                        self.northArrowButton: "North arrow",
                        self.overviewButton: "Overview map",
                        self.scaleBarButton: "Scale bar",
                        self.searchButton: "Search button",
                        self.zoomControlsButton: "Zoom controls",
                        self.zoomSliderButton: "Zoom slider",
                        self.zoomToExtentButton: "Zoom to extent",
                        self.cesiumButton: "3D view",
                        self.editToolButton: "Edit tool",
                        self.textPanelButton: "Text panel",
                        self.exportAsImageButton: "Export as image",
                        self.geolocationButton: "Geolocation",
                        self.geocodingButton: "Geocoding",
                        self.chartToolButton: "Chart tool"}

        def _mousePressEvent(selfb, event):
            QToolButton.mousePressEvent(selfb, event)
            if event.button() == Qt.RightButton :
                name = widgetButtons[selfb]
                menu = QMenu()
                cssAction = QAction("Edit widget CSS...", None)
                cssAction.triggered.connect(lambda: self.editWidgetCss(name))
                menu.addAction(cssAction)
                if name == "Text panel":
                    s = "Edit panel content..."
                else:
                    s = "Edit widget parameters..."
                paramsAction = QAction(s, None)
                paramsAction.triggered.connect(lambda: self.editWidgetParameters(name))
                paramsAction.setEnabled(name in widgetsParams)
                menu.addAction(paramsAction)
                point = selfb.mapToGlobal(event.pos())
                menu.exec_(point)

        for b in widgetButtons:
            b.mousePressEvent = MethodType(_mousePressEvent, b, QToolButton)

        self.widgetButtons = widgetButtons

        self.progressBar.setVisible(False)
        self.progressLabel.setVisible(False)

        class Progress():
            def setText(_, text):
                self.progressLabel.setText(text)
                QApplication.processEvents()
            def setProgress(_, i):
                self.progressBar.setValue(i)
                QApplication.processEvents()

        self.progress = Progress()

        if appdef is not None:
            self.loadAppdef(appdef)

    def customBaseLayers(self):
        pass

    def loadAppdef(self, appdef):
        pass

    def deployCheckChanged(self):
        self.geoserverGroupBox.setEnabled(not self.checkBoxDeployData.isChecked())
        self.postgisGroupBox.setEnabled(not self.checkBoxDeployData.isChecked())

    def editHeaderCss(self):
        dlg = TextEditorDialog(cssStyles["Header"], CSS, "Header")
        dlg.exec_()
        cssStyles["Header"] = dlg.text

    def editFooterCss(self):
        dlg = TextEditorDialog(cssStyles["Footer"], CSS, "Footer")
        dlg.exec_()
        cssStyles["Footer"] = dlg.text

    def editPopupCss(self):
        dlg = TextEditorDialog(cssStyles["Popup"], CSS, "Popup")
        dlg.exec_()
        cssStyles["Popup"] = dlg.text

    def editWidgetParameters(self, widgetName):
        if widgetName == "Text panel":
            dlg = TextEditorDialog(widgetsParams[widgetName]["HTML content"], HTML)
            dlg.exec_()
            widgetsParams[widgetName]["HTML content"] = dlg.text
        else:
            dlg = ParametersEditorDialog(widgetsParams[widgetName])
            dlg.exec_()
            widgetsParams[widgetName] = dlg.params

    def editWidgetCss(self, widgetName):
        dlg = TextEditorDialog(cssStyles.get(widgetName, ""), CSS, widgetName)
        dlg.exec_()
        cssStyles[widgetName] = dlg.text


    def selectImgFilepath(self):
        folder = QFileDialog.getOpenFileName(self, "Select header image file")
        if folder is None:
            self.imgFilepathBox.setText(folder)

    def populateLayers(self):
        skipType = [2]
        root = QgsProject.instance().layerTreeRoot()
        for child in root.children():
            if isinstance(child, QgsLayerTreeGroup):
                layers = []
                for subchild in child.children():
                    if isinstance(subchild, QgsLayerTreeLayer):
                        layers.append(subchild.layer())
                item = TreeGroupItem(child.name(), layers, self.layersTree)
                self.layersTree.addTopLevelItem(item)
            elif isinstance(child, QgsLayerTreeLayer):
                layer = child.layer()
                if layer.type() not in skipType:
                    item = TreeLayerItem(layer, self.layersTree)
                    self.layersTree.addTopLevelItem(item)

        self.layersTree.expandAll()
        self.layersTree.resizeColumnToContents(0)
        self.layersTree.resizeColumnToContents(1)

    def populateConfigParams(self):
        self.settingsItems = defaultdict(dict)
        item = QTreeWidgetItem()
        item.setText(0, "Settings")
        for param, value in appSettings.iteritems():
            subitem = TreeSettingItem(item, self.settingsTree, param, value)
            item.addChild(subitem)
            self.settingsItems[param] = subitem
        self.settingsTree.addTopLevelItem(item)
        item.sortChildren(0, Qt.AscendingOrder)
        self.settingsTree.expandAll()
        self.settingsTree.resizeColumnToContents(0)
        self.settingsTree.resizeColumnToContents(1)

    def _run(self, f):
        self.progressBar.setVisible(True)
        self.progressLabel.setVisible(True)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            f()
        finally:
            self.progressBar.setVisible(False)
            self.progressLabel.setVisible(False)
            QApplication.restoreOverrideCursor()

    def updatePreview(self):
        try:
            appdef = self.createAppDefinition(True)
            path = self._run(lambda: writeOL(appdef, utils.tempFolder(), True, self.progress))
            path = "file:///" + path.replace("\\","/")
            webbrowser.open_new(path)
        except WrongValueException:
            pass

    def createApp(self):
        try:
            #folder = QFileDialog.getExistingDirectory(self, "Select folder to store app")
            folder = "d:\\deploy"
            if folder is None:
                return
            appdef = self.createAppDefinition()
            self._run(lambda: createApp(appdef, not self.checkBoxDeployData.isChecked(), folder, self.progress))
            msgBox = QMessageBox()
            msgBox.setWindowTitle("Web app creator")
            msgBox.setText("App was correctly created and deployed")
            msgBox.setInformativeText("Do you want to open it in a web browser?");
            msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No);
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setDefaultButton(QMessageBox.Yes);
            ret = msgBox.exec_();
            if ret == QMessageBox.Yes:
                webbrowser.open_new("file://%s/index.html" % folder)
        except WrongValueException:
            pass

    def createAppDefinition(self, preview = False):
        layers, groups = self.getLayersAndGroups()
        appdef = {}
        appdef["Settings"] = self.getSettings()
        appdef["Base layers"] = self.getBaseLayers()
        appdef["Layers"] = layers
        if preview:
            for layer in layers:
                providerType = layer.layer.providerType().lower()
                if providerType not in ["wms", "wfs"]:
                    layer.method = utils.METHOD_FILE
        appdef["Groups"] = groups
        appdef["Widgets"] = self.getWidgets()
        deploy = not (self.checkBoxDeployData.isChecked() or preview)
        if deploy:
            appdef["Deploy"] = self.getDeployConfiguration(layers)
            if appdef["Deploy"]["GeoServer workspace"] == "":
                appdef["Deploy"]["GeoServer workspace"] = utils.safeName(appdef["Settings"]["Title"])
            if appdef["Deploy"]["PostGIS schema"] == "":
                appdef["Deploy"]["PostGIS schema"] = utils.safeName(appdef["Settings"]["Title"])
        else:
            appdef["Deploy"] = {}
        return appdef

    def getBaseLayers(self):
        layers = []
        for b in self.baseLayerButtons:
            if b.isChecked():
                layers.append(self.baseLayers[b])
        return layers

    def getWidgets(self):
        widgets = {}
        for button, name in self.widgetButtons.iteritems():
            if button.isChecked():
                widgetParams = widgetsParams.get(name, {}).copy()
                for k, v, in widgetParams.iteritems():
                    if isinstance(v, tuple):
                        widgetParams[k] = v[0]
                widgets[name] = {"Params": widgetParams, "Css": cssStyles.get(name,"")}
        return widgets

    def _getValue(self, textbox, mandatory):
        textbox.setStyleSheet("QLineEdit{background: white}")
        value = textbox.text().strip()
        if value == "" and mandatory:
            textbox.setStyleSheet("QLineEdit{background: yellow}")
            raise WrongValueException()
        return value

    def getDeployConfiguration(self, layers):
        usesGeoServer = False
        usesPostgis = False
        for layer in layers:
            if layer.method != utils.METHOD_FILE:
                if layer.layer.type() == layer.layer.VectorLayer and layer.layer.providerType().lower() != "wfs":
                    usesPostgis = True
                    usesGeoServer = True
                elif layer.layer.type() == layer.layer.RasterLayer and layer.layer.providerType().lower() != "wms":
                    usesGeoServer = True
        try:
            params = {
                "PostGIS host": self._getValue(self.postgisHostBox, usesPostgis),
                "PostGIS port": self._getValue(self.postgisPortBox, usesPostgis),
                "PostGIS database": self._getValue(self.postgisDatabaseBox, usesPostgis),
                "PostGIS schema": self.postgisSchemaBox.text().strip(),
                "PostGIS username": self._getValue(self.postgisUsernameBox, usesPostgis),
                "PostGIS password": self._getValue(self.postgisPasswordBox, usesPostgis),
                "GeoServer url": self._getValue(self.geoserverUrlBox, usesGeoServer).strip("/"),
                "GeoServer username": self._getValue(self.geoserverUsernameBox, usesGeoServer),
                "GeoServer password": self._getValue(self.geoserverPasswordBox, usesGeoServer),
                "GeoServer workspace": self.geoserverWorkspaceBox.text().strip(),
            }
            return params
        except WrongValueException, e:
            self.tabPanel.setCurrentIndex(4)
            raise e


    def getSettings(self):
        try:
            title = self._getValue(self.titleBox, True)
        except WrongValueException, e:
            self.tabPanel.setCurrentIndex(0)
            raise e
        parameters = {"Title": title}
        if self.groupFooter.isChecked():
            parameters.update({"Footer text": self.footerTextBox.toPlainText().strip(),
                      "Footer css": cssStyles["Footer"]})
        if self.groupHeader.isChecked():
            parameters.update({"Header text": self.headerTextBox.toPlainText().strip(),
                      "Header css": cssStyles["Header"],
                      "Header image": self.imgFilepathBox.text().strip()})
        parameters.update({"Popup css": cssStyles["Popup"]})
        try:
            for param, item in self.settingsItems.iteritems():
                parameters[param] = item.value()
        except WrongValueException, e:
            self.tabPanel.setCurrentIndex(5)
            raise e

        return parameters

    def getLayersAndGroups(self):
        layers = []
        groups = {}
        for i in xrange(self.layersTree.topLevelItemCount()):
            item = self.layersTree.topLevelItem(i)
            if isinstance(item, TreeLayerItem):
                if item.checkState(0) == Qt.Checked:
                    layers.append(item.appLayer())
            else:
                for j in xrange(item.childCount()):
                    subitem = item.child(j)
                    layers.append(subitem.appLayer())
                groups[item.name] = item.layers[::-1]

        return layers[::-1], groups


class TreeGroupItem(QTreeWidgetItem):

    def __init__(self, name, layers, layersTree):
        QTreeWidgetItem.__init__(self)
        skipType = [2]
        self.layers = layers
        self.name = name
        self.setText(0, name)
        self.setIcon(0, groupIcon)
        for layer in layers:
            if layer.type() not in skipType:
                item = TreeLayerItem(layer, layersTree)
                self.addChild(item)

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
    def __init__(self, layer, tree):
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
        self.addChild(self.visibleItem)
        if layer.type() == layer.VectorLayer:
            if layer.providerType().lower() != "wfs":
                self.connTypeItem = QTreeWidgetItem(self)
                self.connTypeItem.setText(0, "Connect to this layer using")
                self.addChild(self.connTypeItem)
                self.connTypeCombo = QComboBox()
                self.connTypeCombo.setStyleSheet(self.comboStyle)
                options = ["Use file directly", "GeoServer->WMS", "GeoServer->WFS", "PostGIS->GeoServer->WMS", "PostGIS->GeoServer->WFS"]
                for option in options:
                    self.connTypeCombo.addItem(option)
                tree.setItemWidget(self.connTypeItem, 1, self.connTypeCombo)
                self.connTypeCombo.currentIndexChanged.connect(self.connTypeChanged)
            self.popupItem = QTreeWidgetItem(self)
            self.popupItem.setText(0, "Info popup content")
            self.popupCombo = QComboBox()
            self.popupCombo.setStyleSheet(self.comboStyle)
            options = ["No popup", "Show all attributes"]
            options.extend(["FIELD:" + f.name() for f in self.layer.pendingFields()])
            for option in options:
                self.popupCombo.addItem(option)
            self.addChild(self.popupItem)
            tree.setItemWidget(self.popupItem, 1, self.popupCombo)
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
        else:
            if layer.providerType().lower() != "wms":
                self.connTypeItem = QTreeWidgetItem(self)
                self.connTypeItem.setText(0, "Connect to this layer using")
                self.addChild(self.connTypeItem)
                self.connTypeCombo = QComboBox()
                self.connTypeCombo.setStyleSheet(self.comboStyle)
                options = ["Use file directly", "GeoServer->WMS"]
                for option in options:
                    self.connTypeCombo.addItem(option)
                tree.setItemWidget(self.connTypeItem, 1, self.connTypeCombo)

    def connTypeChanged(self):
        current = self.connTypeCombo.currentIndex()
        disable = current in [METHOD_WMS, METHOD_WMS_POSTGIS]
        try:
            self.popupItem.setDisabled(disable)
            self.popupCombo.setDisabled(disable)
            self.clusterItem.setDisabled(disable)
            self.clusterDistanceItem.setDisabled(disable)
        except:
            pass

    @property
    def popup(self):
        try:
            idx = self.popupCombo.currentIndex()
            options = [utils.NO_POPUP, utils.ALL_ATTRIBUTES]
            popup = options[idx] if idx < 2 else '"%s"' % self.popupCombo.currentText()[len("FIELD:"):]
        except:
            popup = utils.NO_POPUP
        return popup

    @property
    def visible(self):
        return self.visibleItem.checkState(0) == Qt.Checked

    @property
    def method(self):
        try:
            return self.connTypeCombo.currentIndex()
        except:
            return utils.METHOD_DIRECT

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

    def appLayer(self):
        return Layer(self.layer, self.visible, self.popup, self.method, self.clusterDistance)


