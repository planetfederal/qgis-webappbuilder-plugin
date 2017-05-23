# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import re
from qgis.core import *
from qgis.gui import *
import qgis.utils
import qgis
import subprocess
import uuid
import base64
from PyQt4.QtCore import *
from PyQt4.QtGui import QFileDialog, QApplication, QCursor
import inspect
import codecs
import json
from qgiscommons.networkaccessmanager import NetworkAccessManager
from qgiscommons.settings import pluginSetting, setPluginSetting
import urllib.parse

#authEndpointUrl = "https://api.dev.boundlessgeo.io/v1/token/"
#wabCompilerUrl = "http://localhost:8080/package/"

def wabCompilerUrl():
    return urllib.parse.unquote(pluginSetting("sdkendpoint").rstrip("/") + "/package")

def wabVersionUrl():
    return urllib.parse.unquote(pluginSetting("sdkendpoint").rstrip("/") + "/version")


def authUrl():
    return urllib.parse.unquote(pluginSetting("tokenendpoint"))

class topics:
    """Class to store PyPubSub topics shared among various parts of code."""
    endFunction = "endFunction"
    endWriteWebApp = "endWriteWebApp"
    endAppSDKification = "endAppSDKification"

    def __init__():
        pass

MULTIPLE_SELECTION_DISABLED = 0
MULTIPLE_SELECTION_ALT_KEY = 1
MULTIPLE_SELECTION_SHIFT_KEY = 2
MULTIPLE_SELECTION_NO_KEY = 3


try:
    from qgis.core import QGis
    TYPE_MAP = {
        QGis.WKBPoint: 'Point',
        QGis.WKBLineString: 'LineString',
        QGis.WKBPolygon: 'Polygon',
        QGis.WKBMultiPoint: 'MultiPoint',
        QGis.WKBMultiLineString: 'MultiLineString',
        QGis.WKBMultiPolygon: 'MultiPolygon',
    }
    QGisPoint = QGis.WKBPoint

except ImportError:
    from qgis.core import Qgis as QGis
    from qgis.core import QgsWkbTypes
    TYPE_MAP = {
        QgsWkbTypes.Point: 'Point',
        QgsWkbTypes.LineString: 'LineString',
        QgsWkbTypes.Polygon: 'Polygon',
        QgsWkbTypes.MultiPoint: 'MultiPoint',
        QgsWkbTypes.MultiLineString: 'MultiLineString',
        QgsWkbTypes.MultiPolygon: 'MultiPolygon',
    }
    QGisPoint = QgsWkbTypes.Point

class Layer():

    def __init__(self, layer, visible, popup, clusterDistance, clusterColor,
                 allowSelection, showInOverview, timeInfo, showInControls,
                 singleTile):
        self.layer = layer
        self.visible = visible
        self.popup = popup
        self.clusterDistance = clusterDistance
        self.clusterColor = clusterColor
        self.allowSelection = allowSelection
        self.showInOverview = showInOverview
        self.timeInfo = timeInfo
        self.showInControls = showInControls
        self.singleTile = singleTile

    @staticmethod
    def fromDict(d):
        layer = Layer(*[None] * 10)
        for a, b in d.iteritems():
            setattr(layer, a, b)
        layer.layer = findProjectLayerByName(layer.layer)
        return layer


def replaceInTemplate(template, values):
    path = os.path.join(os.path.dirname(__file__), "templates", template)
    with codecs.open(path, encoding="utf-8") as f:
        lines = f.readlines()
    s = "".join(lines)
    for name,value in values.iteritems():
        s = s.replace(name, value)
    return s

def exportLayers(layers, folder, progress, precision, crsid, forPreview):
    progress.setText("Writing local layer files")
    destCrs = QgsCoordinateReferenceSystem(crsid)
    layersFolder = os.path.join(folder, "data")
    QDir().mkpath(layersFolder)
    reducePrecision = re.compile(r"([0-9]+\.[0-9]{%s})([0-9]+)" % precision)
    removeSpaces = lambda txt:'"'.join( it if i%2 else ''.join(it.split())
                         for i,it in enumerate(txt.split('"')))
    ext = "js" if forPreview else "json"
    regexp = re.compile(r'"geometry":.*?null\}')
    for i, appLayer in enumerate(layers):
        layer = appLayer.layer
        if layer.type() == layer.VectorLayer and layer.providerType().lower() != "wfs":
            path = os.path.join(layersFolder, "lyr_%s.%s" % (safeName(layer.name()), ext))
            QgsVectorFileWriter.writeAsVectorFormat(layer,  path, "utf-8", destCrs, 'GeoJson')
            with codecs.open(path, encoding="utf-8") as f:
                lines = f.readlines()
            with codecs.open(path, "w", encoding="utf-8") as f:
                if forPreview:
                    f.write("%s_geojson_callback(" % safeName(layer.name()))
                for line in lines:
                    line = reducePrecision.sub(r"\1", line)
                    line = line.strip("\n\t ")
                    line = removeSpaces(line)
                    if layer.wkbType()==QGis.WKBMultiPoint:
                        line = line.replace("MultiPoint", "Point")
                        line = line.replace("[ [", "[")
                        line = line.replace("] ]", "]")
                        line = line.replace("[[", "[")
                        line = line.replace("]]", "]")
                    line = regexp.sub(r'"geometry":null', line)
                    f.write(line)
                if forPreview:
                    f.write(");")
        elif layer.type() == layer.RasterLayer:
            destFile = os.path.join(layersFolder, safeName(layer.name()) + ".png").replace("\\", "/")
            img = layer.previewAsImage(QSize(layer.width(),layer.height()))
            img.save(destFile)
        progress.setProgress(int(i*100.0/len(layers)))


