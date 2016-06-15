# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utils
import os

from qgis.core import QGis

from utils import *


class SymbologyTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("symbology")

    def testPointsSymbology(self):
        """Check that point symbology exported correctly"""
        folder = createAppFromTestAppdef("symbologypoints")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        if QGis.QGIS_VERSION_INT < 21500:
            self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologypoints-2.14.js"))
        else:
            self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologypoints.js"))

    def testClusterSymbology(self):
        """Check that point clustering works correctly"""
        folder = createAppFromTestAppdef("symbologycluster")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        if QGis.QGIS_VERSION_INT < 21500:
            self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologycluster-2.14.js"))
        else:
            self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologycluster.js"))

    def testLinesSymbology(self):
        """Check that line symbology exported correctly"""
        folder = createAppFromTestAppdef("symbologylines")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologylines.js"))

    def testPolygonsSymbology(self):
        """Check that polygon symbology exported correctly"""
        folder = createAppFromTestAppdef("symbologypolygons")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologypolygons.js"))

    def testSimpleLabelsSymbology(self):
        """Check that labels exported correctly"""
        folder = createAppFromTestAppdef("symbologysimplelabels")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(compareWithExpectedOutputFile(appFile, "symbologysimplelabels.js"))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SymbologyTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
