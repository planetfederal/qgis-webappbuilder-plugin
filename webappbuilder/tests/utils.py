# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
from qgis.utils import iface
from qgis.core import *
from webappbuilder.appcreator import loadAppdef
from webappbuilder.appcreator import processAppdef
from webappbuilder.appcreator import createApp
from webappbuilder.appwriter import writeWebApp
from webappbuilder.utils import tempFolderInTempFolder
from webappbuilder.maindialog import MainDialog
from webappbuilder.settings import initialize
from PyQt4.QtGui import QDialog

def loadTestProject(name = "base"):
    projectFile = os.path.join(os.path.dirname(__file__), "data", name + ".qgs")
    currentProjectFile  = QgsProject.instance().fileName()
    if os.path.normpath(currentProjectFile) != os.path.normpath(projectFile):
        iface.addProject(projectFile)

def testAppdef(name, process = True):
    filename = os.path.join(os.path.dirname(__file__), "data", name + ".appdef")
    appdef = loadAppdef(filename)
    if process:
        processAppdef(appdef)
    return appdef

def openWAB(appdef = None):
    initialize()
    dlg = MainDialog(appdef)
    dlg.open()

def closeWAB():
    for dialog in iface.mainWindow().children():
        if isinstance(dialog, QDialog) and dialog.objectName() == "WebAppBuilderDialog":
            dialog.close()

class SilentProgress():
    def setText(_, text):
        pass
    def setProgress(_, i):
        pass

def createAppFromTestAppdef(appdefName):
    appdef = testAppdef(appdefName)
    folder = tempFolderInTempFolder()
    writeWebApp(appdef, folder, True, True, SilentProgress())
    return folder

def compareWithExpectedOutputFile(file1, file2):
    with open(file1) as f:
        content = f.read()
    filename2 = os.path.join(os.path.dirname(__file__), "expected", file2)
    with open(filename2) as f:
        content2 = f.read()
    return content2 in content

def checkTextInFile(filename, text):
    with open(filename) as f:
        content = f.read()
    return text in content
