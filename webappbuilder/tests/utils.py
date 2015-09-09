import os
from qgis.utils import iface
from qgis.core import *
from webappbuilder.appcreator import loadAppdef
from webappbuilder.appcreator import processAppdef
from webappbuilder.appcreator import createApp
from webappbuilder.appwriter import writeWebApp
from webappbuilder.utils import tempFolderInTempFolder

def loadTestProject(name = "base"):
    projectFile = os.path.join(os.path.dirname(__file__), "data", name + ".qgs")
    currentProjectFile  = QgsProject.instance().fileName()
    if os.path.normpath(currentProjectFile) != os.path.normpath(projectFile):
        iface.addProject(projectFile)

def testAppdef(name):
    filename = os.path.join(os.path.dirname(__file__), "data", name + ".appdef")
    appdef = loadAppdef(filename)
    processAppdef(appdef)
    return appdef

class SilentProgress():
    def setText(_, text):
        pass
    def setProgress(_, i):
        pass

def createAppFromTestAppdef(appdefName):
    appdef = testAppdef(appdefName)
    folder = tempFolderInTempFolder()
    writeWebApp(appdef, folder, True, SilentProgress())
    return folder

def compareWithExpectedOutputFile(file1, file2):
    with open(file1) as f:
        content = f.read()
    filename2 = os.path.join(os.path.dirname(__file__), "expected", file2)
    with open(filename2) as f:
        content2 = f.read()
    return content == content2
