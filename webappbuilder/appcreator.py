import os
from olwriter import writeOL
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from processing.core.Processing import Processing
from processing.gui import AlgorithmExecutor
from processing.algs.gdal.ogr2ogrtopostgis import Ogr2OgrToPostGis as ogr2ogr
from db_manager.db_plugins.postgis.connector import PostGisDBConnector
from geoserver.catalog import Catalog
from utils import *
from sldadapter import getGsCompatibleSld
import jsbeautifier
from json.encoder import JSONEncoder
import json
import utils

class WrongAppDefinitionException(Exception):
	pass

def createApp(appdef, deployData, folder, progress):
	if deployData:
		usesGeoServer = False
		usesPostgis = False
		layers = appdef["Layers"]
		for layer in layers:
			if layer.method in [utils.METHOD_WFS_POSTGIS, utils.METHOD_WMS_POSTGIS]:
				usesPostgis = True
				usesGeoServer = True
			elif layer.method in [utils.METHOD_WFS, utils.METHOD_WMS]:
				usesGeoServer = True
		if usesPostgis:
			importPostgis(appdef, progress)
		if usesGeoServer:
			publishGeoserver(appdef, progress)
	writeOL(appdef, folder, deployData, progress)
	files = [os.path.join(folder, "layers/layers.js"), os.path.join(folder, "index.js")]
	for root, dirs, fs in os.walk(os.path.join(folder, "styles")):
		for f in fs:
			if f.endswith("js"):
				files.append(os.path.join(root, f))
	for path in files:
		try:
			beauty = jsbeautifier.beautify_file(path)
			with open(path, "w") as f:
				f.write(beauty)
		except:
			pass #jsbeautifier gives some random errors sometimes due to imports
	projFile = QgsProject.instance().fileName()
	if projFile:
		appdefFile =  projFile + ".appdef"
		saveAppdef(appdef, appdefFile)

def findLayerByName(name, layers):
	for layer in layers:
		if layer.layer.name() == name:
			return layer

def checkAppCanBeCreated(appdef):
	viewCrs = appdef["Settings"]["App view CRS"]
	problems = []
	if "Chart tool" in appdef["Widgets"]:
		layers = appdef["Layers"]
		charts = appdef["Widgets"]["Chart tool"]["charts"]
		if len(charts) == 0:
			problems.append("Chart tool added, but no charts have been defined. "
						"You should configure the chart tool and define at least one chart")
		if "Selection tools" not in appdef["Widgets"]:
			problems.append("Chart tool added, but the web app has no selection tools. "
						"Charts are created based on selected features, so you should add selection "
						"tools to the web app, to allow the user selecting features in the map")
		for name, chart in charts.iteritems():
			layer = findLayerByName(chart["layer"], layers)
			if layer is None:
				problems.append("Chart tool %s uses a layer (%s) that is not added to web app" % (name, chart["layer"]))
			if not layer.allowSelection:
				problems.append(("Chart tool %s uses a layer (%s) that does not allow selection. " +
							"Selection should be enabled for that layer.") % (name, chart["layer"]))

	if "Bookmarks" in appdef["Widgets"]:
		if len(appdef["Widgets"]["Bookmarks"]["bookmarks"]) == 0:
			problems.append("Bookmarks widget added, but no bookmarks have been defined"
						"You should configure the bookmars widget and define at least one bookmark")

	for applayer in appdef["Layers"]:
		layer = applayer.layer
		if layer.providerType().lower() == "wms" and layer.crs().authid() != viewCrs:
			problems.append("Layer %s uses CRS %s. Reprojection is not supported for WMS services. "
						"This layer will probably not appear correctly in the web app"
						% (layer.name(), layer.crs().authid()))

	if appdef["Base layers"] and viewCrs != "EPSG:3857":
		problems.append("Base layers can only be used if view CRS is EPSG:3857. "
					"They will not appear correctly if the web app uses a different CRS."
					"Your web app uses %s" % viewCrs)

	return problems


def importPostgis(appdef, progress):
	progress.setText("Importing into PostGIS (1/3)")
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
	progress.setText("Publishing to GeoServer (2/3)")
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
			sld = getGsCompatibleSld(layer)
			if sld is not None:
				catalog.create_style(name, sld, True)
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
		progress.setProgress(int(i*100.0/len(appdef["Layers"])))


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
	toSave = {k:v for k,v in appdef.iteritems()}
	for group in toSave["Groups"]:
		toSave["Groups"][group] = [layer.name() for layer in toSave["Groups"][group]]
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
		#self.textBrowser.connect(self.textBrowser, QtCore.SIGNAL("anchorClicked(const QUrl&)"), self.linkClicked)
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

