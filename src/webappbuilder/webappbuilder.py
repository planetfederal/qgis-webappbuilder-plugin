import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import resources_rc
from maindialog import MainDialog
from appcreator import loadAppdef
from settings import initialize

class WebAppBuilderPlugin:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/icons/opengeo.png")
        self.action = QAction(icon, "Web App Builder", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("Boundless", self.action)
        try:
            from github import addUpdatePluginMenu
            addUpdatePluginMenu("Boundless", "volaya", "webappbuilder")
        except:
            pass

    def unload(self):
        self.iface.removePluginMenu("Boundless", self.action)
        try:
            from github import removeUpdatePluginMenu
            removeUpdatePluginMenu("Boundless")
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
