from builtins import object
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import re
import codecs

from qgis.PyQt.QtWidgets import QDialog
from qgis.core import QgsProject
from qgis.utils import iface

from webappbuilder.appcreator import loadAppdef
from webappbuilder.appcreator import processAppdef
from webappbuilder.appcreator import createApp
from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.appwriter import writeWebApp
from webappbuilder.utils import tempFolderInTempFolder
from webappbuilder.maindialog import MainDialog
from webappbuilder.settings import initialize

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

class SilentProgress(object):
    def setText(_, text):
        pass
    def setProgress(_, i):
        pass

def createAppFromTestAppdef(appdefName, checkApp=False):
    appdef = testAppdef(appdefName)
    if checkApp:
        problems = checkAppCanBeCreated(appdef)
    folder = tempFolderInTempFolder()
    writeWebApp(appdef, folder, True, True, SilentProgress())
    return folder

def ignoreLayerID(text):
    """
    Normalize the digit part of an id identifier:

    id: "osm_placenames_large20160602142332803"
    becomes:
    id: "osm_placenames_large0000"
?
    """
    return re.sub(r'(id: "[^\d]+)(\d+)"', r'\g<1>0000', text)

def compareWithExpectedOutputFile(file1, file2, ignoreExtent=False):
    with codecs.open(file1, encoding="utf-8") as f:
        content = f.read()
    filename2 = os.path.join(os.path.dirname(__file__), "expected", file2)
    with codecs.open(filename2, encoding="utf-8") as f:
        content2 = f.read()
    content = "".join(content.split())
    content2 = "".join(content2.split())
    if ignoreExtent:
        content = removeExtent(content)
        content2 = removeExtent(content2)
    return ignoreLayerID(content2) in ignoreLayerID(content)

def checkTextInFile(filename, text):
    with codecs.open(filename, encoding="utf-8") as f:
        content = f.read()
    return text in content


def removeExtent(text):
    return re.sub('varoriginalExtent=(\\[.*?\\]);', '', text)
