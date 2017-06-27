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
from PyQt4.QtCore import Qt, QSettings
from qgiscommons.settings import setPluginSetting, pluginSetting

AUTHDB_MASTERPWD = 'password'
AUTHM = None
AUTHDBDIR = tempfile.mkdtemp(prefix='tmp-qgis_authdb',
                             dir=tempfile.gettempdir())

widgets = ["aboutpanel", "attributestable", "attribution",
           "bookmarks", "charttool", "exportasimage", "fullscreen",
           "geocoding", "geolocation", "help", "homebutton", "layerslist",
           "legend", "links", "loadingpanel", "measuretools", "mouseposition",
           "northarrow", "overviewmap", "print", "query", "refresh", "scalebar",
           "selectiontools", "timeline", "drawfeature", "zoomcontrols", "zoomslider",
           "zoomtolatlon"]

widgetTestAbout = {"attributestable": "Open Attributes table and verify that it shows up and contains feature data",
             "attribution": "Check that the attribution widgets is shown in the lower right corner",
            "bookmarks": "Open the bookmarks menu and select one of the bookmarks. Verify that it zooms to it.",
            "bookmarks": "Click on the 'next' and 'back' arrows in the bookmarks panel to verify that the map moves accordingly",
            "charttool": "Open the Chart panel, clicking on the corresponding button. It will be empty. Activate the selection tool and select a few features in the map. Verify that a char is created and shown.",
            "fullscreen": "Verify that the fullscreen button is added and it works correctly.",
            "geocoding": "Search for 'Raleigh' in the geocoding panel and verify that selecting a search results causes the map to zoom",
            "geolocation": "Click on the geolocation icon and verify it zooms to you current location.",
            "help": "Verify that there is a help button and that it opens the web app help page",
            "homebutton": "Verify that there is a home button. Move the map view to a different location, and then click on the home button. Verify it return to the original extent.",
            "layerslist": "Verify that the layers list is correctly added and has content",
            "legend": "Verify that the legend is correctly added and has content",
            "links": "Verify links menu is added. Click on 'City of Raleigh' link and verify it opens in a new tab",
            "measuretools": "Verify that measure tools are added and working correctly.",
            "mouseposition": "Verify that the mouse position widget is located at the top-left corner, and that it changes its content as you move the mouse over the map.",
            "overviewmap": "Verify that the overview map is shown in the lower left corner",
            "print": "Verify print menu is available and contains two options. Chec that both have a correct thumbnail image",
            "query": "Open the Query panel. Select the 'Building' layer and enter the following filter: 'SHAPE_2_AR > 20000'. Click on 'New' and verify it selects some features in the map",
            "scalebar": "Verify scalebar is displayed in the lower part of the map.",
            "selectiontools": "Verify Selection tools are available and they work",
            "timeline": "Move timeline slider and verify that feature appear and disappear",
            "zoomcontrols": "Verify zoom controls are available and work correctly.",
            "zoomslider": "Verify zoom slider is available and work correctly."}

def loadTestProject(name = "base"):
    projectFile = os.path.join(os.path.dirname(__file__), "data", name + ".qgs")
    currentProjectFile  = QgsProject.instance().fileName()
    if os.path.normpath(currentProjectFile) != os.path.normpath(projectFile):
        iface.addProject(projectFile)

def testAppdef(name, process=True, aboutContent=None):
    filename = os.path.join(os.path.dirname(__file__), "data", name + ".appdef")
    appdef = loadAppdef(filename)
    if aboutContent:
        content = "<h1>Test instructions</h1><p>%s</p>" % aboutContent
        appdef["Widgets"]["aboutpanel"] = {"Parameters":{"content": content}}
    if process:
        processAppdef(appdef)
    return appdef

def openWAB(appdef=None):
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

def createAppFromTestAppdef(appdefName, preview=True, aboutContent=None):
    appdef = testAppdef(appdefName, True, aboutContent)
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
    _networkTimeout = QSettings().value("Qgis/networkAndProxy/networkTimeout")
    QSettings().setValue("Qgis/networkAndProxy/networkTimeout", value)

def resetNetworkTimeout():
    QSettings().setValue("Qgis/networkAndProxy/networkTimeout", _networkTimeout)

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
