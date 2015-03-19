# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_maindialog.ui'
#
# Created: Tue Mar 17 15:01:01 2015
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainDialog(object):
    def setupUi(self, MainDialog):
        MainDialog.setObjectName(_fromUtf8("MainDialog"))
        MainDialog.resize(654, 771)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/ol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.tabPanel = QtGui.QTabWidget(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabPanel.sizePolicy().hasHeightForWidth())
        self.tabPanel.setSizePolicy(sizePolicy)
        self.tabPanel.setTabPosition(QtGui.QTabWidget.West)
        self.tabPanel.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabPanel.setElideMode(QtCore.Qt.ElideRight)
        self.tabPanel.setUsesScrollButtons(True)
        self.tabPanel.setDocumentMode(False)
        self.tabPanel.setTabsClosable(False)
        self.tabPanel.setObjectName(_fromUtf8("tabPanel"))
        self.descriptionTab = QtGui.QWidget()
        self.descriptionTab.setObjectName(_fromUtf8("descriptionTab"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.descriptionTab)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.label_3 = QtGui.QLabel(self.descriptionTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_10.addWidget(self.label_3)
        self.titleBox = QtGui.QLineEdit(self.descriptionTab)
        self.titleBox.setObjectName(_fromUtf8("titleBox"))
        self.verticalLayout_10.addWidget(self.titleBox)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_10.addItem(spacerItem)
        self.groupHeader = QtGui.QGroupBox(self.descriptionTab)
        self.groupHeader.setFlat(True)
        self.groupHeader.setCheckable(True)
        self.groupHeader.setObjectName(_fromUtf8("groupHeader"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupHeader)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_16 = QtGui.QLabel(self.groupHeader)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_4.addWidget(self.label_16)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.imgFilepathBox = QtGui.QLineEdit(self.groupHeader)
        self.imgFilepathBox.setText(_fromUtf8(""))
        self.imgFilepathBox.setObjectName(_fromUtf8("imgFilepathBox"))
        self.horizontalLayout_3.addWidget(self.imgFilepathBox)
        self.buttonSelectImgFilepath = QtGui.QToolButton(self.groupHeader)
        self.buttonSelectImgFilepath.setObjectName(_fromUtf8("buttonSelectImgFilepath"))
        self.horizontalLayout_3.addWidget(self.buttonSelectImgFilepath)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.groupHeader)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.labelEditHeaderCss = QtGui.QLabel(self.groupHeader)
        self.labelEditHeaderCss.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelEditHeaderCss.setObjectName(_fromUtf8("labelEditHeaderCss"))
        self.horizontalLayout_6.addWidget(self.labelEditHeaderCss)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.headerTextBox = QtGui.QPlainTextEdit(self.groupHeader)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerTextBox.sizePolicy().hasHeightForWidth())
        self.headerTextBox.setSizePolicy(sizePolicy)
        self.headerTextBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.headerTextBox.setObjectName(_fromUtf8("headerTextBox"))
        self.verticalLayout_4.addWidget(self.headerTextBox)
        self.verticalLayout_10.addWidget(self.groupHeader)
        self.groupFooter = QtGui.QGroupBox(self.descriptionTab)
        self.groupFooter.setFlat(True)
        self.groupFooter.setCheckable(True)
        self.groupFooter.setObjectName(_fromUtf8("groupFooter"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupFooter)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.label_18 = QtGui.QLabel(self.groupFooter)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_7.addWidget(self.label_18)
        self.labelEditFooterCss = QtGui.QLabel(self.groupFooter)
        self.labelEditFooterCss.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelEditFooterCss.setObjectName(_fromUtf8("labelEditFooterCss"))
        self.horizontalLayout_7.addWidget(self.labelEditFooterCss)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.footerTextBox = QtGui.QPlainTextEdit(self.groupFooter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footerTextBox.sizePolicy().hasHeightForWidth())
        self.footerTextBox.setSizePolicy(sizePolicy)
        self.footerTextBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.footerTextBox.setObjectName(_fromUtf8("footerTextBox"))
        self.verticalLayout_9.addWidget(self.footerTextBox)
        self.verticalLayout_10.addWidget(self.groupFooter)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_10.addItem(spacerItem1)
        self.tabPanel.addTab(self.descriptionTab, _fromUtf8(""))
        self.baseLayerTab = QtGui.QWidget()
        self.baseLayerTab.setObjectName(_fromUtf8("baseLayerTab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.baseLayerTab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.mapQuestAerialButton = QtGui.QToolButton(self.baseLayerTab)
        self.mapQuestAerialButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold;\n"
"     min-width: 100px;\n"
"     max-width: 250px;\n"
"    padding:10px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/mapquestaerial.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mapQuestAerialButton.setIcon(icon1)
        self.mapQuestAerialButton.setIconSize(QtCore.QSize(250, 100))
        self.mapQuestAerialButton.setCheckable(True)
        self.mapQuestAerialButton.setChecked(True)
        self.mapQuestAerialButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mapQuestAerialButton.setObjectName(_fromUtf8("mapQuestAerialButton"))
        self.gridLayout_4.addWidget(self.mapQuestAerialButton, 0, 0, 1, 1)
        self.mapQuestButton = QtGui.QToolButton(self.baseLayerTab)
        self.mapQuestButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold;\n"
"     min-width: 100px;\n"
"     max-width: 250px;\n"
"     padding: 10px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/mapquest.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mapQuestButton.setIcon(icon2)
        self.mapQuestButton.setIconSize(QtCore.QSize(250, 100))
        self.mapQuestButton.setCheckable(True)
        self.mapQuestButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mapQuestButton.setObjectName(_fromUtf8("mapQuestButton"))
        self.gridLayout_4.addWidget(self.mapQuestButton, 0, 1, 1, 1)
        self.stamenWatercolorButton = QtGui.QToolButton(self.baseLayerTab)
        self.stamenWatercolorButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold;\n"
"     min-width: 100px;\n"
"     max-width: 250px;\n"
"     padding: 10px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/watercolor.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stamenWatercolorButton.setIcon(icon3)
        self.stamenWatercolorButton.setIconSize(QtCore.QSize(250, 100))
        self.stamenWatercolorButton.setCheckable(True)
        self.stamenWatercolorButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.stamenWatercolorButton.setObjectName(_fromUtf8("stamenWatercolorButton"))
        self.gridLayout_4.addWidget(self.stamenWatercolorButton, 1, 0, 1, 1)
        self.stamenTonerButton = QtGui.QToolButton(self.baseLayerTab)
        self.stamenTonerButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold;\n"
"     min-width: 100px;\n"
"     max-width: 250px;\n"
"     padding: 10px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/toner.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stamenTonerButton.setIcon(icon4)
        self.stamenTonerButton.setIconSize(QtCore.QSize(250, 100))
        self.stamenTonerButton.setCheckable(True)
        self.stamenTonerButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.stamenTonerButton.setObjectName(_fromUtf8("stamenTonerButton"))
        self.gridLayout_4.addWidget(self.stamenTonerButton, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem2, 3, 0, 1, 1)
        self.osmButton = QtGui.QToolButton(self.baseLayerTab)
        self.osmButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold;\n"
"     min-width: 100px;\n"
"     max-width: 250px;\n"
"    padding:10px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/osm.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.osmButton.setIcon(icon5)
        self.osmButton.setIconSize(QtCore.QSize(250, 100))
        self.osmButton.setCheckable(True)
        self.osmButton.setChecked(False)
        self.osmButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.osmButton.setObjectName(_fromUtf8("osmButton"))
        self.gridLayout_4.addWidget(self.osmButton, 2, 0, 1, 1)
        self.tabPanel.addTab(self.baseLayerTab, _fromUtf8(""))
        self.layersTab = QtGui.QWidget()
        self.layersTab.setObjectName(_fromUtf8("layersTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layersTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.layersTree = QtGui.QTreeWidget(self.layersTab)
        self.layersTree.setMinimumSize(QtCore.QSize(400, 300))
        self.layersTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.layersTree.setObjectName(_fromUtf8("layersTree"))
        self.layersTree.headerItem().setText(0, _fromUtf8("1"))
        self.layersTree.header().setVisible(False)
        self.layersTree.header().setDefaultSectionSize(200)
        self.verticalLayout_3.addWidget(self.layersTree)
        self.tabPanel.addTab(self.layersTab, _fromUtf8(""))
        self.widgetsTab = QtGui.QWidget()
        self.widgetsTab.setObjectName(_fromUtf8("widgetsTab"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widgetsTab)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.widgetsTab)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 2)
        self.scaleBarButton = QtGui.QToolButton(self.widgetsTab)
        self.scaleBarButton.setMinimumSize(QtCore.QSize(134, 100))
        self.scaleBarButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/puzzle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scaleBarButton.setIcon(icon6)
        self.scaleBarButton.setIconSize(QtCore.QSize(32, 32))
        self.scaleBarButton.setCheckable(True)
        self.scaleBarButton.setChecked(True)
        self.scaleBarButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.scaleBarButton.setObjectName(_fromUtf8("scaleBarButton"))
        self.gridLayout_3.addWidget(self.scaleBarButton, 1, 0, 1, 1)
        self.zoomControlsButton = QtGui.QToolButton(self.widgetsTab)
        self.zoomControlsButton.setMinimumSize(QtCore.QSize(134, 100))
        self.zoomControlsButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.zoomControlsButton.setIcon(icon6)
        self.zoomControlsButton.setIconSize(QtCore.QSize(32, 32))
        self.zoomControlsButton.setCheckable(True)
        self.zoomControlsButton.setChecked(True)
        self.zoomControlsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoomControlsButton.setAutoRaise(False)
        self.zoomControlsButton.setArrowType(QtCore.Qt.NoArrow)
        self.zoomControlsButton.setObjectName(_fromUtf8("zoomControlsButton"))
        self.gridLayout_3.addWidget(self.zoomControlsButton, 1, 1, 1, 1)
        self.layersListButton = QtGui.QToolButton(self.widgetsTab)
        self.layersListButton.setMinimumSize(QtCore.QSize(134, 100))
        self.layersListButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.layersListButton.setIcon(icon6)
        self.layersListButton.setIconSize(QtCore.QSize(32, 32))
        self.layersListButton.setCheckable(True)
        self.layersListButton.setChecked(True)
        self.layersListButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.layersListButton.setObjectName(_fromUtf8("layersListButton"))
        self.gridLayout_3.addWidget(self.layersListButton, 1, 2, 1, 1)
        self.overviewButton = QtGui.QToolButton(self.widgetsTab)
        self.overviewButton.setMinimumSize(QtCore.QSize(134, 100))
        self.overviewButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.overviewButton.setIcon(icon6)
        self.overviewButton.setIconSize(QtCore.QSize(32, 32))
        self.overviewButton.setCheckable(True)
        self.overviewButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.overviewButton.setObjectName(_fromUtf8("overviewButton"))
        self.gridLayout_3.addWidget(self.overviewButton, 2, 0, 1, 1)
        self.fullScreenButton = QtGui.QToolButton(self.widgetsTab)
        self.fullScreenButton.setMinimumSize(QtCore.QSize(134, 100))
        self.fullScreenButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.fullScreenButton.setIcon(icon6)
        self.fullScreenButton.setIconSize(QtCore.QSize(32, 32))
        self.fullScreenButton.setCheckable(True)
        self.fullScreenButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.fullScreenButton.setObjectName(_fromUtf8("fullScreenButton"))
        self.gridLayout_3.addWidget(self.fullScreenButton, 2, 1, 1, 1)
        self.attributionButton = QtGui.QToolButton(self.widgetsTab)
        self.attributionButton.setMinimumSize(QtCore.QSize(134, 100))
        self.attributionButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.attributionButton.setIcon(icon6)
        self.attributionButton.setIconSize(QtCore.QSize(32, 32))
        self.attributionButton.setCheckable(True)
        self.attributionButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.attributionButton.setObjectName(_fromUtf8("attributionButton"))
        self.gridLayout_3.addWidget(self.attributionButton, 2, 2, 1, 1)
        self.northArrowButton = QtGui.QToolButton(self.widgetsTab)
        self.northArrowButton.setMinimumSize(QtCore.QSize(134, 100))
        self.northArrowButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.northArrowButton.setIcon(icon6)
        self.northArrowButton.setIconSize(QtCore.QSize(32, 32))
        self.northArrowButton.setCheckable(True)
        self.northArrowButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.northArrowButton.setObjectName(_fromUtf8("northArrowButton"))
        self.gridLayout_3.addWidget(self.northArrowButton, 3, 0, 1, 1)
        self.zoomToExtentButton = QtGui.QToolButton(self.widgetsTab)
        self.zoomToExtentButton.setMinimumSize(QtCore.QSize(134, 100))
        self.zoomToExtentButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.zoomToExtentButton.setIcon(icon6)
        self.zoomToExtentButton.setIconSize(QtCore.QSize(32, 32))
        self.zoomToExtentButton.setCheckable(True)
        self.zoomToExtentButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoomToExtentButton.setObjectName(_fromUtf8("zoomToExtentButton"))
        self.gridLayout_3.addWidget(self.zoomToExtentButton, 3, 1, 1, 1)
        self.zoomSliderButton = QtGui.QToolButton(self.widgetsTab)
        self.zoomSliderButton.setMinimumSize(QtCore.QSize(134, 100))
        self.zoomSliderButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.zoomSliderButton.setIcon(icon6)
        self.zoomSliderButton.setIconSize(QtCore.QSize(32, 32))
        self.zoomSliderButton.setCheckable(True)
        self.zoomSliderButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoomSliderButton.setObjectName(_fromUtf8("zoomSliderButton"))
        self.gridLayout_3.addWidget(self.zoomSliderButton, 3, 2, 1, 1)
        self.exportAsImageButton = QtGui.QToolButton(self.widgetsTab)
        self.exportAsImageButton.setMinimumSize(QtCore.QSize(134, 100))
        self.exportAsImageButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.exportAsImageButton.setIcon(icon6)
        self.exportAsImageButton.setIconSize(QtCore.QSize(32, 32))
        self.exportAsImageButton.setCheckable(True)
        self.exportAsImageButton.setChecked(False)
        self.exportAsImageButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.exportAsImageButton.setObjectName(_fromUtf8("exportAsImageButton"))
        self.gridLayout_3.addWidget(self.exportAsImageButton, 4, 0, 1, 1)
        self.mousePositionButton = QtGui.QToolButton(self.widgetsTab)
        self.mousePositionButton.setMinimumSize(QtCore.QSize(134, 100))
        self.mousePositionButton.setMaximumSize(QtCore.QSize(100, 100))
        self.mousePositionButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.mousePositionButton.setIcon(icon6)
        self.mousePositionButton.setIconSize(QtCore.QSize(32, 32))
        self.mousePositionButton.setCheckable(True)
        self.mousePositionButton.setAutoRepeat(False)
        self.mousePositionButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mousePositionButton.setObjectName(_fromUtf8("mousePositionButton"))
        self.gridLayout_3.addWidget(self.mousePositionButton, 4, 1, 1, 1)
        self.textPanelButton = QtGui.QToolButton(self.widgetsTab)
        self.textPanelButton.setMinimumSize(QtCore.QSize(134, 100))
        self.textPanelButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.textPanelButton.setIcon(icon6)
        self.textPanelButton.setIconSize(QtCore.QSize(32, 32))
        self.textPanelButton.setCheckable(True)
        self.textPanelButton.setChecked(False)
        self.textPanelButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.textPanelButton.setObjectName(_fromUtf8("textPanelButton"))
        self.gridLayout_3.addWidget(self.textPanelButton, 4, 2, 1, 1)
        self.cesiumButton = QtGui.QToolButton(self.widgetsTab)
        self.cesiumButton.setMinimumSize(QtCore.QSize(134, 100))
        self.cesiumButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.cesiumButton.setIcon(icon6)
        self.cesiumButton.setIconSize(QtCore.QSize(32, 32))
        self.cesiumButton.setCheckable(True)
        self.cesiumButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.cesiumButton.setObjectName(_fromUtf8("cesiumButton"))
        self.gridLayout_3.addWidget(self.cesiumButton, 5, 0, 1, 1)
        self.attributesTableButton = QtGui.QToolButton(self.widgetsTab)
        self.attributesTableButton.setMinimumSize(QtCore.QSize(134, 100))
        self.attributesTableButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.attributesTableButton.setIcon(icon6)
        self.attributesTableButton.setIconSize(QtCore.QSize(32, 32))
        self.attributesTableButton.setCheckable(True)
        self.attributesTableButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.attributesTableButton.setObjectName(_fromUtf8("attributesTableButton"))
        self.gridLayout_3.addWidget(self.attributesTableButton, 5, 1, 1, 1)
        self.editToolButton = QtGui.QToolButton(self.widgetsTab)
        self.editToolButton.setMinimumSize(QtCore.QSize(134, 100))
        self.editToolButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.editToolButton.setIcon(icon6)
        self.editToolButton.setIconSize(QtCore.QSize(32, 32))
        self.editToolButton.setCheckable(True)
        self.editToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.editToolButton.setObjectName(_fromUtf8("editToolButton"))
        self.gridLayout_3.addWidget(self.editToolButton, 5, 2, 1, 1)
        self.searchButton = QtGui.QToolButton(self.widgetsTab)
        self.searchButton.setMinimumSize(QtCore.QSize(134, 100))
        self.searchButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.searchButton.setIcon(icon6)
        self.searchButton.setIconSize(QtCore.QSize(32, 32))
        self.searchButton.setCheckable(True)
        self.searchButton.setChecked(False)
        self.searchButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.gridLayout_3.addWidget(self.searchButton, 6, 0, 1, 1)
        self.legendButton = QtGui.QToolButton(self.widgetsTab)
        self.legendButton.setMinimumSize(QtCore.QSize(134, 100))
        self.legendButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #bbbbbb;\n"
"     border-style: outset;\n"
"     border-width: 2px;\n"
"     border-radius: 10px;\n"
"     border-color: beige;\n"
"     font: bold 11px;\n"
"     min-width: 100px;\n"
"     max-widht: 100px;\n"
"     padding: 15px;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #9ABEED;\n"
"     border-style: inset;\n"
" }"))
        self.legendButton.setIcon(icon6)
        self.legendButton.setIconSize(QtCore.QSize(32, 32))
        self.legendButton.setCheckable(True)
        self.legendButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.legendButton.setObjectName(_fromUtf8("legendButton"))
        self.gridLayout_3.addWidget(self.legendButton, 6, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 7, 1, 1, 1)
        self.tabPanel.addTab(self.widgetsTab, _fromUtf8(""))
        self.suiteTab = QtGui.QWidget()
        self.suiteTab.setObjectName(_fromUtf8("suiteTab"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.suiteTab)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.postgisGroupBox = QtGui.QGroupBox(self.suiteTab)
        self.postgisGroupBox.setEnabled(True)
        self.postgisGroupBox.setFlat(True)
        self.postgisGroupBox.setObjectName(_fromUtf8("postgisGroupBox"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.postgisGroupBox)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_8 = QtGui.QLabel(self.postgisGroupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)
        self.postgisHostBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisHostBox.setObjectName(_fromUtf8("postgisHostBox"))
        self.gridLayout_2.addWidget(self.postgisHostBox, 0, 2, 1, 1)
        self.label_10 = QtGui.QLabel(self.postgisGroupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 1, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.postgisGroupBox)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_2.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.postgisGroupBox)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 3, 0, 1, 1)
        self.postgisPortBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisPortBox.setObjectName(_fromUtf8("postgisPortBox"))
        self.gridLayout_2.addWidget(self.postgisPortBox, 1, 2, 1, 1)
        self.postgisSchemaBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisSchemaBox.setText(_fromUtf8(""))
        self.postgisSchemaBox.setObjectName(_fromUtf8("postgisSchemaBox"))
        self.gridLayout_2.addWidget(self.postgisSchemaBox, 3, 2, 1, 1)
        self.postgisDatabaseBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisDatabaseBox.setObjectName(_fromUtf8("postgisDatabaseBox"))
        self.gridLayout_2.addWidget(self.postgisDatabaseBox, 2, 2, 1, 1)
        self.label_13 = QtGui.QLabel(self.postgisGroupBox)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_2.addWidget(self.label_13, 0, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.postgisGroupBox)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_2.addWidget(self.label_14, 2, 0, 1, 1)
        self.postgisUsernameBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisUsernameBox.setObjectName(_fromUtf8("postgisUsernameBox"))
        self.gridLayout_2.addWidget(self.postgisUsernameBox, 4, 2, 1, 1)
        self.postgisPasswordBox = QtGui.QLineEdit(self.postgisGroupBox)
        self.postgisPasswordBox.setEchoMode(QtGui.QLineEdit.Password)
        self.postgisPasswordBox.setObjectName(_fromUtf8("postgisPasswordBox"))
        self.gridLayout_2.addWidget(self.postgisPasswordBox, 5, 2, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_2)
        self.verticalLayout_8.addWidget(self.postgisGroupBox)
        self.geoserverGroupBox = QtGui.QGroupBox(self.suiteTab)
        self.geoserverGroupBox.setFlat(True)
        self.geoserverGroupBox.setObjectName(_fromUtf8("geoserverGroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.geoserverGroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.geoserverUrlBox = QtGui.QLineEdit(self.geoserverGroupBox)
        self.geoserverUrlBox.setObjectName(_fromUtf8("geoserverUrlBox"))
        self.gridLayout.addWidget(self.geoserverUrlBox, 0, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.geoserverGroupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.geoserverPasswordBox = QtGui.QLineEdit(self.geoserverGroupBox)
        self.geoserverPasswordBox.setEchoMode(QtGui.QLineEdit.Password)
        self.geoserverPasswordBox.setObjectName(_fromUtf8("geoserverPasswordBox"))
        self.gridLayout.addWidget(self.geoserverPasswordBox, 2, 2, 1, 1)
        self.geoserverUsernameBox = QtGui.QLineEdit(self.geoserverGroupBox)
        self.geoserverUsernameBox.setObjectName(_fromUtf8("geoserverUsernameBox"))
        self.gridLayout.addWidget(self.geoserverUsernameBox, 1, 2, 1, 1)
        self.label_6 = QtGui.QLabel(self.geoserverGroupBox)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.geoserverGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.geoserverWorkspaceBox = QtGui.QLineEdit(self.geoserverGroupBox)
        self.geoserverWorkspaceBox.setObjectName(_fromUtf8("geoserverWorkspaceBox"))
        self.gridLayout.addWidget(self.geoserverWorkspaceBox, 3, 2, 1, 1)
        self.label_5 = QtGui.QLabel(self.geoserverGroupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_8.addWidget(self.geoserverGroupBox)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_8.addItem(spacerItem4)
        self.groupBox_3 = QtGui.QGroupBox(self.suiteTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tabWidgetDeploy = QtGui.QTabWidget(self.groupBox_3)
        self.tabWidgetDeploy.setObjectName(_fromUtf8("tabWidgetDeploy"))
        self.deployLocalTab = QtGui.QWidget()
        self.deployLocalTab.setObjectName(_fromUtf8("deployLocalTab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.deployLocalTab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_9 = QtGui.QLabel(self.deployLocalTab)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_6.addWidget(self.label_9, 0, 0, 1, 1)
        self.filepathBox = QtGui.QLineEdit(self.deployLocalTab)
        self.filepathBox.setObjectName(_fromUtf8("filepathBox"))
        self.gridLayout_6.addWidget(self.filepathBox, 0, 1, 1, 1)
        self.buttonSelectFilepath = QtGui.QToolButton(self.deployLocalTab)
        self.buttonSelectFilepath.setObjectName(_fromUtf8("buttonSelectFilepath"))
        self.gridLayout_6.addWidget(self.buttonSelectFilepath, 0, 2, 1, 1)
        self.tabWidgetDeploy.addTab(self.deployLocalTab, _fromUtf8(""))
        self.deployRemoteTab = QtGui.QWidget()
        self.deployRemoteTab.setObjectName(_fromUtf8("deployRemoteTab"))
        self.tabWidgetDeploy.addTab(self.deployRemoteTab, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.tabWidgetDeploy, 0, 0, 1, 1)
        self.verticalLayout_8.addWidget(self.groupBox_3)
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem5)
        self.tabPanel.addTab(self.suiteTab, _fromUtf8(""))
        self.settingsTab = QtGui.QWidget()
        self.settingsTab.setObjectName(_fromUtf8("settingsTab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.settingsTab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.settingsTree = QtGui.QTreeWidget(self.settingsTab)
        self.settingsTree.setMinimumSize(QtCore.QSize(300, 0))
        self.settingsTree.setFrameShape(QtGui.QFrame.StyledPanel)
        self.settingsTree.setFrameShadow(QtGui.QFrame.Sunken)
        self.settingsTree.setObjectName(_fromUtf8("settingsTree"))
        self.settingsTree.header().setVisible(False)
        self.settingsTree.header().setCascadingSectionResizes(False)
        self.settingsTree.header().setDefaultSectionSize(200)
        self.verticalLayout.addWidget(self.settingsTree)
        self.tabPanel.addTab(self.settingsTab, _fromUtf8(""))
        self.verticalLayout_6.addWidget(self.tabPanel)
        self.widget = QtGui.QWidget(MainDialog)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem6 = QtGui.QSpacerItem(40, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.buttonCreateApp = QtGui.QPushButton(self.widget)
        self.buttonCreateApp.setIcon(icon)
        self.buttonCreateApp.setObjectName(_fromUtf8("buttonCreateApp"))
        self.horizontalLayout_2.addWidget(self.buttonCreateApp)
        self.buttonUpdate = QtGui.QPushButton(self.widget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/preview.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonUpdate.setIcon(icon7)
        self.buttonUpdate.setObjectName(_fromUtf8("buttonUpdate"))
        self.horizontalLayout_2.addWidget(self.buttonUpdate)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_6.addWidget(self.widget)
        self.verticalLayout_2.addLayout(self.verticalLayout_6)

        self.retranslateUi(MainDialog)
        self.tabPanel.setCurrentIndex(0)
        self.tabWidgetDeploy.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(_translate("MainDialog", "Web App Builder", None))
        self.label_3.setText(_translate("MainDialog", "Title", None))
        self.titleBox.setText(_translate("MainDialog", "My Web App", None))
        self.groupHeader.setTitle(_translate("MainDialog", "Header", None))
        self.label_16.setText(_translate("MainDialog", "Background image", None))
        self.buttonSelectImgFilepath.setText(_translate("MainDialog", "...", None))
        self.label_4.setText(_translate("MainDialog", "Text", None))
        self.labelEditHeaderCss.setText(_translate("MainDialog", "<a href=\'css\'>Edit css</a>", None))
        self.groupFooter.setTitle(_translate("MainDialog", "Footer", None))
        self.label_18.setText(_translate("MainDialog", "Text", None))
        self.labelEditFooterCss.setText(_translate("MainDialog", "<a href=\'css\'>Edit css</a>", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.descriptionTab), _translate("MainDialog", "Description", None))
        self.mapQuestAerialButton.setText(_translate("MainDialog", "MapQuest Aerial", None))
        self.mapQuestButton.setText(_translate("MainDialog", "MapQuest", None))
        self.stamenWatercolorButton.setText(_translate("MainDialog", "Stamen Watercolor", None))
        self.stamenTonerButton.setText(_translate("MainDialog", "Stamen Toner", None))
        self.osmButton.setText(_translate("MainDialog", "OSM", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.baseLayerTab), _translate("MainDialog", "Base Layers", None))
        self.layersTree.headerItem().setText(1, _translate("MainDialog", "2", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.layersTab), _translate("MainDialog", "Layers", None))
        self.label_2.setText(_translate("MainDialog", "Click to select widgets to include. Right click to customize widget", None))
        self.scaleBarButton.setText(_translate("MainDialog", "Scale Bar", None))
        self.zoomControlsButton.setText(_translate("MainDialog", "Zoom Controls", None))
        self.layersListButton.setText(_translate("MainDialog", "Layers List", None))
        self.overviewButton.setText(_translate("MainDialog", "Overview Map", None))
        self.fullScreenButton.setText(_translate("MainDialog", "Full Screen", None))
        self.attributionButton.setText(_translate("MainDialog", "Attribution", None))
        self.northArrowButton.setText(_translate("MainDialog", "North Arrow", None))
        self.zoomToExtentButton.setText(_translate("MainDialog", "Zoom to Extent", None))
        self.zoomSliderButton.setText(_translate("MainDialog", "Zoom Slider", None))
        self.exportAsImageButton.setText(_translate("MainDialog", "Export as image", None))
        self.mousePositionButton.setText(_translate("MainDialog", "Mouse Position", None))
        self.textPanelButton.setText(_translate("MainDialog", "Text panel", None))
        self.cesiumButton.setText(_translate("MainDialog", "3D View", None))
        self.attributesTableButton.setText(_translate("MainDialog", "Attributes Table", None))
        self.editToolButton.setText(_translate("MainDialog", "Edit Tool", None))
        self.searchButton.setText(_translate("MainDialog", "Search", None))
        self.legendButton.setText(_translate("MainDialog", "Legend", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.widgetsTab), _translate("MainDialog", "Widgets", None))
        self.postgisGroupBox.setTitle(_translate("MainDialog", "PostGIS", None))
        self.label_8.setText(_translate("MainDialog", "Password", None))
        self.postgisHostBox.setText(_translate("MainDialog", "localhost", None))
        self.label_10.setText(_translate("MainDialog", "Port", None))
        self.label_11.setText(_translate("MainDialog", "Username", None))
        self.label_12.setText(_translate("MainDialog", "Schema", None))
        self.postgisPortBox.setText(_translate("MainDialog", "5432", None))
        self.postgisSchemaBox.setPlaceholderText(_translate("MainDialog", "[Leave blank to use project name]", None))
        self.postgisDatabaseBox.setText(_translate("MainDialog", "geogig", None))
        self.label_13.setText(_translate("MainDialog", "Host", None))
        self.label_14.setText(_translate("MainDialog", "Database", None))
        self.postgisUsernameBox.setText(_translate("MainDialog", "postgres", None))
        self.postgisPasswordBox.setText(_translate("MainDialog", "postgres", None))
        self.geoserverGroupBox.setTitle(_translate("MainDialog", "GeoServer", None))
        self.geoserverUrlBox.setText(_translate("MainDialog", "http://localhost:8080/geoserver", None))
        self.label_7.setText(_translate("MainDialog", "Password", None))
        self.geoserverPasswordBox.setText(_translate("MainDialog", "geoserver", None))
        self.geoserverUsernameBox.setText(_translate("MainDialog", "admin", None))
        self.label_6.setText(_translate("MainDialog", "Username", None))
        self.label.setText(_translate("MainDialog", "Url", None))
        self.geoserverWorkspaceBox.setPlaceholderText(_translate("MainDialog", "[leave blank to use project name]", None))
        self.label_5.setText(_translate("MainDialog", "Workspace", None))
        self.groupBox_3.setTitle(_translate("MainDialog", "Deploy app to", None))
        self.label_9.setText(_translate("MainDialog", "Filepath", None))
        self.filepathBox.setText(_translate("MainDialog", "d:\\deploy", None))
        self.buttonSelectFilepath.setText(_translate("MainDialog", "...", None))
        self.tabWidgetDeploy.setTabText(self.tabWidgetDeploy.indexOf(self.deployLocalTab), _translate("MainDialog", "Local", None))
        self.tabWidgetDeploy.setTabText(self.tabWidgetDeploy.indexOf(self.deployRemoteTab), _translate("MainDialog", "Remote", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.suiteTab), _translate("MainDialog", "Deploy", None))
        self.settingsTree.headerItem().setText(0, _translate("MainDialog", "Setting", None))
        self.settingsTree.headerItem().setText(1, _translate("MainDialog", "Value", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.settingsTab), _translate("MainDialog", "Settings", None))
        self.buttonCreateApp.setText(_translate("MainDialog", "Create App", None))
        self.buttonUpdate.setText(_translate("MainDialog", "Preview", None))

import resources_rc
