# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import sys
import utils
from webappbuilder.appcreator import checkAppCanBeCreated
from webappbuilder.tests.utils import testAppdef


class AppdefValidityTest(unittest.TestCase):

    def setUp(self):
        utils.loadTestProject()

    def testBaseLayerNot3857(self):
        """Test handling layers which are not in EPSG:3857"""
        problems = checkAppCanBeCreated(testAppdef("baselayernot3857"))
        self.assertEqual(0, len(problems))
        #self.assertTrue("Base layers can only be used if view CRS is EPSG:3857." in problems[0])

    def testUnsupportedSymbology(self):
        """Test detection of unsupported symbology"""
        problems = checkAppCanBeCreated(testAppdef("unsupportedsymbology"))
        self.assertEqual(1, len(problems))
        self.assertTrue("unsupported" in problems[0])

def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(AppdefValidityTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
