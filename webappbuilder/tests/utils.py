# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import re
import codecs
import tempfile
from qgis.utils import iface
from qgis.core import *
from webappbuilder.appcreator import loadAppdef
from webappbuilder.appcreator import processAppdef
from webappbuilder.appcreator import createApp
from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.appwriter import writeWebApp
from qgiscommons.files import tempFolderInTempFolder
from webappbuilder.maindialog import MainDialog
from webappbuilder.settings import initialize
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import Qt
from qgiscommons.settings import setPluginSetting, pluginSetting

AUTHDB_MASTERPWD = 'password'
AUTHM = None
AUTHDBDIR = tempfile.mkdtemp(prefix='tmp-qgis_authdb',
                             dir=tempfile.gettempdir())

widgets = ["aboutpanel", "addlayer", "attributestable", "attribution",
           "bookmarks", "charttool", "edit", "exportasimage", "fullscreen",
           "geocoding", "geolocation", "help", "homebutton", "layerslist",
           "legend", "links", "loadingpanel", "measuretools", "mouseposition",
           "northarrow", "overviewmap", "print", "query", "refresh", "scalebar",
           "selectiontools", "timeline", "wfst", "zoomcontrols", "zoomslider"]

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
    dlg = MainDialog(appdef, parent=iface.mainWindow())
    dlg.open()
    dlg.setWindowModality(Qt.NonModal)

def hideWAB():
    dlg = getWABDialog()
    if dlg:
        dlg.hide()

def showWAB():
    dlg = getWABDialog()
    if dlg:
        dlg.show()

def closeWAB():
    for dialog in iface.mainWindow().children():
        if isinstance(dialog, QDialog) and dialog.objectName() == "WABMainDialog":
            dialog.close()
            # necessary to delete Dialog instance to avoid inter test
            # dependencies and GUI memory
            dialog.deleteLater()

def getWABDialog():
    for child in iface.mainWindow().children():
        if isinstance(child, MainDialog) and child.objectName() == "WABMainDialog":
            return child
    return None

class SilentProgress():
    def setText(_, text):
        pass
    def setProgress(_, i):
        pass

def createAppFromTestAppdef(appdefName, checkApp=False, preview=True):
    appdef = testAppdef(appdefName)
    if checkApp:
        problems = checkAppCanBeCreated(appdef)
    folder = tempFolderInTempFolder("webappbuilder")
    writeWebApp(appdef, folder, preview, SilentProgress())
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

_sdkEndpoint = None
def _setWrongSdkEndpoint():
    global _sdkEndpoint
    _sdkEndpoint = pluginSetting("sdkendpoint")
    setPluginSetting("sdkendpoint", "wrong")

def _resetSdkEndpoint():
    setPluginSetting("sdkendpoint", _sdkEndpoint)
    closeWAB()

_networkTimeout = None
def setNetworkTimeout(value=60000):
    global _networkTimeout
    _networkTimeout = pluginSetting("networkAndProxy/networkTimeout", namespace="Qgis")
    setPluginSetting("networkAndProxy/networkTimeout", value, namespace="Qgis")

def resetNetworkTimeout():
    setPluginSetting("networkAndProxy/networkTimeout", _networkTimeout, namespace="Qgis")

def initAuthManager():
    """
    Setup AuthManager instance.
    heavily based on testqgsauthmanager.cpp.
    """
    global AUTHM
    if not AUTHM:
        AUTHM = QgsAuthManager.instance()
        # check if QgsAuthManager has been already initialised... a side effect
        # of the QgsAuthManager.init() is that AuthDbPath is set
        if AUTHM.authenticationDbPath():
            # already initilised => we are inside QGIS. Assumed that the
            # actual qgis_auth.db has the same master pwd as AUTHDB_MASTERPWD
            if AUTHM.masterPasswordIsSet():
                msg = 'Auth master password not set from passed string'
                assert AUTHM.masterPasswordSame(AUTHDB_MASTERPWD)
            else:
                msg = 'Master password could not be set'
                assert AUTHM.setMasterPassword(AUTHDB_MASTERPWD, True), msg
        else:
            # outside qgis => setup env var before db init
            os.environ['QGIS_AUTH_DB_DIR_PATH'] = AUTHDBDIR
            msg = 'Master password could not be set'
            assert AUTHM.setMasterPassword(AUTHDB_MASTERPWD, True), msg
            AUTHM.init(AUTHDBDIR)
