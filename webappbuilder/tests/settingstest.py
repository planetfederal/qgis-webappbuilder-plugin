import unittest
import sys
import utils
import os
from utils import *


class SettingsTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("settings")

    def testViewCrs(self):
        folder = createAppFromTestAppdef("viewcrs")
        outputFile = os.path.join(folder, "index.js")
        self.assertTrue(checkTextInFile(outputFile, "EPSG:23030"))

    def testCanvasExtent(self):
        folder = createAppFromTestAppdef("canvasextent")
        outputFile = os.path.join(folder, "index.js")
        #can't check canvas extent, since it depends on screen config, so we chek it doesn't use layer one
        self.assertFalse(checkTextInFile(outputFile, "[55659.745397, 55660.451865, 1057535.162536, 1062414.311268]"))

    def testLayersExtent(self):
        folder = createAppFromTestAppdef("layersextent")
        outputFile = os.path.join(folder, "index.js")
        self.assertTrue(checkTextInFile(outputFile, "[55659.745397, 55660.451865, 1057535.162536, 1062414.311268]"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SettingsTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

