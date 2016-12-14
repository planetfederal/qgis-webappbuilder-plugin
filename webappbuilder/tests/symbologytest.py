# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os

from webappbuilder.tests import utils


class SymbologyTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("symbology")

    def testPointsSymbology(self):
        """Check that point symbology exported correctly"""
        folder = utils.createAppFromTestAppdef("symbologypoints")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "symbologypoints.js"))

    def testClusterSymbology(self):
        """Check that point clustering works correctly"""
        folder = utils.createAppFromTestAppdef("symbologycluster")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "symbologycluster.js"))

    def testLinesSymbology(self):
        """Check that line symbology exported correctly"""
        folder = utils.createAppFromTestAppdef("symbologylines")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "symbologylines.js"))

    def testPolygonsSymbology(self):
        """Check that polygon symbology exported correctly"""
        folder = utils.createAppFromTestAppdef("symbologypolygons")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "symbologypolygons.js"))

    def testSimpleLabelsSymbology(self):
        """Check that labels exported correctly"""
        folder = utils.createAppFromTestAppdef("symbologysimplelabels")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "symbologysimplelabels.js"))


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SymbologyTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
