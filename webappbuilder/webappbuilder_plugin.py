# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import traceback

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from webappbuilder.maindialog import MainDialog
from webappbuilder.appcreator import loadAppdef
from webappbuilder.settings import initialize
from qgiscommons2.files import removeTempFolder
from qgiscommons2.gui import addHelpMenu, removeHelpMenu, addAboutMenu, removeAboutMenu
from qgiscommons2.settings import readSettings, pluginSetting
from qgiscommons2.gui.settings import addSettingsMenu, removeSettingsMenu
import utils

class WebAppBuilderPlugin:

    def __init__(self, iface):
        self.iface = iface
        try:
            from webappbuilder.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "Web App Builder")
        except:
            pass
        readSettings()

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/icons/sdk.svg")
        self.action = QAction(icon, "Web App Builder", self.iface.mainWindow())
        self.action.setObjectName("startWebAppBuilder")
        self.action.triggered.connect(self.run)

        self.iface.addWebToolBarIcon(self.action)
        self.iface.addPluginToWebMenu("Web App Builder", self.action)

        addSettingsMenu("Web App Builder", self.iface.addPluginToWebMenu)
        addHelpMenu("Web App Builder", self.iface.addPluginToWebMenu)
        addAboutMenu("Web App Builder", self.iface.addPluginToWebMenu)

    def unload(self):
        self.iface.removeWebToolBarIcon(self.action)
        self.iface.removePluginWebMenu("Web App Builder", self.action)
        removeSettingsMenu("Web App Builder", self.iface.removePluginWebMenu)
        removeHelpMenu("Web App Builder", self.iface.removePluginWebMenu)
        removeAboutMenu("Web App Builder", self.iface.removePluginWebMenu)
        removeTempFolder()

        try:
            from webappbuilder.tests import testerplugin
            from qgistester.tests import removeTestModule
            removeTestModule(testerplugin, "Web App Builder")
        except:
            pass

    def run(self):
        appdef = None
        projFile = QgsProject.instance().fileName()
        if projFile:
            appdefFile =  projFile + ".appdef"
            if os.path.exists(appdefFile):
                if pluginSetting("askreload") == "Ask":
                    ret = QMessageBox.question(self.iface.mainWindow(), "Web app builder",
                                              "This project has been already published as a web app.\n"
                                              "Do you want to reload app configuration?",
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if ret == QMessageBox.Yes:
                        appdef = loadAppdef(appdefFile)
                elif pluginSetting("askreload") == "Open last configuration":
                    appdef = loadAppdef(appdefFile)
        initialize()
        # reset credential token in case related credentials are changed
        dlg = MainDialog(appdef)
        dlg.exec_()

