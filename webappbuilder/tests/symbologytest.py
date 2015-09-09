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
        styleFile = os.path.join(folder,"styles", "points.js")
        self.assertTrue(compareFiles(styleFile, "symbologypoints.js"))

    def testClusterSymbology(self):
        folder = createAppFromTestAppdef("symbologycluster")
        styleFile = os.path.join(folder,"styles", "points.js")
        self.assertTrue(compareFiles(styleFile, "symbologycluster.js"))

    def testLinesSymbology(self):
        folder = createAppFromTestAppdef("symbologylines")
        styleFile = os.path.join(folder,"styles", "lines.js")
        self.assertTrue(compareFiles(styleFile, "symbologylines.js"))

    def testPolygonsSymbology(self):
        folder = createAppFromTestAppdef("symbologypolygons")
        styleFile = os.path.join(folder,"styles", "polygons.js")
        self.assertTrue(compareFiles(styleFile, "symbologypolygons.js"))

    def testSimpleLabelsSymbology(self):
        folder = createAppFromTestAppdef("symbologysimplelabels")
        styleFile = os.path.join(folder,"styles", "simplelabels.js")
        self.assertTrue(compareFiles(styleFile, "symbologysimplelabels.js"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SymbologyTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())

