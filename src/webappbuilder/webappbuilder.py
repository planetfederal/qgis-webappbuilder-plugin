import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import resources_rc
from maindialog import MainDialog
from appcreator import loadAppdef


class WebAppBuilderPlugin:

    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        icon = QIcon(os.path.dirname(__file__) + "/icons/opengeo.png")
        self.action = QAction(icon, "Web App Builder", self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu("Boundless", self.action)

    def unload(self):
        self.iface.removePluginMenu("Boundless", self.action)

    def run(self):
        appdef = None
        projFile = QgsProject.instance().fileName()
        if projFile:
            ret = QMessageBox.question(self.iface.mainWindow(), "Web app builder",
                                          "This project has been already published as a web app.\n"
                                          "Do you want to reload app configuration?",
                                          QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if ret == QMessageBox.Yes:
                appdefFile =  projFile + ".appdef"
                appdef = loadAppdef(appdefFile)
        dlg = MainDialog(appdef)
        dlg.exec_()
