import sys
import os
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
import utils
from collections import defaultdict
from qgis.utils import iface
from appcreator import createApp, AppDefProblemsDialog, loadAppdef, saveAppdef, checkAppCanBeCreated
import settings
from types import MethodType
import webbrowser
from treesettingsitem import TreeSettingItem
from utils import *
from functools import partial
from settings import outputFolders, webAppWidgets
import traceback
from treelayeritem import TreeLayerItem, TreeGroupItem
from exceptions import WrongValueException
from PyQt4 import uic

# Adding so that our UI files can find resources_rc.py
sys.path.append(os.path.dirname(__file__))

WIDGET, BASE = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'ui_maindialog.ui'))

class MainDialog(BASE, WIDGET):

    items = {}

    def __init__(self, appdef):
        QDialog.__init__(self)
        self.setupUi(self)
        self.widgetButtons = {}
        self.populateLayers()
        self.populateBaseLayers()
        self.populateConfigParams()
        self.populateThemes()
        self.populateWidgets()
        self.buttonLogo.clicked.connect(self.selectLogo)
        self.buttonCreateApp.clicked.connect(self.createApp)
        self.checkBoxDeployData.stateChanged.connect(self.deployCheckChanged)
        self.tabPanel.currentChanged.connect(self.tabChanged)
        self.expandLayersButton.clicked.connect(lambda: self.layersTree.expandAll())
        self.collapseLayersButton.clicked.connect(self.collapseLayers)
        self.filterLayersBox.textChanged.connect(self.filterLayers)
        self.buttonOpen.setIcon(QgsApplication.getThemeIcon('/mActionFileOpen.svg'))
        self.buttonSave.setIcon(QgsApplication.getThemeIcon('/mActionFileSave.svg'))
        self.buttonHelp.setIcon(QgsApplication.getThemeIcon('/mActionHelpAPI.png'))
        self.buttonOpen.clicked.connect(self.openAppdef)
        self.buttonSave.clicked.connect(self.saveAppdef)
        self.buttonHelp.clicked.connect(self.showHelp)

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

        self.tabPanel.setCurrentIndex(0)

    def showHelp(self):
        webbrowser.open_new("http://qgis.boundlessgeo.com/static/webappbuilder/usage.rst")

    def tabChanged(self, index):
        if index == 4:
            self.updateDeployGroups()

    def updateDeployGroups(self):
        postGisMethods = [utils.METHOD_WMS_POSTGIS, utils.METHOD_WFS_POSTGIS]
        geoServerMethods = [utils.METHOD_WMS_POSTGIS, utils.METHOD_WFS_POSTGIS,
                           utils.METHOD_WMS, utils.METHOD_WFS]
        usesGeoServer = False
        usesPostGis = False
        layers, _ = self.getLayersAndGroups()
        for layer in layers:
            if layer.method in geoServerMethods:
                usesGeoServer = True
                if layer.method in postGisMethods:
                    usesPostGis = True
        self.geoserverGroupBox.setEnabled(usesGeoServer)
        self.postgisGroupBox.setEnabled(not self.checkBoxDeployData.isChecked() and usesPostGis)

    def collapseLayers(self):
        self.layersTree.collapseAll()
        for i in xrange(self.layersTree.topLevelItemCount()):
            item = self.layersTree.topLevelItem(i)
            if isinstance(item, TreeGroupItem):
                item.setExpanded(True)

    def filterLayers(self):
        text = self.filterLayersBox.text()
        for i in xrange(self.layersTree.topLevelItemCount()):
            item = self.layersTree.topLevelItem(i)
            if isinstance(item, TreeLayerItem):
                itemText = item.text(0)
                item.setHidden(text != "" and text not in itemText)
            else:
                groupVisible = False
                for j in xrange(item.childCount()):
                    subitem = item.child(j)
                    subitemText = subitem.text(0)
                    hidden = text != "" and text not in subitemText
                    if not hidden:
                        groupVisible = True
                    subitem.setHidden(hidden)
                item.setHidden(not groupVisible)

    def selectLogo(self):
        img = QFileDialog.getOpenFileName(self, "Select image file")
        if img:
            self.logoBox.setText(img)

    def openAppdef(self):
        appdefFile = QFileDialog.getOpenFileName(self, "Select app definition file", "",
                                          "Appdef files (*.appdef)")
        if appdefFile:
            appdef = loadAppdef(appdefFile)
            if appdef:
                self.loadAppdef(appdef)
                self.tabPanel.setCurrentIndex(0)


    def saveAppdef(self):
        appdefFile = QFileDialog.getSaveFileName(self, "Select app definition file", "",
                                          "Appdef files (*.appdef)")
        if appdefFile:
            saveAppdef(self.createAppDefinition(False), appdefFile)

    def loadAppdef(self, appdef):
        try:
            self.titleBox.setText(appdef["Settings"]["Title"])
            self.logoBox.setText(appdef["Settings"]["Logo"])
            for button, widgetName in self.widgetButtons.iteritems():
                if widgetName in appdef["Widgets"]:
                    button.setChecked(True)
                    button.webAppWidget.setParameters(appdef["Widgets"][widgetName]["Parameters"])

            for name in self.settingsItems:
                if name in appdef["Settings"]:
                    self.settingsItems[name].setValue(appdef["Settings"][name])
            theme = appdef["Settings"]["Theme"]
            for button, themeName in self.themesButtons.iteritems():
                if themeName == theme:
                    button.click()
            baseLayers = appdef["Base layers"]
            for button, name in self.baseLayers.iteritems():
                button.setChecked(name in baseLayers)
            for button, name in self.baseOverlays.iteritems():
                button.setChecked(name in baseLayers)
            items = []
            for i in xrange(self.layersTree.topLevelItemCount()):
                item = self.layersTree.topLevelItem(i)
                if isinstance(item, TreeLayerItem):
                    items.append(item)
                else:
                    try:
                        item.setShowContent(appdef["Groups"][item.text(0)]["showContent"])
                    except:
                        pass
                    for j in xrange(item.childCount()):
                        subitem = item.child(j)
                        if isinstance(subitem, TreeLayerItem):
                            items.append(subitem)

            layers = {lay["layer"]: lay for lay in appdef["Layers"]}
            for item in items:
                if item.layer.name() in layers:
                    item.setCheckState(0, Qt.Checked)
                    layer = layers[item.layer.name()]
                    item.setValues(layer["visible"], layer["popup"], layer["method"],
                                   layer["clusterDistance"], layer["clusterColor"],
                                   layer["allowSelection"],
                                   layer["showInOverview"], layer["timeInfo"],
                                   layer["showInControls"], layer["singleTile"])
                else:
                    item.setCheckState(0, Qt.Unchecked)

                deploy = appdef["Deploy"]

                self.postgisHostBox.setText(deploy["PostGIS host"])
                self.postgisPortBox.setText(deploy["PostGIS port"])
                self.postgisDatabaseBox.setText(deploy["PostGIS database"])
                self.postgisSchemaBox.setText(deploy["PostGIS schema"])
                self.postgisUsernameBox.setText(deploy["PostGIS username"])
                self.postgisPasswordBox.setText(deploy["PostGIS password"])
                self.geoserverUrlBox.setText(deploy["GeoServer url"])
                self.geoserverUsernameBox.setText(deploy["GeoServer username"])
                self.geoserverPasswordBox.setText(deploy["GeoServer password"])
                self.geoserverWorkspaceBox.setText(deploy["GeoServer workspace"])
        except Exception, e:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.WARNING)
            QMessageBox.warning(iface.mainWindow(), "Error loading app definition",
                "App definition could not be loaded.\nCheck QGIS log for more details")

    def deployCheckChanged(self):
        self.updateDeployGroups()

    buttonStyle = '''QToolButton {background-color: #7c899f;
                                     border-color: #7c899f;
                                     border-style: solid;
                                     border-width: 3px;
                                     border-radius: 10px;
                                     font: bold 11px;
                                     padding: 15px;
                                     max-width: 220px;
                                     color: white;
                                 }
                                 QToolButton:checked {
                                     background-color: #2d67c6;
                                     border-color:#4d8ef7;
                                 }'''

    def populateWidgets(self):
        def _mousePressEvent(selfb, event):
            QToolButton.mousePressEvent(selfb, event)
            if event.button() == Qt.RightButton:
                menu = QMenu()
                paramsAction = QAction("Configure...", None)
                paramsAction.triggered.connect(selfb.webAppWidget.configure)
                paramsAction.setEnabled(bool(selfb.webAppWidget.parameters()))
                menu.addAction(paramsAction)
                point = selfb.mapToGlobal(event.pos())
                menu.exec_(point)

        for i, (_, w) in enumerate(sorted(webAppWidgets.items())):
            button = QToolButton(self.scrollAreaWidgetContents)
            sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
            button.setSizePolicy(sizePolicy)
            button.setMaximumSize(QSize(110, 110))
            button.setFixedWidth(110)
            button.setFixedHeight(110)
            button.setStyleSheet(self.buttonStyle)
            button.setIcon(w.icon())
            button.setText(w.description().replace(" ", "\n"))
            button.setIconSize(QSize(32, 32))
            button.setCheckable(True)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.webAppWidget = w
            row = i / 5
            col = i % 5
            self.gridLayoutWidgets.addWidget(button, row, col, 1, 1)
            button.mousePressEvent = MethodType(_mousePressEvent, button, QToolButton)
            self.widgetButtons[button] = w.name()
        spacerItem3 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayoutWidgets.addItem(spacerItem3, row + 1, 0, 1, 1)

    def populateThemes(self):
        self.themesButtons = {}
        basePath = os.path.join(os.path.dirname(__file__), "themes")
        themes = [o for o in os.listdir(basePath) if os.path.isdir(os.path.join(basePath,o))]
        for i, theme in enumerate(themes):
            button = QToolButton()
            icon = QIcon(os.path.join(os.path.dirname(__file__), "themes", theme, "icon.png"))
            button.setIcon(icon)
            button.setText(theme)
            button.setIconSize(QSize(80, 80))
            button.setCheckable(True)
            button.setChecked(i == 0)
            button.setFixedWidth(250)
            button.setFixedHeight(150)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet(self.buttonStyle)
            def clicked(button):
                for b in self.themesButtons:
                    b.setChecked(False)
                button.setChecked(True)
            button.clicked.connect(partial(clicked, button))
            row = i / 2
            col = i % 2
            self.gridLayoutThemes.addWidget(button, row, col, 1, 1)
            self.themesButtons[button] = theme

    def populateBaseLayers(self):
        self.baseLayers = {}
        layers = sorted([lay for lay in settings.baseLayers.keys()])
        for i, layer in enumerate(layers):
            button = QToolButton()
            filename = os.path.join(os.path.dirname(__file__), "baselayers", layer.lower().replace(" ", "") + ".png")
            icon = QIcon(filename)
            button.setIcon(icon)
            button.setText(layer)
            button.setIconSize(QSize(160, 80))
            button.setCheckable(True)
            button.setChecked(False)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet(self.buttonStyle)
            row = i / 3
            col = i % 3
            self.gridLayoutBaseLayers.addWidget(button, row, col, 1, 1)
            self.baseLayers[button] = layer
        layers = sorted([lay for lay in settings.baseOverlays.keys()])
        self.baseOverlays = {}
        for i, layer in enumerate(layers):
            button = QToolButton()
            filename = os.path.join(os.path.dirname(__file__), "baselayers", layer.lower().replace(" ", "") + ".png")
            icon = QIcon(filename)
            button.setIcon(icon)
            button.setText(layer)
            button.setIconSize(QSize(160, 80))
            button.setCheckable(True)
            button.setChecked(False)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet(self.buttonStyle)
            row = i / 3
            col = i % 3
            self.gridLayoutBaseOverlays.addWidget(button, row, col, 1, 1)
            self.baseOverlays[button] = layer


    def populateLayers(self):
        skipType = [2]
        visibleLayers = iface.mapCanvas().layers()
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
                    item.setCheckState(0, Qt.Checked if layer in visibleLayers else Qt.Unchecked)
                    item.toggleChildren()
                    self.layersTree.addTopLevelItem(item)

        self.layersTree.expandAll()
        self.layersTree.resizeColumnToContents(0)
        self.layersTree.resizeColumnToContents(1)

        def toggleLayerItemChildren(item, _):
            if isinstance(item, TreeLayerItem):
                item.toggleChildren()
        self.layersTree.itemChanged.connect(toggleLayerItemChildren)
        self.collapseLayers()

    def populateConfigParams(self):
        self.settingsItems = defaultdict(dict)
        item = QTreeWidgetItem()
        item.setText(0, "Settings")
        for param, value in settings.appSettings.iteritems():
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
            return f()
        finally:
            self.progressBar.setVisible(False)
            self.progressLabel.setVisible(False)
            QApplication.restoreOverrideCursor()



    def createApp(self):
        try:
            appdef = self.createAppDefinition()
            problems = checkAppCanBeCreated(appdef)
            if problems:
                dlg = AppDefProblemsDialog(problems)
                dlg.exec_()
                if not dlg.ok:
                    return
            projFile = QgsProject.instance().fileName()
            previousFolder = outputFolders.get(projFile, "")
            folder = QFileDialog.getExistingDirectory(self, "Select folder to store app", previousFolder)
            if folder:
                self._run(lambda: createApp(appdef, not self.checkBoxDeployData.isChecked(), folder, self.progress))
                outputFolders[projFile] = folder
                QMessageBox().information(self, "Web App Builder", "App has been correctly created")
        except WrongValueException:
            pass
        except:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.CRITICAL)
            QMessageBox.critical(iface.mainWindow(), "Error creating web app",
                                 "Could not create web app.\nCheck the QGIS log for more details.")


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
        appdef["Deploy"] = self.getDeployConfiguration(layers)
        if appdef["Deploy"]["GeoServer workspace"] == "":
            appdef["Deploy"]["GeoServer workspace"] = utils.safeName(appdef["Settings"]["Title"])
        if appdef["Deploy"]["PostGIS schema"] == "":
            appdef["Deploy"]["PostGIS schema"] = utils.safeName(appdef["Settings"]["Title"])

        return appdef

    def getBaseLayers(self):
        layers = []
        for b in self.baseLayers:
            if b.isChecked():
                layers.append(self.baseLayers[b])
        for b in self.baseOverlays:
            if b.isChecked():
                layers.append(self.baseOverlays[b])
        return layers

    def getWidgets(self):
        widgets = {}
        for button, name in self.widgetButtons.iteritems():
            if button.isChecked():
                widgets[name] = button.webAppWidget
        return widgets

    def _getValue(self, textbox, mandatory):
        textbox.setStyleSheet("QLineEdit{background: white}")
        value = textbox.text().strip()
        if value == "" and mandatory:
            textbox.setStyleSheet("QLineEdit{background: yellow}")
            raise WrongValueException()
        return value

    def getDeployConfiguration(self, layers):
        postGisMethods = [utils.METHOD_WMS_POSTGIS, utils.METHOD_WFS_POSTGIS]
        geoServerMethods = [utils.METHOD_WMS_POSTGIS, utils.METHOD_WFS_POSTGIS,
                           utils.METHOD_WMS, utils.METHOD_WFS]
        usesGeoServer = False
        usesPostGis = False
        layers, _ = self.getLayersAndGroups()
        for layer in layers:
            if layer.method in geoServerMethods:
                usesGeoServer = True
                if layer.method in postGisMethods:
                    usesPostGis = True

        deploy = not self.checkBoxDeployData.isChecked()
        usesPostGis = usesPostGis and deploy
        try:
            params = {
                "PostGIS host": self._getValue(self.postgisHostBox, usesPostGis),
                "PostGIS port": self._getValue(self.postgisPortBox, usesPostGis),
                "PostGIS database": self._getValue(self.postgisDatabaseBox, usesPostGis),
                "PostGIS schema": self.postgisSchemaBox.text().strip(),
                "PostGIS username": self._getValue(self.postgisUsernameBox, usesPostGis),
                "PostGIS password": self._getValue(self.postgisPasswordBox, usesPostGis),
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
        for b in self.themesButtons:
            if b.isChecked():
                themeName = b.text()
                break
        logo = self.logoBox.text().strip()
        if logo and not os.path.exists(logo):
            self.tabPanel.setCurrentIndex(0)
            self.logoBox.setStyleSheet("QLineEdit{background: yellow}")
            raise WrongValueException()
        self.logoBox.setStyleSheet("QLineEdit{background: white}")
        parameters = {"Title": title,
                      "Logo": logo,
                      "Theme": themeName
                      }
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
            elif isinstance(item, TreeGroupItem):
                groupLayers = []
                for j in xrange(item.childCount()):
                    subitem = item.child(j)
                    if isinstance(subitem, TreeLayerItem) and subitem.checkState(0) == Qt.Checked:
                        layers.append(subitem.appLayer())
                        groupLayers.append(subitem.layer)
                if groupLayers:
                    groups[item.name] = {"showContent": item.showContent(),
                                         "layers": groupLayers[::-1]}

        return layers[::-1], groups



