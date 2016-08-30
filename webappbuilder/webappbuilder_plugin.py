# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import shutil
import webbrowser

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

from webappbuilder.maindialog import MainDialog
from webappbuilder.appcreator import loadAppdef
from webappbuilder.settings import initialize
from webappbuilder.utils import tempFolder


class WebAppBuilderPlugin:

    def __init__(self, iface):
        self.iface = iface
        try:
            from webappbuilder.tests import testerplugin
            from qgistester.tests import addTestModule
            addTestModule(testerplugin, "Web App Builder")
        except:
            pass

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/icons/opengeo.png")
        self.action = QAction(icon, "Web App Builder", self.iface.mainWindow())
        self.action.setObjectName("startWebAppBuilder")
        self.action.triggered.connect(self.run)

        helpIcon = QgsApplication.getThemeIcon('/mActionHelpAPI.png')
        self.helpAction = QAction(helpIcon, "Web App Builder Help", self.iface.mainWindow())
        self.helpAction.setObjectName("webAppBuilderHelp")
        self.helpAction.triggered.connect(lambda: webbrowser.open_new("http://boundlessgeo.github.io/qgis-plugins-documentation/webappbuilder/"))

        self.iface.addWebToolBarIcon(self.action)
        self.iface.addPluginToWebMenu("Web App Builder", self.action)
        self.iface.addPluginToWebMenu("Web App Builder", self.helpAction)

    def unload(self):
        self.iface.removeWebToolBarIcon(self.action)
        self.iface.removePluginWebMenu("Web App Builder", self.action)
        self.iface.removePluginWebMenu("Web App Builder", self.helpAction)
        shutil.rmtree(tempFolder())

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
                ret = QMessageBox.question(self.iface.mainWindow(), "Web app builder",
                                          "This project has been already published as a web app.\n"
                                          "Do you want to reload app configuration?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if ret == QMessageBox.Yes:
                    appdef = loadAppdef(appdefFile)
        initialize()
        dlg = MainDialog(appdef)
        dlg.exec_()
