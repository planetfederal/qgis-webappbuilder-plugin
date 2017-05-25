# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import re
import codecs
import traceback
from pubsub import pub
from appwriter import writeWebApp, stopWritingWebApp
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from utils import *
import utils
import jsbeautifier
from jsmin import jsmin
from json.encoder import JSONEncoder
import json
import requests
from settings import webAppWidgets
import viewer
import xml.etree.ElementTree as ET
import importlib
from exp2js import is_expression_supported

class VersionMismatchError(Exception):
	pass

# need a global where to store parameters to be used in PyPubSub listener
# because PyPubSub does not support persistence of lambda functions
__appdef = None
def endWriteWebAppListener(success, reason):
	from pubsub import pub
	pub.unsubscribe(endWriteWebAppListener , utils.topics.endWriteWebApp)

	if success:
		from PyQt4.QtCore import *
		projFile = QgsProject.instance().fileName()
		if projFile:
			appdefFile =  projFile + ".appdef"
			saveAppdef(__appdef, appdefFile)

	# communicate end of function
	pub.sendMessage(utils.topics.endFunction, success=success, reason=reason)

def stopAppCreation():
	stopWritingWebApp()

def createApp(appdef, folder, forPreview, progress):
	# save to global __appdef to patch a PyPubSub limitation that does not allow
	# to register a lambda function as listener (weak reference is unregistered
	# as soon the lambda is out of scope)
	global __appdef
	__appdef = appdef

	viewer.shutdown()
	pub.subscribe(endWriteWebAppListener , utils.topics.endWriteWebApp)
	try:
		writeWebApp(appdef, folder, forPreview, progress)
	except Exception as ex:
		endWriteWebAppListener(False, traceback.format_exc())

def checkSDKServerVersion():
	if not utils.checkEndpoint():
		return "Provided endpoint does not seem to be a valid SDK service endpoint"
	localVersion = utils.sdkVersion()

	token = utils.getToken()


	headers = {}
	headers["authorization"] = "Bearer {}".format(token)

	nam = NetworkAccessManager(debug=pluginSetting("logresponse"))
	try:
		resp, text = nam.request(wabVersionUrl(), headers=headers)
	except Exception as e:
		# check if 401/403 => probably token expired
		permissionDenied = utils.isPermissionDenied( str(e) )
		if not permissionDenied:
			raise e
		else:
			# renew token and try again
			utils.resetCachedToken()
			token = utils.getToken()

			# retry call
			headers["authorization"] = "Bearer {}".format(token)
			try:
				resp, text = nam.request(wabVersionUrl(), headers=headers)
			except Exception as e:
				# check if 401/403 => probably token expired
				permissionDenied = utils.isPermissionDenied( str(e) )
				if not permissionDenied:
					raise e
				else:
					raise Exception("Permission denied with current Connect credentials")

	remoteVersion = json.loads(text)["boundless-sdk"]
	if localVersion != remoteVersion:
		raise VersionMismatchError("The server SDK version (%s) is different from the expected version (%s)" % (remoteVersion, localVersion))


