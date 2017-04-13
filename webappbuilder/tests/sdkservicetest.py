# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from webappbuilder.appwriter import *
from qgiscommons.files import *
import unittest
import sys
import shutil
import os
from webappbuilder import utils
from pubsub import pub
from PyQt4.QtCore import QEventLoop
try:
    from qgis.core import QGis
except ImportError:
    from qgis.core import Qgis as QGis


class Progress():
    def setText(_, text):
        pass
    def setProgress(_, i):
        pass
    def oscillate(_):
        pass

_loop = None
_correctResponse = False

def endAppSDKificationListener(success, reason):
    from pubsub import pub
    pub.unsubscribe(endAppSDKificationListener, utils.topics.endAppSDKification)
    _loop.exit()
    global _correctResponse
    _correctResponse = not success


class SdkServiceTest(unittest.TestCase):

    def testServerSDKErrors(self):
        dst = os.path.join(tempFolderInTempFolder("webappbuilder"), "webapp")
        shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "wrong_app"), dst)
        pub.subscribe(endAppSDKificationListener, utils.topics.endAppSDKification)
        try:
            global _loop
            _loop = QEventLoop()
            appSDKification(dst, Progress())
            _loop.exec_(flags = QEventLoop.ExcludeUserInputEvents)
            self.assertTrue(_correctResponse)
        except Exception as e:
            self.fail(str(e))



def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(SdkServiceTest, 'test'))
    return suite

def run_tests():
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite())
