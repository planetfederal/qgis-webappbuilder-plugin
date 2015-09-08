import unittest
import sys
import utils
from webappbuilder.appcreator import checkAppCanBeCreated
import os
from utils import *
from webappbuilder.settings import webAppWidgets

widgetFiles = {"layerslist": ['resources/bootbox.min.js', 'resources/filtrex.js', 'resources/layerslist.css', 'resources/layerslist.js'],
                "geolocation":['resources/geolocation.css', 'resources/geolocation.js'],
                "zoomslider":['resources/zoomslider.css'],
                "mouseposition":['resources/mouseposition.css'],
                "links":[],
                "exportasimage":['resources/exportasimage.js'],
                "selectiontools":['resources/selectiontools.js'],
                "homebutton":['resources/homebutton.css', 'resources/homebutton.js'],
                "query":['resources/filtrex.js', 'resources/query.css', 'resources/query.js'],
                "bookmarks":[],
                "addlayer":['resources/addlayer.js', 'resources/bootbox.min.js'],
                "help":['help/help.html'],
                "fullscreen":['resources/fullscreen.css'],
                "charttool":['resources/c3.min.css', 'resources/c3.min.js', 'resources/charts.css', 'resources/charts.js', 'resources/d3.min.js'],
                "zoomcontrols":['resources/zoomcontrols.css'],
                "timeline":['resources/timeline.css', 'resources/timeline.js'],
                "print":['resources/bootbox.min.js', 'resources/jspdf.min.js', 'resources/print.js'],
                "geocoding":['resources/geocoding.css', 'resources/geocoding.js', 'resources/marker.png'],
                "attributestable":['resources/attributestable.css', 'resources/attributestable.js'],
                "attribution":['resources/attribution.css'],
                "measuretools":['resources/measure.js', 'resources/measuretools.css'],
                "scalebar":['resources/scalebar.css'],
                "legend":['resources/legend.css', 'resources/legend.js'],
                "threedview":['resources/3dview.css', 'resources/cesium-control.js', 'resources/Cesium.js', 'resources/exports.js', 'resources/ol3cesium.js', 'resources/ol3cesium.js.map'],
                "edit":['resources/bootbox.min.js', 'resources/edit.css', 'resources/edit.js'],
                "analysis":[],
                "northarrow":['resources/northarrow.css'],
                "overviewmap":['resources/overviewmap.css'],
                "aboutpanel":['resources/about.css']}

class WidgetsTest(unittest.TestCase):

    def testFilesCorrectlyCopied(self):
        appdef = testAppdef("empty")
        missing = []
        for w in webAppWidgets:
            widget = webAppWidgets[w]
            widget.resetParameters()
            appdef["Widgets"] = {w:widget}
            folder = tempFolderInTempFolder()
            writeWebApp(appdef, folder, True, SilentProgress())
            for f in widgetFiles[w]:
                path = os.path.join(folder, f)
                if not os.path.exists(path):
                    missing.append(w)
                    break
        self.assertTrue(len(missing) == 0, "Missing this files:\n"+ "\n".join(missing))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(WidgetsTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