def checkAppCanBeCreated(appdef, forPreview=False):
	##viewCrs = appdef["Settings"]["App view CRS"]
	jsonp = appdef["Settings"]["Use JSONP for WFS connections"]
	problems = []
	layers = appdef["Layers"]

	widgets = appdef["Widgets"].values()
	for w in widgets:
		w.checkProblems(appdef, problems, forPreview)

	themeModule = importlib.import_module("webappbuilder.themes." + appdef["Settings"]["Theme"])
	themeModule.checkProblems(appdef, problems)

	def getSize(lyr):
		ptsInFeature = 1 if lyr.geometryType() == QGis.Point else 10 #quick estimate...
		return lyr.featureCount() * (ptsInFeature + lyr.pendingFields().size())

	MAXSIZE = 30000
	for applayer in layers:
		if applayer.layer.type() == applayer.layer.VectorLayer and applayer.layer.providerType().lower() != "wfs":
			if getSize(applayer.layer) > MAXSIZE:
				problems.append("Layer %s might be too big for being loaded directly from a file." % applayer.layer.name())

	for applayer in layers:
		layer = applayer.layer
		if layer.providerType().lower() == "wms":
			try:
				source = layer.source()
				url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0] + "?REQUEST=GetCapabilities"
				r = run(lambda: requests.get(url, headers={"origin": "null"}))
				cors = r.headers.get("Access-Control-Allow-Origin", "").lower()
				if cors not in ["null", "*"]:
					problems.append("Server for layer %s is not allowed to accept cross-origin requests."
								" Popups and printing might not work correctly for that layer."	% layer.name())
			except:
				QgsMessageLog.logMessage("Warning: cannot verify cross-origin configuration for layer '%s'."
                            % layer.name(), level=QgsMessageLog.WARNING)

	for applayer in layers:
		layer = applayer.layer
		if layer.providerType().lower() == "wfs":
			datasourceUri = QgsDataSourceURI(layer.source())
			url = datasourceUri.param("url") or layer.source().split("?")[0]
			url = url + "?service=WFS&version=1.1.0&REQUEST=GetCapabilities"
			try:
				if jsonp:
					r = run(lambda: requests.get(url))
					if "text/javascript" not in r.text:
						problems.append("Server for layer %s does not support JSONP. WFS layer won't be correctly loaded in Web App."
									% layer.name())
				else:
					r = run(lambda: requests.get(url, headers={"origin": "null"}))
					cors = r.headers.get("Access-Control-Allow-Origin", "").lower()
					if cors not in ["null", "*"]:
						problems.append("Server for layer %s is not allowed to accept cross-origin requests." % layer.name())
			except:
				QgsMessageLog.logMessage("Warning: cannot verify if WFS layer server has the required configuration. Layer: '%s'."
                            % layer.name(), level=QgsMessageLog.WARNING)

		if layer.type() != layer.VectorLayer:
			continue
		renderer = applayer.layer.rendererV2()
		allowed = [QgsSingleSymbolRendererV2, QgsCategorizedSymbolRendererV2,
					QgsGraduatedSymbolRendererV2, QgsHeatmapRenderer, QgsRuleBasedRendererV2]
		try:
			allowed.append(QgsNullSymbolRenderer)
		except:
			pass
		if not isinstance(renderer, tuple(allowed)):
			problems.append("Symbology used by layer %s includes unsupported elements."
							"Only single symbol, categorized, graduated, heatmap and rule-based renderers are supported."
						"This layer will not be correctly styled in the web app."
						% layer.name())
		if isinstance(renderer, QgsRuleBasedRendererV2):
			rules = renderer.rootRule().children()
			for	rule in rules:
				expr = rule.filterExpression()
				unsupported = is_expression_supported(expr)
				if unsupported:
					problems.append("The expression '%s' has unsupported functions: %s"
								% (expr, ", ".join(unsupported)))

		if str(layer.customProperty("labeling/enabled")).lower() == "true":
			if unicode(layer.customProperty("labeling/isExpression")).lower() == "true":
				expr = layer.customProperty("labeling/fieldName")
				unsupported = is_expression_supported(expr)
				if unsupported:
					problems.append("The expression '%s' has unsupported functions: %s"
								% (expr, ", ".join(unsupported)))


	#TODO: check that layers using time attributes are not published using WMS

	hasTimeInfo = False
	for applayer in layers:
		if applayer.timeInfo is not None:
			hasTimeInfo = True
			break;

	if hasTimeInfo and "timeline" not in appdef["Widgets"]:
		problems.append("There are layers with time information, but timeline widget is not used.")

	if "timeline" in appdef["Widgets"]:
		for applayer in layers:
			layer = applayer.layer
			if layer.providerType().lower() == "wms":
				try:
					source = layer.source()
					url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0]
					layernames = re.search(r"layers=(.*?)(?:&|$)", source).groups(0)[0]
					r = requests.get(url + "?service=WMS&request=GetCapabilities")
					root = ET.fromstring(re.sub('\\sxmlns="[^"]+"', '', r.text))
					for layerElement in root.iter('Layer'):
						name = layerElement.find("Name").text
						if name == layernames:
							# look for discrete values
							time = layerElement.find('Extent')
							if time is not None:
								applayer.timeInfo = time
								hasTimeInfo = True
							# look for interval values
							time = layerElement.find('Dimension')
							if time is not None and time.attrib['name'] == 'time':
								applayer.timeInfo = '"{}"'.format(time.text)
								hasTimeInfo = True

				except:
					#we swallow error, since this is not a vital info to add, so the app can still be created.
					pass

		if not hasTimeInfo:
			problems.append("Timeline widget is used but there are no layers with time information")

	return problems


