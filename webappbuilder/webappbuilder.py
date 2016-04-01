import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from maindialog import MainDialog
from appcreator import loadAppdef
from settings import initialize
import shutil
from utils import tempFolder
import webbrowser


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
        self.action.triggered.connect(self.run)
        self.iface.addPluginToWebMenu("Web App Builder", self.action)
        helpIcon = QgsApplication.getThemeIcon('/mActionHelpAPI.png')
        self.helpAction = QAction(helpIcon, "Web App Builder Help", self.iface.mainWindow())
        self.helpAction.triggered.connect(lambda: webbrowser.open_new("http://boundlessgeo.github.io/qgis-app-builder/"))
        self.iface.addPluginToWebMenu("Web App Builder", self.helpAction)

    def unload(self):
        self.iface.removePluginWebMenu("Web App Builder", self.action)
        self.iface.removePluginWebMenu("Web App Builder", self.helpAction)
        shutil.rmtree(tempFolder())

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
