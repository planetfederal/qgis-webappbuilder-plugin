import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import resources_rc
from maindialog import MainDialog


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
        dlg = MainDialog()
        dlg.exec_()