class DefaultEncoder(JSONEncoder):
	def default(self, o):
		return o.__dict__

def saveAppdef(appdef, filename):
	toSave = {k:v for k,v in appdef.iteritems() if k != "Widgets"}
	for group in toSave["Groups"]:
		toSave["Groups"][group]["layers"] = [layer.name()
								for layer in toSave["Groups"][group]["layers"]]
	toSave["Widgets"] = {}
	for wName, w in appdef["Widgets"].iteritems():
		toSave["Widgets"][wName] = {"Parameters":w.parameters()}
	layers = []
	for layer in toSave["Layers"]:
		layer.layer = layer.layer.name()
		layers.append(layer)
	toSave["Layers"] = layers
	with codecs.open(filename, "w", encoding="utf-8") as f:
		f.write(json.dumps(toSave, sort_keys=True, indent=4, cls=DefaultEncoder))

def loadAppdef(filename):
	try:
		with codecs.open(filename, encoding="utf-8") as f:
			data = json.load(f)
		return data
	except Exception, e:
		return None

'''
Converts a appdef coming from an appdef file (a dict with only string objects)
into a dict that contains layers, widgets, etc, so it can be passed to the methods
that create the webapp based on it. It modifies values of objects in the appdef dict,
based on the content of the current project.
'''
def processAppdef(appdef):
	newWidgets = {}
	for w, props in appdef["Widgets"].iteritems():
		obj = webAppWidgets[w]
		obj.setParameters(props["Parameters"])
		newWidgets[w] = obj
	appdef["Widgets"] = newWidgets
	newLayers = []
	for layer in appdef["Layers"]:
		newLayers.append(Layer.fromDict(layer))
	appdef["Layers"] = newLayers
	newGroups = {}
	for groupName, group in appdef["Groups"].iteritems():
		newGroups[groupName] = {}
		groupLayers = []
		for layer in group["layers"]:
			groupLayers.append(findProjectLayerByName(layer))
		newGroups[groupName]["layers"] = groupLayers
		newGroups[groupName]["showContent"] = group["showContent"]
		newGroups[groupName]["isGroupExpanded"] = group.get("isGroupExpanded", True)
	appdef["Groups"] = newGroups

warningIcon = os.path.join(os.path.dirname(__file__), "icons", "warning.png")

class AppDefProblemsDialog(QDialog):

	def __init__(self, problems, parent=None):
		super(AppDefProblemsDialog, self).__init__(parent)
		self.title = "Wrong Web App Definition"
		self.msg = ("The following problems were found in your app definition:\n"
					"Do you want to create the web app?")
		self.problems = problems
		self.ok = False
		self.initGui()


	def initGui(self):
		self.setWindowTitle(self.title)
		layout = QVBoxLayout()

		msgLabel = QLabel(self.msg)
		msgLabel.setWordWrap(True)
		layout.addWidget(msgLabel)

		class MyBrowser(QTextBrowser):
			def loadResource(self, type_, name):
				return None
		self.textBrowser = MyBrowser()
		problems = ['<li><img src="%s"/> &nbsp; %s</li>' % (warningIcon, p) for p in self.problems]
		text = '<html><ul>%s</ul></html>' % "".join(problems)
		self.textBrowser.setHtml(text)
		layout.addWidget(self.textBrowser)
		buttonBox = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
		layout.addWidget(buttonBox)
		self.setLayout(layout)

		self.connect(buttonBox, SIGNAL("rejected()"), self.close)
		self.connect(buttonBox, SIGNAL("accepted()"), self.okPressed)

		self.setMinimumWidth(400)
		self.setMinimumHeight(400)
		self.resize(500, 400)

	def okPressed(self):
		self.ok = True
		self.close()
