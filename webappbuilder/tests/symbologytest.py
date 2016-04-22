import unittest
import sys
import utils
import os
from utils import *


class SymbologyTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("symbology")

    def testPointsSymbology(self):
        folder = createAppFromTestAppdef("symbologypoints")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologypoints.js"))

    def testClusterSymbology(self):
        folder = createAppFromTestAppdef("symbologycluster")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologycluster.js"))

    def testLinesSymbology(self):
        folder = createAppFromTestAppdef("symbologylines")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologylines.js"))

    def testPolygonsSymbology(self):
        folder = createAppFromTestAppdef("symbologypolygons")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologypolygons.js"))

    def testSimpleLabelsSymbology(self):
        folder = createAppFromTestAppdef("symbologysimplelabels")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologysimplelabels.js"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SymbologyTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
