# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import sys
import unittest

from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.settings import webAppWidgets
from webappbuilder.tests import utils

widgets = ["aboutpanel", "addlayer", "attributestable", "attribution",
           "bookmarks", "charttool", "edit", "exportasimage", "fullscreen",
           "geocoding", "geolocation", "help", "homebutton", "layerslist",
           "legend", "links", "loadingpanel", "measuretools", "mouseposition",
           "northarrow", "overviewmap", "print", "query", "refresh", "scalebar",
           "selectiontools", "timeline", "wfst", "zoomcontrols", "zoomslider"]

class WidgetsTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject("bakeries")

    def testWidgetsCorrectlyLoaded(self):
        """Check that all widgets loaded"""
        for w in widgets:
            self.assertTrue(w in webAppWidgets), 'Widget {} not loaded'.format(w)

    def testChartWidgetNotAdeed(self):
        """Check that chart widget is not generated if it is not configured"""
        folder = utils.createAppFromTestAppdef("chartwidget")
        appFile = os.path.join(folder, "webapp", "app_prebuilt.js")
        self.assertTrue(utils.compareWithExpectedOutputFile(appFile, "nochartwidget.js", True))


def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(WidgetsTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
