import os
import re
from appwriter import writeWebApp
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from db_manager.db_plugins.postgis.connector import PostGisDBConnector
from geoserver.catalog import Catalog
from utils import *
from sldadapter import getGsCompatibleSld
import jsbeautifier
from jsmin import jsmin
from json.encoder import JSONEncoder
import json
import requests
from settings import webAppWidgets

def createApp(appdef, deployData, folder, progress):
	if deployData:
		usesGeoServer = False
		usesPostgis = False
		layers = appdef["Layers"]
		for layer in layers:
			if layer.method in [METHOD_WFS_POSTGIS, METHOD_WMS_POSTGIS]:
				usesPostgis = True
				usesGeoServer = True
			elif layer.method in [METHOD_WFS, METHOD_WMS]:
				usesGeoServer = True
		if usesPostgis:
			importPostgis(appdef, progress)
		if usesGeoServer:
			publishGeoserver(appdef, progress)
	writeWebApp(appdef, folder, deployData, progress)

	projFile = QgsProject.instance().fileName()
	if projFile:
		appdefFile =  projFile + ".appdef"
		saveAppdef(appdef, appdefFile)


def checkAppCanBeCreated(appdef):
	viewCrs = appdef["Settings"]["App view CRS"]
	problems = []
	layers = appdef["Layers"]

	widgets = appdef["Widgets"].values()
	for w in widgets:
		w.checkProblems(appdef, problems)

	for applayer in layers:
		layer = applayer.layer
		if layer.providerType().lower() == "wms":
			if layer.crs().authid() != viewCrs:
				problems.append("Layer %s uses CRS %s. Reprojection is not supported for WMS services. "
						"This layer will probably not appear correctly in the web app"
						% (layer.name(), layer.crs().authid()))
			if applayer.popup != "":
				source = layer.source()
				url = re.search(r"url=(.*?)(?:&|$)", source).groups(0)[0] + "?REQUEST=GetCapabilities"
				r = requests.get(url, headers={"origin": "null"})
				if "access-control-allow-origin" not in r:
					problems.append("Server for layer %s is not allowed to accept cross-origin requests."
								" Popups might not work correctly for that layer."	% layer.name())
	if appdef["Base layers"] and viewCrs != "EPSG:3857":
		problems.append("Base layers can only be used if view CRS is EPSG:3857. "
					"They will not appear correctly if the web app uses a different CRS."
					"Your web app uses %s" % viewCrs)

	for applayer in layers:
		layer = applayer.layer
		if layer.type() != layer.VectorLayer or applayer.method == METHOD_WMS:
			continue
		renderer = applayer.layer.rendererV2()
		if not isinstance(renderer, (QgsSingleSymbolRendererV2, QgsCategorizedSymbolRendererV2,
									QgsGraduatedSymbolRendererV2)):
			problems.append("Symbology used by layer %s includes unsupported elements. "
						"This layer will not be correctly styled in the web app."
						% layer.name())


	#TODO: check that layers using time attributes are not published using WMS

	hasTimeInfo = False
	for applayer in layers:
		if applayer.timeInfo is not None:
			hasTimeInfo = True
			break;

	if hasTimeInfo and "timeline" not in appdef["Widgets"]:
		problems.append("There are layers with time information, but timeline widget is not used.")

	if not hasTimeInfo and "timeline" in appdef["Widgets"]:
		problems.append("Timeline widget is used but there are no layers with time information")

	return problems


