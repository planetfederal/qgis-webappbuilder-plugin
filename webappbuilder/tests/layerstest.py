# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import os

from webappbuilder.tests import utils


class LayersTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("layers")

    def testLocalPointsLayer(self):
        """Check that point layers processed correctly"""
        folder = utils.createAppFromTestAppdef("localpoints")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_localpoints.js"))

    def testLocalLinesLayer(self):
        """Check that line layers processed correctly"""
        folder = utils.createAppFromTestAppdef("locallines")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_locallines.js"))

    def testLocalPolygonsLayer(self):
        """Check that polygon layers processed correctly"""
        folder = utils.createAppFromTestAppdef("localpolygons")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_localpolygons.js"))

    def testLocalRasterLayer(self):
        """Check that raster layers processed correctly"""
        folder = utils.createAppFromTestAppdef("localraster")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_localraster.js"))

    def testWMSLayer(self):
        """Check that WMS layers processed correctly"""
        folder = utils.createAppFromTestAppdef("layerwms")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_wms.js"))

    #def testWFSLayer(self):
    #    """Check that WFS layers processed correctly"""
    #    folder = utils.createAppFromTestAppdef("layerwfs")
    #    appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
    #    self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_wfs.js"))

    def testLayerGroup(self):
        """Check that groups of layers processed correctly"""
        folder = utils.createAppFromTestAppdef("layergroup")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_layergroup.js"))

    def testMultipleBaseLayers(self):
        """Check that base and overlay layers processed correctly"""
        folder = utils.createAppFromTestAppdef("multiplebaselayers")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "layers_multiplebaselayers.js"))

    def testPopups(self):
        """Check that popups can be added"""
        folder = utils.createAppFromTestAppdef("popupsonhover")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.checkTextInFile(appFile, 'popupInfo: "<b>n</b>: [n]"'))

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(LayersTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
