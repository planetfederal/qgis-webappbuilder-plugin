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
from appcreator import createApp, WrongAppDefinitionException,\
    AppDefProblemsDialog, loadAppdef, saveAppdef
import settings
from types import MethodType
import webbrowser
from parameditor import ParametersEditorDialog
from treesettingsitem import TreeSettingItem
from utils import METHOD_WMS, METHOD_WMS_POSTGIS
from themeeditor import ThemeEditorDialog
from functools import partial
from texteditor import TextEditorDialog, HTML
from bookmarkseditor import BookmarksEditorDialog
from charttooldialog import ChartToolDialog
from settings import WrongValueException, outputFolders
from linksdialog import LinksDialog
from popupeditor import PopupEditorDialog
import traceback


class Layer():

    def __init__(self, layer, visible, popup, method, clusterDistance, allowSelection):
        self.layer = layer
        self.visible = visible
        self.popup = popup
        self.method = method
        self.clusterDistance = clusterDistance
        self.allowSelection = allowSelection

groupIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "group.gif"))
layerIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer.png"))
pointIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_point.png"))
lineIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_line.png"))
polygonIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_polygon.png"))
rasterIcon = QIcon(os.path.join(os.path.dirname(__file__), "icons", "layer_raster.jpg"))

class MainDialog(QDialog, Ui_MainDialog):

    items = {}


    def __init__(self, appdef):
        QDialog.__init__(self)
        self.setupUi(self)
        self.populateLayers()
        self.populateBaseLayers()
        self.populateConfigParams()
        self.populateThemes()
        self.buttonLogo.clicked.connect(self.selectLogo)
        self.buttonConfigureTheme.clicked.connect(self.configureTheme)
        self.buttonPreview.clicked.connect(self.updatePreview)
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
        widgetButtons = {self.attributesTableButton: "Attributes table",
                        self.attributionButton: "Attribution",
                        self.fullScreenButton: "Full screen",
                        self.layersListButton: "Layers list",
                        self.mousePositionButton: "Mouse position",
                        self.northArrowButton: "North arrow",
                        self.overviewButton: "Overview map",
                        self.scaleBarButton: "Scale bar",
                        self.zoomControlsButton: "Zoom controls",
                        self.zoomSliderButton: "Zoom slider",
                        self.homeButton: "Home button",
                        self.cesiumButton: "3D view",
                        self.aboutPanelButton: "About panel",
                        self.exportAsImageButton: "Export as image",
                        self.geolocationButton: "Geolocation",
                        self.measureToolButton: "Measure tool",
                        self.geocodingButton: "Geocoding",
                        self.chartToolButton: "Chart tool",
                        self.linksButton: "Links",
                        self.helpButton: "Help",
                        self.bookmarksButton: "Bookmarks",
                        self.queryButton: "Query",
                        self.selectionToolsButton: "Selection tools"}

        def _mousePressEvent(selfb, event):
            QToolButton.mousePressEvent(selfb, event)
            if event.button() == Qt.RightButton :
                name = widgetButtons[selfb]
                menu = QMenu()
                paramsAction = QAction("Configure...", None)
                paramsAction.triggered.connect(lambda: self.editWidgetParameters(name))
                paramsAction.setEnabled(name in settings.widgetsParams)
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

    def configureTheme(self):
        dlg = ThemeEditorDialog()
        dlg.exec_()

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
                    for paramName, value in appdef["Widgets"][widgetName].iteritems():
                        if isinstance(value, tuple):
                            settings.widgetsParams[widgetName][paramName][0] = value
                        else:
                            settings.widgetsParams[widgetName][paramName] = value
            for name in self.settingsItems:
                if name in appdef["Settings"]:
                    self.settingsItems[name].setValue(appdef["Settings"][name])
            theme = appdef["Settings"]["Theme"]["Name"]
            for button, themeName in self.themesButtons.iteritems():
                if themeName == theme:
                    button.click()
            baseLayers = appdef["Base layers"]
            for button, name in self.baseLayers.iteritems():
                button.setChecked(name in baseLayers)
            for button, name in self.baseOverlays.iteritems():
                button.setChecked(name in baseLayers)
            settings.currentCss = appdef["Settings"]["Theme"]["Css"]
            items = []
            for i in xrange(self.layersTree.topLevelItemCount()):
                item = self.layersTree.topLevelItem(i)
                if isinstance(item, TreeLayerItem):
                    items.append(item)
                else:
                    for j in xrange(item.childCount()):
                        subitem = item.child(j)
                        items.append(subitem)
            layers = {lay["layer"]: lay for lay in appdef["Layers"]}
            for item in items:
                if item.layer.name() in layers:
                    item.setCheckState(0, Qt.Checked)
                    layer = layers[item.layer.name()]
                    item.setValues(layer["visible"], layer["popup"], layer["method"],
                                   layer["clusterDistance"], layer["allowSelection"])
                else:
                    item.setCheckState(0, Qt.Unchecked)
        except Exception, e:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.WARNING)
            QMessageBox.warning(iface.mainWindow(), "Error loading app definition",
                "App definition could not be loaded.\nCheck QGIS log for more details")

    def deployCheckChanged(self):
        self.updateDeployGroups()

    def editWidgetParameters(self, widgetName):
        if widgetName == "Text panel":
            dlg = TextEditorDialog(settings.widgetsParams[widgetName]["HTML content"], HTML)
            dlg.exec_()
            settings.widgetsParams[widgetName]["HTML content"] = dlg.text
        elif widgetName == "Links":
            dlg = LinksDialog(settings.widgetsParams[widgetName]["links"], self)
            dlg.exec_()
            if dlg.ok:
                settings.widgetsParams[widgetName]["links"] = dlg.links
        elif widgetName == "Bookmarks":
            dlg = BookmarksEditorDialog(self, settings.widgetsParams[widgetName]["bookmarks"],
                                        settings.widgetsParams[widgetName]["format"],
                                        settings.widgetsParams[widgetName]["interval"],
                                        settings.widgetsParams[widgetName]["introTitle"],
                                        settings.widgetsParams[widgetName]["introText"],
                                        settings.widgetsParams[widgetName]["showIndicators"])
            dlg.exec_()
            if dlg.bookmarks:
                settings.widgetsParams[widgetName]["bookmarks"] = dlg.bookmarks
                settings.widgetsParams[widgetName]["format"] = dlg.format
                settings.widgetsParams[widgetName]["interval"] = dlg.interval
                settings.widgetsParams[widgetName]["introTitle"] = dlg.introTitle
                settings.widgetsParams[widgetName]["introText"] = dlg.introText
                settings.widgetsParams[widgetName]["showIndicators"] = dlg.showIndicators

        elif widgetName == "Chart tool":
            dlg = ChartToolDialog(settings.widgetsParams[widgetName]["charts"], self)
            dlg.exec_()
            settings.widgetsParams[widgetName]["charts"] = dlg.charts
        else:
            dlg = ParametersEditorDialog(settings.widgetsParams[widgetName])
            dlg.exec_()
            settings.widgetsParams[widgetName] = dlg.params

    buttonStyle = '''QToolButton {
                background-color: #bbbbbb; border-style: outset; border-width: 2px;
                border-radius: 10px; border-color: beige; font: bold;
                min-width: 100px; max-width: 250px; padding:10px;}
                QToolButton:checked { background-color: #9ABEED; border-style: inset;}'''

    def populateThemes(self):
        self.themesButtons = {}
        themes = [k for k in settings.themes.keys() if k != "basic"]
        if "basic" in settings.themes:
            themes.insert(0, "basic")
        for i, theme in enumerate(themes):
            button = QToolButton()
            icon = QIcon(os.path.join(os.path.dirname(__file__), "themes", theme, theme + ".png"))
            button.setIcon(icon)
            button.setText(theme)
            button.setIconSize(QSize(80, 80))
            button.setCheckable(True)
            button.setChecked(i == 0)
            button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            button.setStyleSheet(self.buttonStyle)
            def clicked(button):
                for b in self.themesButtons:
                    b.setChecked(False)
                button.setChecked(True)
                settings.currentTheme = button.text()
                settings.currentCss = settings.themes[button.text()]

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

    def updatePreview(self):
        try:
            appdef = self.createAppDefinition(True)
            path = self._run(lambda: writeOL(appdef, utils.tempFolder(), True, self.progress))
            path = "file:///" + path.replace("\\","/")
            webbrowser.open_new(path)
        except WrongValueException:
            pass
        except WrongAppDefinitionException, e:
            dlg = AppDefProblemsDialog(unicode(e))
            dlg.exec_()
        except:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.CRITICAL)
            QMessageBox.critical(iface.mainWindow(), "Error creating web app",
                                 "Could not create web app.\nSee QGIS log for more details.")

    def createApp(self):
        try:
            projFile = QgsProject.instance().fileName()
            previousFolder = outputFolders.get(projFile, "")
            folder = QFileDialog.getExistingDirectory(self, "Select folder to store app", previousFolder)
            if folder:
                appdef = self.createAppDefinition()
                self._run(lambda: createApp(appdef, not self.checkBoxDeployData.isChecked(), folder, self.progress))
                outputFolders[projFile] = folder
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
        except WrongAppDefinitionException, e:
            dlg = AppDefProblemsDialog(unicode(e))
            dlg.exec_()
        except:
            QgsMessageLog.logMessage(traceback.format_exc(), level=QgsMessageLog.CRITICAL)
            QMessageBox.critical(iface.mainWindow(), "Error creating web app",
                                 "Could not create web app.\nSee QGIS log for more details.")


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
                params = settings.widgetsParams.get(name, {}).copy()
                for k, v, in params.iteritems():
                    if isinstance(v, tuple):
                        params[k] = v[0]
                widgets[name] = params
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
                      "Theme": {"Name": themeName,
                                "Css": settings.currentCss}
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
            else:
                groupLayers = []
                for j in xrange(item.childCount()):
                    subitem = item.child(j)
                    if subitem.checkState(0) == Qt.Checked:
                        layers.append(subitem.appLayer())
                        groupLayers.append(subitem.layer)
                if groupLayers:
                    groups[item.name] = groupLayers[::-1]

        return layers[::-1], groups


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
                item = TreeLayerItem(layer, layersTree)
                item.setCheckState(0, Qt.Checked if layer in visibleLayers else Qt.Unchecked)
                item.toggleChildren()
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
            self.popupLabel = QLabel()
            self.popupLabel.setText("<a href='#'>Edit</a>")
            tree.setItemWidget(self.popupItem, 1, self.popupLabel)
            def edit():
                dlg = PopupEditorDialog(self.popup, [f.name() for f in self.layer.pendingFields()])
                dlg.exec_()
                self.popup = dlg.text.strip()
            self.popupLabel.connect(self.popupLabel, SIGNAL("linkActivated(QString)"), edit)
            self.addChild(self.popupItem)
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

    def setValues(self, visible, popup, method, clusterDistance, allowSelection):
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
            self.allowSelectionItem.setCheckState(0, Qt.Checked if allowSelection else Qt.Unchecked)
        except:
            pass
        self.visibleItem.setCheckState(0, Qt.Checked if visible else Qt.Unchecked)
        try:
            self.connTypeCombo.setCurrentIndex(method)
        except:
            pass
        self.popup = popup

    def appLayer(self):
        return Layer(self.layer, self.visible, self.popup, self.method, self.clusterDistance, self.allowSelection)