def importPostgis(appdef, progress):
	progress.setText("Importing into PostGIS")
	progress.setProgress(0)
	host = appdef["Deploy"]["PostGIS host"]
	port = appdef["Deploy"]["PostGIS port"]
	username = appdef["Deploy"]["PostGIS username"]
	password = appdef["Deploy"]["PostGIS password"]
	dbname = appdef["Deploy"]["PostGIS database"]
	schema = appdef["Deploy"]["PostGIS schema"]
	uri = QgsDataSourceURI()
	uri.setConnection(host, port, dbname, username, password)
	connector = PostGisDBConnector(uri)
	schemas = connector.getSchemas()
	schemaExists = schema in [s[1] for s in schemas]
	for i, layer in enumerate(appdef["Layers"]):
		if layer.method in [METHOD_WFS_POSTGIS, METHOD_WMS_POSTGIS]:
			if not schemaExists:
				connector.createSchema(schema)
				schemaExists = True
			tables = connector.getTables(schema=schema)
			tablename = safeName(layer.layer.name())
			tableExists = tablename in [t[1] for t in tables]
			if tableExists:
				connector.deleteTable([schema, tablename])
				importLayerIntoPostgis(layer.layer, host, port, username, password,
								dbname, schema, tablename)
		progress.setProgress(int(i*100.0/len(appdef["Layers"])))

def importLayerIntoPostgis(layer, host, port, username, password, dbname, schema, tablename):
	pk = "id"
	geom = "geom"
	providerName = "postgres"

	uri = QgsDataSourceURI()
	uri.setConnection(host, str(port), dbname, username, self.geodb.password)
	uri.setDataSource(schema, tablename, geom, "", pk)

	ret, errMsg = QgsVectorLayerImport.importLayer(layer, uri.uri(), providerName, layer.crs(), False, False, options)
	if ret != 0:
		raise Exception("Could not import layer '%s': %s" % (layer.name(), errMsg))



def publishGeoserver(appdef, progress):
	viewCrs = appdef["Settings"]["App view CRS"]
	usesGeoServer = False
	for applayer in appdef["Layers"]:
		if applayer.method != METHOD_FILE:
			if applayer.layer.type() == applayer.layer.VectorLayer and applayer.layer.providerType().lower() != "wfs":
				usesGeoServer = True
	if not usesGeoServer:
		return
	progress.setText("Publishing to GeoServer")
	progress.setProgress(0)
	geoserverUrl = appdef["Deploy"]["GeoServer url"] + "/rest"
	geoserverPassword = appdef["Deploy"]["GeoServer password"]
	geoserverUsername = appdef["Deploy"]["GeoServer username"]
	workspaceName = appdef["Deploy"]["GeoServer workspace"]
	dsName = "ds_" + workspaceName
	host = appdef["Deploy"]["PostGIS host"]
	port = appdef["Deploy"]["PostGIS port"]
	postgisUsername = appdef["Deploy"]["PostGIS username"]
	postgisPassword = appdef["Deploy"]["PostGIS password"]
	database = appdef["Deploy"]["PostGIS database"]
	schema = appdef["Deploy"]["PostGIS schema"]
	catalog = Catalog(geoserverUrl, geoserverUsername, geoserverPassword)
	workspace = catalog.get_workspace(workspaceName)
	if workspace is None:
		workspace = catalog.create_workspace(workspaceName, workspaceName)
	try:
		store = catalog.get_store(dsName, workspace)
		resources = store.get_resources()
		for resource in resources:
			layers = catalog.get_layers(resource)
			for layer in layers:
				catalog.delete(layer)
			catalog.delete(resource)
		catalog.delete(store)
	except Exception:
		pass
	store = None
	for i, applayer in enumerate(appdef["Layers"]):
		layer = applayer.layer
		if applayer.method != METHOD_FILE and applayer.method != METHOD_DIRECT:
			name = safeName(layer.name())
			sld, icons = getGsCompatibleSld(layer)
			if sld is not None:
				catalog.create_style(name, sld, True)
				uploadIcons(icons, geoserverUsername, geoserverPassword, catalog.gs_base_url)
			if layer.type() == layer.VectorLayer:
				if applayer.method == METHOD_WFS_POSTGIS or applayer.method == METHOD_WMS_POSTGIS:
					if store is None:
						store = catalog.create_datastore(dsName, workspace)
						store.connection_parameters.update(
							host=host, port=str(port), database=database, user=postgisUsername, schema=schema,
							passwd=postgisPassword, dbtype="postgis")
						catalog.save(store)
					catalog.publish_featuretype(name, store, layer.crs().authid())
				else:
					path = getDataFromLayer(layer, viewCrs)
					catalog.create_featurestore(name,
													path,
													workspace=workspace,
													overwrite=True)
				gslayer = catalog.get_layer(name)
				r = gslayer.resource
				r.dirty['srs'] = viewCrs
				catalog.save(r)
			elif layer.type() == layer.RasterLayer:
				path = getDataFromLayer(layer, viewCrs)
				catalog.create_coveragestore(name,
				                          path,
				                          workspace=workspace,
				                          overwrite=True)
			if sld is not None:
				publishing = catalog.get_layer(name)
				publishing.default_style = catalog.get_style(name)
				catalog.save(publishing)
		progress.setProgress(int((i+1)*100.0/len(appdef["Layers"])))



