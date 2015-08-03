# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_maindialog.ui'
#
# Created: Fri Jul 31 09:25:05 2015
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
        MainDialog.resize(742, 627)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/ol.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainDialog.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabPanel = QtGui.QTabWidget(MainDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabPanel.sizePolicy().hasHeightForWidth())
        self.tabPanel.setSizePolicy(sizePolicy)
        self.tabPanel.setTabPosition(QtGui.QTabWidget.North)
        self.tabPanel.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabPanel.setElideMode(QtCore.Qt.ElideRight)
        self.tabPanel.setUsesScrollButtons(True)
        self.tabPanel.setDocumentMode(False)
        self.tabPanel.setTabsClosable(False)
        self.tabPanel.setObjectName(_fromUtf8("tabPanel"))
        self.descriptionTab = QtGui.QWidget()
        self.descriptionTab.setObjectName(_fromUtf8("descriptionTab"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.descriptionTab)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.label_3 = QtGui.QLabel(self.descriptionTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_4.addWidget(self.label_3)
        self.titleBox = QtGui.QLineEdit(self.descriptionTab)
        self.titleBox.setObjectName(_fromUtf8("titleBox"))
        self.verticalLayout_4.addWidget(self.titleBox)
        self.label_16 = QtGui.QLabel(self.descriptionTab)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.verticalLayout_4.addWidget(self.label_16)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.logoBox = QtGui.QLineEdit(self.descriptionTab)
        self.logoBox.setText(_fromUtf8(""))
        self.logoBox.setObjectName(_fromUtf8("logoBox"))
        self.horizontalLayout_3.addWidget(self.logoBox)
        self.buttonLogo = QtGui.QToolButton(self.descriptionTab)
        self.buttonLogo.setObjectName(_fromUtf8("buttonLogo"))
        self.horizontalLayout_3.addWidget(self.buttonLogo)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.label_4 = QtGui.QLabel(self.descriptionTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        self.widgetThemes = QtGui.QWidget(self.descriptionTab)
        self.widgetThemes.setObjectName(_fromUtf8("widgetThemes"))
        self.gridLayoutThemes = QtGui.QGridLayout(self.widgetThemes)
        self.gridLayoutThemes.setMargin(0)
        self.gridLayoutThemes.setObjectName(_fromUtf8("gridLayoutThemes"))
        self.verticalLayout_4.addWidget(self.widgetThemes)
        spacerItem = QtGui.QSpacerItem(20, 15, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_4.addItem(spacerItem)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.buttonConfigureTheme = QtGui.QPushButton(self.descriptionTab)
        self.buttonConfigureTheme.setObjectName(_fromUtf8("buttonConfigureTheme"))
        self.horizontalLayout_6.addWidget(self.buttonConfigureTheme)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem2)
        self.tabPanel.addTab(self.descriptionTab, _fromUtf8(""))
        self.layersTab = QtGui.QWidget()
        self.layersTab.setObjectName(_fromUtf8("layersTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layersTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.filterLayersBox = QtGui.QLineEdit(self.layersTab)
        self.filterLayersBox.setObjectName(_fromUtf8("filterLayersBox"))
        self.horizontalLayout_5.addWidget(self.filterLayersBox)
        self.expandLayersButton = QtGui.QToolButton(self.layersTab)
        self.expandLayersButton.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.expandLayersButton.setIcon(icon1)
        self.expandLayersButton.setObjectName(_fromUtf8("expandLayersButton"))
        self.horizontalLayout_5.addWidget(self.expandLayersButton)
        self.collapseLayersButton = QtGui.QToolButton(self.layersTab)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.collapseLayersButton.setIcon(icon2)
        self.collapseLayersButton.setObjectName(_fromUtf8("collapseLayersButton"))
        self.horizontalLayout_5.addWidget(self.collapseLayersButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.layersTree = QtGui.QTreeWidget(self.layersTab)
        self.layersTree.setMinimumSize(QtCore.QSize(400, 300))
        self.layersTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.layersTree.setObjectName(_fromUtf8("layersTree"))
        self.layersTree.headerItem().setText(0, _fromUtf8("1"))
        self.layersTree.header().setVisible(False)
        self.layersTree.header().setDefaultSectionSize(200)
        self.verticalLayout_3.addWidget(self.layersTree)
        self.tabPanel.addTab(self.layersTab, _fromUtf8(""))
        self.baseLayerTab = QtGui.QWidget()
        self.baseLayerTab.setObjectName(_fromUtf8("baseLayerTab"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.baseLayerTab)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_17 = QtGui.QLabel(self.baseLayerTab)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.verticalLayout_6.addWidget(self.label_17)
        self.scrollArea = QtGui.QScrollArea(self.baseLayerTab)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.widgetBaseLayers = QtGui.QWidget()
        self.widgetBaseLayers.setGeometry(QtCore.QRect(0, 0, 698, 243))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetBaseLayers.sizePolicy().hasHeightForWidth())
        self.widgetBaseLayers.setSizePolicy(sizePolicy)
        self.widgetBaseLayers.setObjectName(_fromUtf8("widgetBaseLayers"))
        self.gridLayoutBaseLayers = QtGui.QGridLayout(self.widgetBaseLayers)
        self.gridLayoutBaseLayers.setObjectName(_fromUtf8("gridLayoutBaseLayers"))
        self.scrollArea.setWidget(self.widgetBaseLayers)
        self.verticalLayout_6.addWidget(self.scrollArea)
        self.label_18 = QtGui.QLabel(self.baseLayerTab)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_6.addWidget(self.label_18)
        self.scrollArea_2 = QtGui.QScrollArea(self.baseLayerTab)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName(_fromUtf8("scrollArea_2"))
        self.widgetBaseOverlays = QtGui.QWidget()
        self.widgetBaseOverlays.setGeometry(QtCore.QRect(0, 0, 698, 242))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetBaseOverlays.sizePolicy().hasHeightForWidth())
        self.widgetBaseOverlays.setSizePolicy(sizePolicy)
        self.widgetBaseOverlays.setObjectName(_fromUtf8("widgetBaseOverlays"))
        self.gridLayoutBaseOverlays = QtGui.QGridLayout(self.widgetBaseOverlays)
        self.gridLayoutBaseOverlays.setObjectName(_fromUtf8("gridLayoutBaseOverlays"))
        self.scrollArea_2.setWidget(self.widgetBaseOverlays)
        self.verticalLayout_6.addWidget(self.scrollArea_2)
        self.tabPanel.addTab(self.baseLayerTab, _fromUtf8(""))
        self.widgetsTab = QtGui.QWidget()
        self.widgetsTab.setObjectName(_fromUtf8("widgetsTab"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.widgetsTab)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_2 = QtGui.QLabel(self.widgetsTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_7.addWidget(self.label_2)
        self.scrollArea_3 = QtGui.QScrollArea(self.widgetsTab)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName(_fromUtf8("scrollArea_3"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 681, 774))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.scaleBarButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scaleBarButton.sizePolicy().hasHeightForWidth())
        self.scaleBarButton.setSizePolicy(sizePolicy)
        self.scaleBarButton.setMinimumSize(QtCore.QSize(120, 120))
        self.scaleBarButton.setMaximumSize(QtCore.QSize(120, 120))
        self.scaleBarButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/puzzle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scaleBarButton.setIcon(icon3)
        self.scaleBarButton.setIconSize(QtCore.QSize(32, 32))
        self.scaleBarButton.setCheckable(True)
        self.scaleBarButton.setChecked(True)
        self.scaleBarButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.scaleBarButton.setObjectName(_fromUtf8("scaleBarButton"))
        self.gridLayout_3.addWidget(self.scaleBarButton, 0, 0, 1, 1)
        self.zoomControlsButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomControlsButton.sizePolicy().hasHeightForWidth())
        self.zoomControlsButton.setSizePolicy(sizePolicy)
        self.zoomControlsButton.setMinimumSize(QtCore.QSize(120, 120))
        self.zoomControlsButton.setMaximumSize(QtCore.QSize(120, 120))
        self.zoomControlsButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.zoomControlsButton.setIcon(icon3)
        self.zoomControlsButton.setIconSize(QtCore.QSize(32, 32))
        self.zoomControlsButton.setCheckable(True)
        self.zoomControlsButton.setChecked(True)
        self.zoomControlsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoomControlsButton.setAutoRaise(False)
        self.zoomControlsButton.setArrowType(QtCore.Qt.NoArrow)
        self.zoomControlsButton.setObjectName(_fromUtf8("zoomControlsButton"))
        self.gridLayout_3.addWidget(self.zoomControlsButton, 0, 1, 1, 1)
        self.layersListButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layersListButton.sizePolicy().hasHeightForWidth())
        self.layersListButton.setSizePolicy(sizePolicy)
        self.layersListButton.setMinimumSize(QtCore.QSize(120, 120))
        self.layersListButton.setMaximumSize(QtCore.QSize(120, 120))
        self.layersListButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"     border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"    color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"     border-color:#4d8ef7;\n"
" }"))
        self.layersListButton.setIcon(icon3)
        self.layersListButton.setIconSize(QtCore.QSize(32, 32))
        self.layersListButton.setCheckable(True)
        self.layersListButton.setChecked(True)
        self.layersListButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.layersListButton.setObjectName(_fromUtf8("layersListButton"))
        self.gridLayout_3.addWidget(self.layersListButton, 0, 2, 1, 1)
        self.overviewButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overviewButton.sizePolicy().hasHeightForWidth())
        self.overviewButton.setSizePolicy(sizePolicy)
        self.overviewButton.setMinimumSize(QtCore.QSize(120, 120))
        self.overviewButton.setMaximumSize(QtCore.QSize(120, 120))
        self.overviewButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.overviewButton.setIcon(icon3)
        self.overviewButton.setIconSize(QtCore.QSize(32, 32))
        self.overviewButton.setCheckable(True)
        self.overviewButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.overviewButton.setObjectName(_fromUtf8("overviewButton"))
        self.gridLayout_3.addWidget(self.overviewButton, 0, 3, 1, 1)
        self.northArrowButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.northArrowButton.sizePolicy().hasHeightForWidth())
        self.northArrowButton.setSizePolicy(sizePolicy)
        self.northArrowButton.setMinimumSize(QtCore.QSize(120, 120))
        self.northArrowButton.setMaximumSize(QtCore.QSize(120, 120))
        self.northArrowButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.northArrowButton.setIcon(icon3)
        self.northArrowButton.setIconSize(QtCore.QSize(32, 32))
        self.northArrowButton.setCheckable(True)
        self.northArrowButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.northArrowButton.setObjectName(_fromUtf8("northArrowButton"))
        self.gridLayout_3.addWidget(self.northArrowButton, 0, 4, 1, 1)
        self.homeButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy)
        self.homeButton.setMinimumSize(QtCore.QSize(120, 120))
        self.homeButton.setMaximumSize(QtCore.QSize(120, 120))
        self.homeButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.homeButton.setIcon(icon3)
        self.homeButton.setIconSize(QtCore.QSize(32, 32))
        self.homeButton.setCheckable(True)
        self.homeButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.homeButton.setObjectName(_fromUtf8("homeButton"))
        self.gridLayout_3.addWidget(self.homeButton, 1, 0, 1, 1)
        self.fullScreenButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fullScreenButton.sizePolicy().hasHeightForWidth())
        self.fullScreenButton.setSizePolicy(sizePolicy)
        self.fullScreenButton.setMinimumSize(QtCore.QSize(120, 120))
        self.fullScreenButton.setMaximumSize(QtCore.QSize(120, 120))
        self.fullScreenButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.fullScreenButton.setIcon(icon3)
        self.fullScreenButton.setIconSize(QtCore.QSize(32, 32))
        self.fullScreenButton.setCheckable(True)
        self.fullScreenButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.fullScreenButton.setObjectName(_fromUtf8("fullScreenButton"))
        self.gridLayout_3.addWidget(self.fullScreenButton, 1, 1, 1, 1)
        self.attributionButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attributionButton.sizePolicy().hasHeightForWidth())
        self.attributionButton.setSizePolicy(sizePolicy)
        self.attributionButton.setMinimumSize(QtCore.QSize(120, 120))
        self.attributionButton.setMaximumSize(QtCore.QSize(120, 120))
        self.attributionButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.attributionButton.setIcon(icon3)
        self.attributionButton.setIconSize(QtCore.QSize(32, 32))
        self.attributionButton.setCheckable(True)
        self.attributionButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.attributionButton.setObjectName(_fromUtf8("attributionButton"))
        self.gridLayout_3.addWidget(self.attributionButton, 1, 2, 1, 1)
        self.zoomSliderButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoomSliderButton.sizePolicy().hasHeightForWidth())
        self.zoomSliderButton.setSizePolicy(sizePolicy)
        self.zoomSliderButton.setMinimumSize(QtCore.QSize(120, 120))
        self.zoomSliderButton.setMaximumSize(QtCore.QSize(120, 120))
        self.zoomSliderButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.zoomSliderButton.setIcon(icon3)
        self.zoomSliderButton.setIconSize(QtCore.QSize(32, 32))
        self.zoomSliderButton.setCheckable(True)
        self.zoomSliderButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.zoomSliderButton.setObjectName(_fromUtf8("zoomSliderButton"))
        self.gridLayout_3.addWidget(self.zoomSliderButton, 1, 3, 1, 1)
        self.measureToolButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.measureToolButton.sizePolicy().hasHeightForWidth())
        self.measureToolButton.setSizePolicy(sizePolicy)
        self.measureToolButton.setMinimumSize(QtCore.QSize(120, 120))
        self.measureToolButton.setMaximumSize(QtCore.QSize(120, 120))
        self.measureToolButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.measureToolButton.setIcon(icon3)
        self.measureToolButton.setIconSize(QtCore.QSize(32, 32))
        self.measureToolButton.setCheckable(True)
        self.measureToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.measureToolButton.setObjectName(_fromUtf8("measureToolButton"))
        self.gridLayout_3.addWidget(self.measureToolButton, 1, 4, 1, 1)
        self.selectionToolsButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectionToolsButton.sizePolicy().hasHeightForWidth())
        self.selectionToolsButton.setSizePolicy(sizePolicy)
        self.selectionToolsButton.setMinimumSize(QtCore.QSize(120, 120))
        self.selectionToolsButton.setMaximumSize(QtCore.QSize(120, 120))
        self.selectionToolsButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.selectionToolsButton.setIcon(icon3)
        self.selectionToolsButton.setIconSize(QtCore.QSize(32, 32))
        self.selectionToolsButton.setCheckable(True)
        self.selectionToolsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.selectionToolsButton.setObjectName(_fromUtf8("selectionToolsButton"))
        self.gridLayout_3.addWidget(self.selectionToolsButton, 2, 0, 1, 1)
        self.geolocationButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.geolocationButton.sizePolicy().hasHeightForWidth())
        self.geolocationButton.setSizePolicy(sizePolicy)
        self.geolocationButton.setMinimumSize(QtCore.QSize(120, 120))
        self.geolocationButton.setMaximumSize(QtCore.QSize(120, 120))
        self.geolocationButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.geolocationButton.setIcon(icon3)
        self.geolocationButton.setIconSize(QtCore.QSize(32, 32))
        self.geolocationButton.setCheckable(True)
        self.geolocationButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.geolocationButton.setObjectName(_fromUtf8("geolocationButton"))
        self.gridLayout_3.addWidget(self.geolocationButton, 2, 1, 1, 1)
        self.attributesTableButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attributesTableButton.sizePolicy().hasHeightForWidth())
        self.attributesTableButton.setSizePolicy(sizePolicy)
        self.attributesTableButton.setMinimumSize(QtCore.QSize(120, 120))
        self.attributesTableButton.setMaximumSize(QtCore.QSize(120, 120))
        self.attributesTableButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.attributesTableButton.setIcon(icon3)
        self.attributesTableButton.setIconSize(QtCore.QSize(32, 32))
        self.attributesTableButton.setCheckable(True)
        self.attributesTableButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.attributesTableButton.setObjectName(_fromUtf8("attributesTableButton"))
        self.gridLayout_3.addWidget(self.attributesTableButton, 2, 2, 1, 1)
        self.chartToolButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chartToolButton.sizePolicy().hasHeightForWidth())
        self.chartToolButton.setSizePolicy(sizePolicy)
        self.chartToolButton.setMinimumSize(QtCore.QSize(120, 120))
        self.chartToolButton.setMaximumSize(QtCore.QSize(120, 120))
        self.chartToolButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.chartToolButton.setIcon(icon3)
        self.chartToolButton.setIconSize(QtCore.QSize(32, 32))
        self.chartToolButton.setCheckable(True)
        self.chartToolButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.chartToolButton.setObjectName(_fromUtf8("chartToolButton"))
        self.gridLayout_3.addWidget(self.chartToolButton, 2, 3, 1, 1)
        self.legendButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.legendButton.sizePolicy().hasHeightForWidth())
        self.legendButton.setSizePolicy(sizePolicy)
        self.legendButton.setMinimumSize(QtCore.QSize(120, 120))
        self.legendButton.setMaximumSize(QtCore.QSize(120, 120))
        self.legendButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.legendButton.setIcon(icon3)
        self.legendButton.setIconSize(QtCore.QSize(32, 32))
        self.legendButton.setCheckable(True)
        self.legendButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.legendButton.setObjectName(_fromUtf8("legendButton"))
        self.gridLayout_3.addWidget(self.legendButton, 2, 4, 1, 1)
        self.mousePositionButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mousePositionButton.sizePolicy().hasHeightForWidth())
        self.mousePositionButton.setSizePolicy(sizePolicy)
        self.mousePositionButton.setMinimumSize(QtCore.QSize(120, 120))
        self.mousePositionButton.setMaximumSize(QtCore.QSize(120, 120))
        self.mousePositionButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.mousePositionButton.setIcon(icon3)
        self.mousePositionButton.setIconSize(QtCore.QSize(32, 32))
        self.mousePositionButton.setCheckable(True)
        self.mousePositionButton.setAutoRepeat(False)
        self.mousePositionButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.mousePositionButton.setObjectName(_fromUtf8("mousePositionButton"))
        self.gridLayout_3.addWidget(self.mousePositionButton, 3, 0, 1, 1)
        self.queryButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queryButton.sizePolicy().hasHeightForWidth())
        self.queryButton.setSizePolicy(sizePolicy)
        self.queryButton.setMinimumSize(QtCore.QSize(120, 120))
        self.queryButton.setMaximumSize(QtCore.QSize(120, 120))
        self.queryButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.queryButton.setIcon(icon3)
        self.queryButton.setIconSize(QtCore.QSize(32, 32))
        self.queryButton.setCheckable(True)
        self.queryButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.queryButton.setObjectName(_fromUtf8("queryButton"))
        self.gridLayout_3.addWidget(self.queryButton, 3, 1, 1, 1)
        self.geocodingButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.geocodingButton.sizePolicy().hasHeightForWidth())
        self.geocodingButton.setSizePolicy(sizePolicy)
        self.geocodingButton.setMinimumSize(QtCore.QSize(120, 120))
        self.geocodingButton.setMaximumSize(QtCore.QSize(120, 120))
        self.geocodingButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.geocodingButton.setIcon(icon3)
        self.geocodingButton.setIconSize(QtCore.QSize(32, 32))
        self.geocodingButton.setCheckable(True)
        self.geocodingButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.geocodingButton.setObjectName(_fromUtf8("geocodingButton"))
        self.gridLayout_3.addWidget(self.geocodingButton, 3, 2, 1, 1)
        self.bookmarksButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookmarksButton.sizePolicy().hasHeightForWidth())
        self.bookmarksButton.setSizePolicy(sizePolicy)
        self.bookmarksButton.setMinimumSize(QtCore.QSize(120, 120))
        self.bookmarksButton.setMaximumSize(QtCore.QSize(120, 120))
        self.bookmarksButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.bookmarksButton.setIcon(icon3)
        self.bookmarksButton.setIconSize(QtCore.QSize(32, 32))
        self.bookmarksButton.setCheckable(True)
        self.bookmarksButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.bookmarksButton.setObjectName(_fromUtf8("bookmarksButton"))
        self.gridLayout_3.addWidget(self.bookmarksButton, 3, 3, 1, 1)
        self.aboutPanelButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutPanelButton.sizePolicy().hasHeightForWidth())
        self.aboutPanelButton.setSizePolicy(sizePolicy)
        self.aboutPanelButton.setMinimumSize(QtCore.QSize(120, 120))
        self.aboutPanelButton.setMaximumSize(QtCore.QSize(120, 120))
        self.aboutPanelButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.aboutPanelButton.setIcon(icon3)
        self.aboutPanelButton.setIconSize(QtCore.QSize(32, 32))
        self.aboutPanelButton.setCheckable(True)
        self.aboutPanelButton.setChecked(False)
        self.aboutPanelButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.aboutPanelButton.setObjectName(_fromUtf8("aboutPanelButton"))
        self.gridLayout_3.addWidget(self.aboutPanelButton, 3, 4, 1, 1)
        self.exportAsImageButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportAsImageButton.sizePolicy().hasHeightForWidth())
        self.exportAsImageButton.setSizePolicy(sizePolicy)
        self.exportAsImageButton.setMinimumSize(QtCore.QSize(120, 120))
        self.exportAsImageButton.setMaximumSize(QtCore.QSize(120, 120))
        self.exportAsImageButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.exportAsImageButton.setIcon(icon3)
        self.exportAsImageButton.setIconSize(QtCore.QSize(32, 32))
        self.exportAsImageButton.setCheckable(True)
        self.exportAsImageButton.setChecked(False)
        self.exportAsImageButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.exportAsImageButton.setObjectName(_fromUtf8("exportAsImageButton"))
        self.gridLayout_3.addWidget(self.exportAsImageButton, 4, 0, 1, 1)
        self.linksButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linksButton.sizePolicy().hasHeightForWidth())
        self.linksButton.setSizePolicy(sizePolicy)
        self.linksButton.setMinimumSize(QtCore.QSize(120, 120))
        self.linksButton.setMaximumSize(QtCore.QSize(120, 120))
        self.linksButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.linksButton.setIcon(icon3)
        self.linksButton.setIconSize(QtCore.QSize(32, 32))
        self.linksButton.setCheckable(True)
        self.linksButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.linksButton.setObjectName(_fromUtf8("linksButton"))
        self.gridLayout_3.addWidget(self.linksButton, 4, 1, 1, 1)
        self.helpButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.helpButton.setSizePolicy(sizePolicy)
        self.helpButton.setMinimumSize(QtCore.QSize(120, 120))
        self.helpButton.setMaximumSize(QtCore.QSize(120, 120))
        self.helpButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.helpButton.setIcon(icon3)
        self.helpButton.setIconSize(QtCore.QSize(32, 32))
        self.helpButton.setCheckable(True)
        self.helpButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.gridLayout_3.addWidget(self.helpButton, 4, 2, 1, 1)
        self.analysisToolsButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analysisToolsButton.sizePolicy().hasHeightForWidth())
        self.analysisToolsButton.setSizePolicy(sizePolicy)
        self.analysisToolsButton.setMinimumSize(QtCore.QSize(120, 120))
        self.analysisToolsButton.setMaximumSize(QtCore.QSize(120, 120))
        self.analysisToolsButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.analysisToolsButton.setIcon(icon3)
        self.analysisToolsButton.setIconSize(QtCore.QSize(32, 32))
        self.analysisToolsButton.setCheckable(True)
        self.analysisToolsButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.analysisToolsButton.setObjectName(_fromUtf8("analysisToolsButton"))
        self.gridLayout_3.addWidget(self.analysisToolsButton, 4, 3, 1, 1)
        self.cesiumButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cesiumButton.sizePolicy().hasHeightForWidth())
        self.cesiumButton.setSizePolicy(sizePolicy)
        self.cesiumButton.setMinimumSize(QtCore.QSize(120, 120))
        self.cesiumButton.setMaximumSize(QtCore.QSize(120, 120))
        self.cesiumButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.cesiumButton.setIcon(icon3)
        self.cesiumButton.setIconSize(QtCore.QSize(32, 32))
        self.cesiumButton.setCheckable(True)
        self.cesiumButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.cesiumButton.setObjectName(_fromUtf8("cesiumButton"))
        self.gridLayout_3.addWidget(self.cesiumButton, 4, 4, 1, 1)
        self.timelineButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timelineButton.sizePolicy().hasHeightForWidth())
        self.timelineButton.setSizePolicy(sizePolicy)
        self.timelineButton.setMinimumSize(QtCore.QSize(120, 120))
        self.timelineButton.setMaximumSize(QtCore.QSize(120, 120))
        self.timelineButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.timelineButton.setIcon(icon3)
        self.timelineButton.setIconSize(QtCore.QSize(32, 32))
        self.timelineButton.setCheckable(True)
        self.timelineButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.timelineButton.setObjectName(_fromUtf8("timelineButton"))
        self.gridLayout_3.addWidget(self.timelineButton, 5, 0, 1, 1)
        self.addLayerButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addLayerButton.sizePolicy().hasHeightForWidth())
        self.addLayerButton.setSizePolicy(sizePolicy)
        self.addLayerButton.setMinimumSize(QtCore.QSize(120, 120))
        self.addLayerButton.setMaximumSize(QtCore.QSize(120, 120))
        self.addLayerButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.addLayerButton.setIcon(icon3)
        self.addLayerButton.setIconSize(QtCore.QSize(32, 32))
        self.addLayerButton.setCheckable(True)
        self.addLayerButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.addLayerButton.setObjectName(_fromUtf8("addLayerButton"))
        self.gridLayout_3.addWidget(self.addLayerButton, 5, 1, 1, 1)
        self.printButton = QtGui.QToolButton(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printButton.sizePolicy().hasHeightForWidth())
        self.printButton.setSizePolicy(sizePolicy)
        self.printButton.setMinimumSize(QtCore.QSize(120, 120))
        self.printButton.setMaximumSize(QtCore.QSize(120, 120))
        self.printButton.setStyleSheet(_fromUtf8("QToolButton {\n"
"     background-color: #7c899f;\n"
"   border-color: #7c899f;\n"
"     border-style: solid;\n"
"     border-width: 3px;\n"
"     border-radius: 10px;\n"
"     font: bold 11px;\n"
"     padding: 15px;\n"
"  color: white;\n"
" }\n"
" QToolButton:checked {\n"
"     background-color: #2d67c6;\n"
"   border-color:#4d8ef7;\n"
" }"))
        self.printButton.setIcon(icon3)
        self.printButton.setIconSize(QtCore.QSize(32, 32))
        self.printButton.setCheckable(True)
        self.printButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.printButton.setObjectName(_fromUtf8("printButton"))
        self.gridLayout_3.addWidget(self.printButton, 5, 2, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 6, 0, 1, 1)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_7.addWidget(self.scrollArea_3)
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
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem4)
        self.checkBoxDeployData = QtGui.QCheckBox(self.suiteTab)
        self.checkBoxDeployData.setObjectName(_fromUtf8("checkBoxDeployData"))
        self.verticalLayout_8.addWidget(self.checkBoxDeployData)
        self.label_9 = QtGui.QLabel(self.suiteTab)
        self.label_9.setStyleSheet(_fromUtf8("color: rgb(163, 163, 163);"))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_8.addWidget(self.label_9)
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
        self.verticalLayout_2.addWidget(self.tabPanel)
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
        self.progressLabel = QtGui.QLabel(self.widget)
        self.progressLabel.setObjectName(_fromUtf8("progressLabel"))
        self.horizontalLayout_2.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout_2.addWidget(self.progressBar)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.buttonOpen = QtGui.QPushButton(self.widget)
        self.buttonOpen.setText(_fromUtf8(""))
        self.buttonOpen.setObjectName(_fromUtf8("buttonOpen"))
        self.horizontalLayout_2.addWidget(self.buttonOpen)
        self.buttonSave = QtGui.QPushButton(self.widget)
        self.buttonSave.setText(_fromUtf8(""))
        self.buttonSave.setObjectName(_fromUtf8("buttonSave"))
        self.horizontalLayout_2.addWidget(self.buttonSave)
        self.buttonHelp = QtGui.QPushButton(self.widget)
        self.buttonHelp.setText(_fromUtf8(""))
        self.buttonHelp.setObjectName(_fromUtf8("buttonHelp"))
        self.horizontalLayout_2.addWidget(self.buttonHelp)
        self.buttonCreateApp = QtGui.QPushButton(self.widget)
        self.buttonCreateApp.setIcon(icon)
        self.buttonCreateApp.setObjectName(_fromUtf8("buttonCreateApp"))
        self.horizontalLayout_2.addWidget(self.buttonCreateApp)
        self.buttonPreview = QtGui.QPushButton(self.widget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/qgis2ol/icons/preview.gif")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonPreview.setIcon(icon4)
        self.buttonPreview.setObjectName(_fromUtf8("buttonPreview"))
        self.horizontalLayout_2.addWidget(self.buttonPreview)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(MainDialog)
        self.tabPanel.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainDialog)

    def retranslateUi(self, MainDialog):
        MainDialog.setWindowTitle(_translate("MainDialog", "Web App Builder", None))
        self.label_3.setText(_translate("MainDialog", "<b>App Title</b>", None))
        self.titleBox.setText(_translate("MainDialog", "My Web App", None))
        self.label_16.setText(_translate("MainDialog", "<b>Logo image</b>", None))
        self.buttonLogo.setText(_translate("MainDialog", "...", None))
        self.label_4.setText(_translate("MainDialog", "<b>Theme</b>", None))
        self.buttonConfigureTheme.setText(_translate("MainDialog", "Configure theme...", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.descriptionTab), _translate("MainDialog", "Description", None))
        self.filterLayersBox.setPlaceholderText(_translate("MainDialog", "Enter text to filter layers list...", None))
        self.expandLayersButton.setToolTip(_translate("MainDialog", "Expand layers", None))
        self.collapseLayersButton.setToolTip(_translate("MainDialog", "Collapase layers", None))
        self.collapseLayersButton.setText(_translate("MainDialog", "-", None))
        self.layersTree.headerItem().setText(1, _translate("MainDialog", "2", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.layersTab), _translate("MainDialog", "QGIS Layers", None))
        self.label_17.setText(_translate("MainDialog", "<b>Base Layers</b>", None))
        self.label_18.setText(_translate("MainDialog", "<b>Overlays</b>", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.baseLayerTab), _translate("MainDialog", "Other Layers", None))
        self.label_2.setText(_translate("MainDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Controls</span> (right click to configure)</p></body></html>", None))
        self.scaleBarButton.setText(_translate("MainDialog", "Scale bar", None))
        self.zoomControlsButton.setText(_translate("MainDialog", "Zoom", None))
        self.layersListButton.setText(_translate("MainDialog", "Layers\n"
"list", None))
        self.overviewButton.setText(_translate("MainDialog", "Overview\n"
"map", None))
        self.northArrowButton.setText(_translate("MainDialog", "North\n"
"arrow", None))
        self.homeButton.setText(_translate("MainDialog", "Home \n"
"button", None))
        self.fullScreenButton.setText(_translate("MainDialog", "Full \n"
"screen", None))
        self.attributionButton.setText(_translate("MainDialog", "Attribution", None))
        self.zoomSliderButton.setText(_translate("MainDialog", "Zoom\n"
"slider", None))
        self.measureToolButton.setText(_translate("MainDialog", "Measure", None))
        self.selectionToolsButton.setText(_translate("MainDialog", "Selection", None))
        self.geolocationButton.setText(_translate("MainDialog", "Geolocation", None))
        self.attributesTableButton.setText(_translate("MainDialog", "Attributes\n"
"table", None))
        self.chartToolButton.setText(_translate("MainDialog", "Charts", None))
        self.legendButton.setText(_translate("MainDialog", "Legend", None))
        self.mousePositionButton.setText(_translate("MainDialog", "Mouse \n"
"position", None))
        self.queryButton.setText(_translate("MainDialog", "Query", None))
        self.geocodingButton.setText(_translate("MainDialog", "Geocoding", None))
        self.bookmarksButton.setText(_translate("MainDialog", "Bookmarks", None))
        self.aboutPanelButton.setText(_translate("MainDialog", "About\n"
"panel", None))
        self.exportAsImageButton.setText(_translate("MainDialog", "Export as\n"
"image", None))
        self.linksButton.setText(_translate("MainDialog", "Links", None))
        self.helpButton.setText(_translate("MainDialog", "Help", None))
        self.analysisToolsButton.setText(_translate("MainDialog", "Analysis", None))
        self.cesiumButton.setText(_translate("MainDialog", "3D View", None))
        self.timelineButton.setText(_translate("MainDialog", "Timeline", None))
        self.addLayerButton.setText(_translate("MainDialog", "Add layer", None))
        self.printButton.setText(_translate("MainDialog", "Print", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.widgetsTab), _translate("MainDialog", "Controls", None))
        self.postgisGroupBox.setTitle(_translate("MainDialog", "PostGIS", None))
        self.label_8.setText(_translate("MainDialog", "Password", None))
        self.postgisHostBox.setText(_translate("MainDialog", "localhost", None))
        self.label_10.setText(_translate("MainDialog", "Port", None))
        self.label_11.setText(_translate("MainDialog", "Username", None))
        self.label_12.setText(_translate("MainDialog", "Schema", None))
        self.postgisPortBox.setText(_translate("MainDialog", "5432", None))
        self.postgisSchemaBox.setPlaceholderText(_translate("MainDialog", "[Leave blank to use project name]", None))
        self.postgisDatabaseBox.setText(_translate("MainDialog", "database", None))
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
        self.checkBoxDeployData.setText(_translate("MainDialog", "Do not deploy layer data", None))
        self.label_9.setText(_translate("MainDialog", "Check this box only if you are updating the UI of an existing app", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.suiteTab), _translate("MainDialog", "Deploy", None))
        self.settingsTree.headerItem().setText(0, _translate("MainDialog", "Setting", None))
        self.settingsTree.headerItem().setText(1, _translate("MainDialog", "Value", None))
        self.tabPanel.setTabText(self.tabPanel.indexOf(self.settingsTab), _translate("MainDialog", "Settings", None))
        self.progressLabel.setText(_translate("MainDialog", "progress", None))
        self.buttonCreateApp.setText(_translate("MainDialog", "Create App", None))
        self.buttonPreview.setText(_translate("MainDialog", "Preview", None))

import resources_rc
