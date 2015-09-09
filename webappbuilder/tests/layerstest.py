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
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_localpoints.js"))

    def testLocalLinesLayer(self):
        folder = createAppFromTestAppdef("locallines")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_locallines.js"))

    def testLocalPolygonsLayer(self):
        folder = createAppFromTestAppdef("localpolygons")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_localpolygons.js"))

    def testLocalRasterLayer(self):
        folder = createAppFromTestAppdef("localraster")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_localraster.js"))

    def testWMSLayer(self):
        folder = createAppFromTestAppdef("layerwms")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_wms.js"))

    def testWFSLayer(self):
        folder = createAppFromTestAppdef("layerwfs")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_wfs.js"))

    def testLayerGroup(self):
        folder = createAppFromTestAppdef("layergroup")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_layergroup.js"))

    def testMultipleBaseLayers(self):
        folder = createAppFromTestAppdef("multiplebaselayers")
        layersFile = os.path.join(folder, "layers", "layers.js")
        self.assertTrue(compareWithExpectedOutputFile(layersFile, "layers_multiplebaselayers.js"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(LayersTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

