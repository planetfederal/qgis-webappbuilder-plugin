import os
import sys
import unittest

from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.settings import webAppWidgets
from webappbuilder.tests.utils import *

widgetFiles = {"threedview":['resources/3dview.css', 'resources/cesium-control.js', 'resources/Cesium.js', 'resources/exports.js', 'resources/ol3cesium.js', 'resources/ol3cesium.js.map'],
               "aboutpanel":['resources/about.css'],
               "addlayer":['resources/addlayer.js', 'resources/bootbox.min.js'],
               "attributestable":['resources/attributestable.css', 'resources/attributestable.js'],
               "attribution":['resources/attribution.css'],
               "bookmarks":[],
               "charttool":['resources/c3.min.css', 'resources/c3.min.js', 'resources/charts.css', 'resources/charts.js', 'resources/d3.min.js'],
               "edit":['resources/bootbox.min.js', 'resources/edit.css', 'resources/edit.js'],
               "exportasimage":['resources/exportasimage.js'],
               "fullscreen":['resources/fullscreen.css'],
               "geocoding":['resources/geocoding.css', 'resources/geocoding.js', 'resources/marker.png'],
               "geolocation":['resources/geolocation.css', 'resources/geolocation.js'],
               "help":['help/help.html'],
               "homebutton":['resources/homebutton.css', 'resources/homebutton.js'],
               "layerslist": ['resources/bootbox.min.js', 'resources/filtrex.js', 'resources/layerslist.css', 'resources/layerslist.js'],
               "legend":['resources/legend.css', 'resources/legend.js'],
               "links":[],
               "loadingpanel":[],
               "measuretools":['resources/measure.js', 'resources/measuretools.css'],
               "mouseposition":['resources/mouseposition.css'],
               "northarrow":['resources/northarrow.css'],
               "overviewmap":['resources/overviewmap.css'],
               "print":['resources/bootbox.min.js', 'resources/jspdf.min.js', 'resources/print.js'],
               "query":['resources/filtrex.js', 'resources/query.css', 'resources/query.js'],
               "refresh":[],
               "scalebar":['resources/scalebar.css'],
               "selectiontools":['resources/selectiontools.js'],
               "timeline":['resources/timeline.css', 'resources/timeline.js'],
               "wfst":[],
               "zoomcontrols":['resources/zoomcontrols.css'],
               "zoomslider":['resources/zoomslider.css']}


class WidgetsTest(unittest.TestCase):

    def testWidgetsCorrectlyLoaded(self):
        """Check that all widgets loaded"""
        for w in widgetFiles:
            self.assertTrue(w in webAppWidgets), 'Widget {} not loaded'.format(w)

    #~ def testFilesCorrectlyCopied(self):
        #~ appdef = testAppdef("empty")
        #~ missing = []
        #~ for w in webAppWidgets:
            #~ widget = webAppWidgets[w]
            #~ widget.resetParameters()
            #~ appdef["Widgets"] = {w:widget}
            #~ folder = tempFolderInTempFolder()
            #~ writeWebApp(appdef, folder, True, True, SilentProgress())
            #~ print 'WIDGET', w
            #~ print widgetFiles[w]
            #~ for f in widgetFiles[w]:
                #~ path = os.path.join(folder, f)
                #~ if not os.path.exists(path):
                    #~ missing.append(w)
                    #~ break
        #~ self.assertTrue(len(missing) == 0, "Missing this files:\n"+ "\n".join(missing))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(WidgetsTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

