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

def createApp(appdef):
	if not checkAppCanBeCreated():
		return
	QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
	try:
		importPostgis(appdef)
		publishGeoserver(appdef)
		writeOL(appdef)
		folder = appdef["Deploy"]["App path"]
		files = [os.path.join(folder, "layers/layers.js"), os.path.join(folder, "index.js")]
		for root, dirs, fs in os.walk(os.path.join(appdef["Deploy"]["App path"], "styles")):
			for f in fs:
				files.append(os.path.join(root, f))
		for path in files:
			beauty = jsbeautifier.beautify_file(path)
			with open(path, "w") as f :
				f.write(beauty)
	finally:
		QApplication.restoreOverrideCursor()

def checkAppCanBeCreated():
	return True

def importPostgis(appdef):
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
	for layer in appdef["Layers"]:
		if layer.method in [METHOD_WFS_POSTGIS, METHOD_WMS_POSTGIS]:
			if not schemaExists:
				connector.createSchema(schema)
				schemaExists = True
			importLayerIntoPostgis(layer.layer, host, port, username, password, dbname, schema,
								tablename = safeName(layer.layer.name())
								)
			print "Imported into PostGIS:" + layer.layer.name()

def importLayerIntoPostgis(layer, host, port, username, password, dbname, schema, tablename):
	extent = '{},{},{},{}'.format(
	        layer.extent().xMinimum(), layer.extent().xMaximum(),
	        layer.extent().yMinimum(), layer.extent().yMaximum())
	geomtypes = {QGis.WKBPoint: 3,
	             QGis.WKBLineString: 4,
	             QGis.WKBPolygon: 5,
	             QGis.WKBMultiPoint: 7,
	             QGis.WKBMultiLineString: 9,
	             QGis.WKBMultiPolygon: 8}
	geomtype = geomtypes.get(layer.wkbType(), 0)

	params = {ogr2ogr.INPUT_LAYER: layer,
	            ogr2ogr.DBNAME: dbname,
	            ogr2ogr.PORT : port,
	            ogr2ogr.HOST : host,
	            ogr2ogr.USER : username,
	            ogr2ogr.PASSWORD: password,
	            ogr2ogr.SCHEMA: schema,
	            ogr2ogr.GTYPE: geomtype,
	            ogr2ogr.TABLE: tablename,
	            ogr2ogr.S_SRS: layer.crs().authid(),
	            ogr2ogr.T_SRS: layer.crs().authid(),
	            ogr2ogr.OVERWRITE: True,
	            ogr2ogr.APPEND: False,
	            ogr2ogr.SPAT: extent
	            }
	alg = Processing.getAlgorithm("gdalogr:importvectorintopostgisdatabasenewconnection")
	for name, value in params.iteritems():
		param = alg.getParameterFromName(name)
		if param and param.setValue(value):
			continue
		output = alg.getOutputFromName(name)
		if output and output.setValue(value):
			continue
	AlgorithmExecutor.runalg(alg)

def publishGeoserver(appdef):
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
	for applayer in appdef["Layers"]:
		layer = applayer.layer
		if applayer.method != METHOD_FILE and applayer.method != METHOD_DIRECT:
			name = safeName(layer.name())
			sld = getGsCompatibleSld(layer)
			if sld is not None:
				catalog.create_style(name, sld, True)
			if layer.type() == layer.VectorLayer:
				if applayer.method == METHOD_WFS_POSTGIS:
					if store is None:
						store = catalog.create_datastore(dsName, workspace)
						store.connection_parameters.update(
							host=host, port=str(port), database=database, user=postgisUsername, schema=schema,
							passwd=postgisPassword, dbtype="postgis")
						catalog.save(store)
					catalog.publish_featuretype(name, store, layer.crs().authid())
				else:
					path = getDataFromLayer(layer)
					catalog.create_featurestore(name,
													path,
													workspace=workspace,
													overwrite=True)
			elif layer.type() == layer.RasterLayer:
				path = getDataFromLayer(layer)
				catalog.create_coveragestore(name,
				                          path,
				                          workspace=workspace,
				                          overwrite=True)
			print sld
			if sld is not None:
				publishing = catalog.get_layer(name)
				publishing.default_style = catalog.get_style(name)
				catalog.save(publishing)
			print "Published to GeoServer: " + layer.name()


def getDataFromLayer(layer):
	if layer.type() == layer.RasterLayer:
		data = exportRasterLayer(layer)
	else:
		filename = exportVectorLayer(layer)
		basename, extension = os.path.splitext(filename)
		data = {
		    'shp': basename + '.shp',
		    'shx': basename + '.shx',
		    'dbf': basename + '.dbf',
		    'prj': basename + '.prj'
		}
	return data

epsg3587 = QgsCoordinateReferenceSystem("EPSG:3857")

def exportVectorLayer(layer):
	settings = QSettings()
	systemEncoding = settings.value( "/UI/encoding", "System" )
	filename = unicode(layer.source())
	destFilename = unicode(layer.name())
	if not filename.lower().endswith("shp") or layer.crs().authid() != "EPSG:3857":

		output = tempFilenameInTempFolder(destFilename + ".shp")
		provider = layer.dataProvider()
		writer = QgsVectorFileWriter(output, systemEncoding, layer.pendingFields(), provider.geometryType(), epsg3587)
		for feat in layer.getFeatures():
			writer.addFeature(feat)
		del writer
		return output
	else:
		return filename

def exportRasterLayer(layer):
	if not unicode(layer.source()).lower().endswith("tif") or layer.crs().authid() != "EPSG:3857":
		filename = str(layer.name())
		output = tempFilenameInTempFolder(filename + ".tif")
		writer = QgsRasterFileWriter(output)
		writer.setOutputFormat("GTiff");
		writer.writeRaster(layer.pipe(), layer.width(), layer.height(), layer.extent(), epsg3587)
		del writer
		return output
	else:
		return unicode(layer.source())