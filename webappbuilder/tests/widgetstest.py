# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import sys
import unittest

from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.settings import webAppWidgets
from webappbuilder.tests.utils import *

widgets = ["aboutpanel", "addlayer", "attributestable", "attribution",
           "bookmarks", "charttool", "edit", "exportasimage", "fullscreen",
           "geocoding", "geolocation", "help", "homebutton", "layerslist",
           "legend", "links", "loadingpanel", "measuretools", "mouseposition",
           "northarrow", "overviewmap", "print", "query", "refresh", "scalebar",
           "selectiontools", "timeline", "wfst", "zoomcontrols", "zoomslider"]

class WidgetsTest(unittest.TestCase):

    def testWidgetsCorrectlyLoaded(self):
        """Check that all widgets loaded"""
        for w in widgets:
            self.assertTrue(w in webAppWidgets), 'Widget {} not loaded'.format(w)

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(WidgetsTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