def uploadIcons(icons, url, geoserverUsername, geoserverPassword):
	url = url + "app/api/icons"
	for icon in icons:
		files = {'file': (icon[1], icon[2])}
		r = requests.post(url, files=files, auth=(geoserverUsername, geoserverPassword))
		try:
			r.raise_for_status()
		except Exception, e:
			raise Exception ("Error uploading SVG icon to GeoServer:\n" + str(e))
		break

def getDataFromLayer(layer, crsid):
	if layer.type() == layer.RasterLayer:
		data = exportRasterLayer(layer, crsid)
	else:
		filename = exportVectorLayer(layer, crsid)
		basename, extension = os.path.splitext(filename)
		data = {
		    'shp': basename + '.shp',
		    'shx': basename + '.shx',
		    'dbf': basename + '.dbf',
		    'prj': basename + '.prj'
		}
	return data

def exportVectorLayer(layer, crsid):
	destCrs = QgsCoordinateReferenceSystem(crsid)
	settings = QSettings()
	systemEncoding = settings.value( "/UI/encoding", "System" )
	filename = unicode(layer.source())
	destFilename = unicode(layer.name())
	if not filename.lower().endswith("shp") or layer.crs().authid() != crsid:
		output = tempFilenameInTempFolder(destFilename + ".shp")
		provider = layer.dataProvider()
		writer = QgsVectorFileWriter(output, systemEncoding, layer.pendingFields(), provider.geometryType(), destCrs)
		crsTransform = QgsCoordinateTransform(layer.crs(), destCrs)
		outFeat = QgsFeature()
		for f in layer.getFeatures():
			geom = f.geometry()
			geom.transform(crsTransform)
			outFeat.setGeometry(geom)
			outFeat.setAttributes(f.attributes())
			writer.addFeature(outFeat)
		del writer
		return output
	else:
		return filename

def exportRasterLayer(layer, crsid):
	destCrs = QgsCoordinateReferenceSystem(crsid)
	if not unicode(layer.source()).lower().endswith("tif") or layer.crs().authid() != crsid:
		filename = str(layer.name())
		output = tempFilenameInTempFolder(filename + ".tif")
		writer = QgsRasterFileWriter(output)
		writer.setOutputFormat("GTiff");
		writer.writeRaster(layer.pipe(), layer.width(), layer.height(), layer.extent(), destCrs)
		del writer
		return output
	else:
		return unicode(layer.source())


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
		toSave["Widgets"][wName] = {"Parameters":w.parameters(), "Css": w.css()}
	layers = []
	for layer in toSave["Layers"]:
		layer.layer = layer.layer.name()
		layers.append(layer)
	toSave["Layers"] = layers
	with open(filename, "w") as f:
		f.write(json.dumps(toSave, sort_keys=True, indent=4, cls=DefaultEncoder))

def loadAppdef(filename):
	try:
		with open(filename) as f:
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
		obj.setCss(props["Css"])
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






