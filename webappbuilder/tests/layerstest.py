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
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_localpoints.js"))

    def testLocalLinesLayer(self):
        folder = createAppFromTestAppdef("locallines")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_locallines.js"))

    def testLocalPolygonsLayer(self):
        folder = createAppFromTestAppdef("localpolygons")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_localpolygons.js"))

    def testLocalRasterLayer(self):
        folder = createAppFromTestAppdef("localraster")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_localraster.js"))

    def testWMSLayer(self):
        folder = createAppFromTestAppdef("layerwms")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_wms.js"))

    def testWFSLayer(self):
        folder = createAppFromTestAppdef("layerwfs")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_wfs.js"))

    def testLayerGroup(self):
        folder = createAppFromTestAppdef("layergroup")
        styleFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(styleFile, "layers_layergroup.js"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(LayersTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

