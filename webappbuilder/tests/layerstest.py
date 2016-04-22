import unittest
import sys
import utils
import os
from utils import *


class LayersTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("layers")

    def testLocalPointsLayer(self):
        folder = createAppFromTestAppdef("localpoints")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_localpoints.js"))

    def testLocalLinesLayer(self):
        folder = createAppFromTestAppdef("locallines")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_locallines.js"))

    def testLocalPolygonsLayer(self):
        folder = createAppFromTestAppdef("localpolygons")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_localpolygons.js"))

    def testLocalRasterLayer(self):
        folder = createAppFromTestAppdef("localraster")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_localraster.js"))

    def testWMSLayer(self):
        folder = createAppFromTestAppdef("layerwms")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_wms.js"))

    def testWFSLayer(self):
        folder = createAppFromTestAppdef("layerwfs")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_wfs.js"))

    def testLayerGroup(self):
        folder = createAppFromTestAppdef("layergroup")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_layergroup.js"))

    def testMultipleBaseLayers(self):
        folder = createAppFromTestAppdef("multiplebaselayers")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "layers_multiplebaselayers.js"))

    def testPopups(self):
        folder = createAppFromTestAppdef("popupsonhover")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(checkTextInFile(appFile, 'popupInfo: "<b>n</b>: [n]"'))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(LayersTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