def findLayerByName(name, layers):
    for layer in layers:
        if layer.layer.name() == name:
            return layer

def safeName(name):
    #TODO: we are assuming that at least one character is valid...
    validChars = '123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    return ''.join(c for c in name if c in validChars).lower()


def findProjectLayerByName(name):
    layers = QgsProject.instance().layerTreeRoot().findLayers()
    for layer in layers:
        mapLayer = layer.layer()
        if mapLayer.name() == name:
            return mapLayer


def run(f):
    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    try:
        return f()
    finally:
        QApplication.restoreOverrideCursor()

def getConnectAuthCfg():
    """try to get connect plugin auth configuration.
    """
    authcfg = None
    # check if Connect plugin is istalled
    try:
        qgis.utils.plugins["boundlessconnect"]
        from boundlessconnect.plugins import boundlessRepoName
        from pyplugin_installer.installer_data import reposGroup
    except:
        msg = "You need to log in via Connect plugin but it is not installed or enabled"
        raise Exception(msg)

    # check if auth setting is available in connect plugin
    settings = QSettings()
    settings.beginGroup(reposGroup)
    authcfg = settings.value(boundlessRepoName + '/authcfg', '')
    if not authcfg:
        msg = "You need to login via Connect plugin"
        raise Exception(msg)

    return authcfg

def getCredentialsFromAuthDb(authcfg):
    credentials = (None, None)
    if authcfg:
        authConfig = QgsAuthMethodConfig()
        if QgsAuthManager.instance().loadAuthenticationConfig(authcfg, authConfig, True):
            credentials = (authConfig.config('username'), authConfig.config('password'))

    return credentials

__cachedToken = None
def resetCachedToken():
    global __cachedToken
    __cachedToken = None

def getToken():
    """
    Function to get a access token from endpoint sending "custom" basic auth.
    Parameters

    The return value is a token string or Exception. This is cached and returned
    every call or request again if cache is empty
    """
    global __cachedToken
    if __cachedToken:
        return __cachedToken

    # start with a clean cache
    __cachedToken = None

    # get authcfg to point to saved credentials in QGIS Auth manager
    authcfg = getConnectAuthCfg()
    if not authcfg:
        raise Exception("Connect authcfg is empty")

    usr, pwd = getCredentialsFromAuthDb(authcfg)
    if not usr and not pwd:
        raise Exception("Cannot find stored credentials with authcfg = {}".format(authcfg))

    # prepare data for the token request
    httpAuth = base64.b64encode('{}:{}'.format(usr.strip(), pwd.strip())).decode("ascii")
    headers = {}
    headers["Authorization"] = "Basic {}".format(httpAuth)
    headers["Content-Type"] = "application/json"

    # request token in synchronous way => block GUI
    nam = NetworkAccessManager(debug=pluginSetting("logresponse"))
    try:
        res, resText = nam.request(authUrl(), method="GET", headers=headers)
    except Exception as e:
        if nam.http_call_result.status_code in [401, 403]:
            raise Exception("Permission denied")
        else:
            raise e

    # todo: check res code in case not authorization
    if not res.ok:
        raise Exception("Cannot get token: {}".format(res.reason))

    # parse token from resText
    resDict = json.loads(str(resText))
    try:
        __cachedToken = resDict["token"]
    except:
        pass

    if not __cachedToken:
        raise Exception("Cannot get authentication token")

    return __cachedToken

def sdkVersion():
    path = os.path.join(os.path.dirname(__file__), "package.json")
    with open(path) as f:
        package = json.load(f)
    return package["version"]

def checkEndpoint():
    return True

def isPermissionDenied(message=None):
	'''Check message if it contain NetworkAccessManager excetpion related to
	a permission denied.
	'''
	# TODO: better management of error code parsing delegating to utils or
	#       some NetworkAccessManager static method
	if not message:
		return False

	pattern = re.match(r'(.*)Network error #(\d+3)(.*)', message)
	if not pattern:
		return False

	try:
		errorCode = pattern.group(2)
		if errorCode in ['401', '403']:
			return True
	except:
		return False
