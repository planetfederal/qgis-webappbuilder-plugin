# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import unittest
import webbrowser
import os
import settingstest
import widgetstest
import appdefvaliditytest
import symbologytest
import layerstest
import sdkservicetest
from webappbuilder.tests.utils import (loadTestProject, createAppFromTestAppdef,
                                       openWAB, closeWAB, testAppdef, _setWrongSdkEndpoint,
                                       _resetSdkEndpoint, widgets,
                                       setNetworkTimeout, resetNetworkTimeout,
                                       getWABDialog, hideWAB)
from qgis.utils import iface
from PyQt4.QtTest import QTest
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import Qt

try:
    from qgis.core import QGis
except ImportError:
    from qgis.core import Qgis as QGis

webAppFolder = None

def functionalTests():
    # create TestCase instance to use Assert methods
    tc = unittest.TestCase('__init__')

    try:
        from qgistester.test import Test
        from qgistester.utils import layerFromName
    except:
        return []

    def _createWebApp(n, checkApp=False, preview=True):
        global webAppFolder
        webAppFolder = createAppFromTestAppdef(n, checkApp, preview)

    def _test(n):
        test = Test("Verify '%s' tutorial" % n)
        test.addStep("Setting up project", lambda: loadTestProject(n))
        test.addStep("Creating web app", lambda: _createWebApp(n))
        test.addStep("Verify web app in browser", prestep=lambda: webbrowser.open_new(
                    "file:///" + webAppFolder.replace("\\","/") + "/webapp/index_debug.html"))
        return test
    tests = [_test("bakeries"), _test("schools"), _test("fires")]

    appdefFolder = os.path.join(os.path.dirname(__file__), "data")


    def _testWidget(n, preview):
        sPreview = "(Preview)" if preview else ""
        test = Test("Verify '%s' widget %s" % (n, sPreview))
        test.addStep("Setting up project", lambda: loadTestProject("widgets"))
        test.addStep("Creating web app", lambda: _createWebApp(n, preview=preview))
        test.addStep("Verify web app in browser", prestep=lambda: webbrowser.open_new(
                    "file:///" + webAppFolder.replace("\\","/") + "/webapp/index_debug.html"))
        return test

    for w in widgets:
        for i in ["", "2", "3"]:
            f = os.path.join(appdefFolder, "%s%s.appdef" % (w, i))
            if os.path.exists(f):
                for preview in [True, False]:
                    tests.append(_testWidget(w, preview))

    unconfiguredBookmarksTest = Test("Verify bookmarks widget cannot be used if no bookmarks defined")
    unconfiguredBookmarksTest.addStep("Load project", lambda: loadTestProject())
    unconfiguredBookmarksTest.addStep("Open WAB", lambda: openWAB())
    unconfiguredBookmarksTest.addStep("Try to create an app with the bookmarks widget, without configuring it to add bookmarks.\n"
                         "Verify it shows a warning.")
    unconfiguredBookmarksTest.setCleanup(closeWAB)
    tests.append(unconfiguredBookmarksTest)

    unsupportedSymbologyTest = Test("Verify warning for unsupported symbology")
    unsupportedSymbologyTest.addStep("Load project", lambda: loadTestProject())
    unsupportedSymbologyTest.addStep("Open WAB", openWAB)
    unsupportedSymbologyTest.addStep("Click on 'Preview'. Verify a warning about unsupported symbology is shown.\n"
                         "Verify it shows a warning.")
    unsupportedSymbologyTest.setCleanup(closeWAB)
    tests.append(unsupportedSymbologyTest)

    wrongLogoTest = Test("Verify warning for wrong logo file")
    wrongLogoTest.addStep("Load project", lambda: loadTestProject())
    wrongLogoTest.addStep("Open WAB", openWAB)
    wrongLogoTest.addStep("Enter 'wrong' in the logo textbox and click on 'Preview'."
                                     "The logo texbox should get a yellow background.")
    wrongLogoTest.setCleanup(closeWAB)
    tests.append(wrongLogoTest)


    nodataTest = Test("Verify that NODATA values are transparent")
    nodataTest.addStep("Load project", lambda: loadTestProject("nodata"))
    nodataTest.addStep("Creating web app", lambda: _createWebApp("nodata"))
    nodataTest.addStep("Verify web app in browser. NODATA values should be transparent. "
                       "<b>NOTE</b> don't use Chrome/Chromium to check this web app they "
                       "have bug and it might not work as expected. Use Firefox or another browser.",
                       prestep=lambda: webbrowser.open_new(
                             "file:///" + webAppFolder.replace("\\","/") + "/webapp/index_debug.html"))
    tests.append(nodataTest)



    createEmpyAppTest = Test("Verify creating an app with no layers")
    createEmpyAppTest.addStep("Load project", iface.newProject)
    createEmpyAppTest.addStep("Open WAB", lambda: openWAB())
    createEmpyAppTest.addStep("Create an app preview and check it is correctly created")
    createEmpyAppTest.setCleanup(closeWAB)
    tests.append(createEmpyAppTest)

    wrongEndpointTest = Test("Verify wrong SDK service URL")
    wrongEndpointTest.addStep("Load project", iface.newProject)
    wrongEndpointTest.addStep("Load project", _setWrongSdkEndpoint)
    wrongEndpointTest.addStep("Open WAB", lambda: openWAB())
    wrongEndpointTest.addStep("Try to create an app preview and check it complains of a wrong URL")
    wrongEndpointTest.setCleanup(_resetSdkEndpoint)
    tests.append(wrongEndpointTest)

    wmsTimeinfoTest = Test("Verify that spatio-temporal WMS layers supported")
    wmsTimeinfoTest.addStep("Load project", lambda: loadTestProject("wms-timeinfo-interval"))
    wmsTimeinfoTest.addStep("Creating web app", lambda: _createWebApp("wms-timeinfo-interval", checkApp=True))
    wmsTimeinfoTest.addStep("Verify web app in browser.", prestep=lambda: webbrowser.open_new(
                             "file:///" + webAppFolder.replace("\\","/") + "/webapp/index_debug.html"))
    tests.append(wmsTimeinfoTest )

    try:
        from boundlessconnect.tests.testerplugin import _startConectPlugin
        denyCompilationTest = Test("Verify deny compilation for invalid Connect credentials")
        denyCompilationTest.addStep("Reset project", iface.newProject)
        denyCompilationTest.addStep('Enter invalid Connect credentials and accept dialog by pressing "Login" button.\n'
                                'Check that Connect shows Warning message complaining about only open access permissions.'
                                'Close error message by pressing "Yes" button.',
                        prestep=lambda: _startConectPlugin(), isVerifyStep=True)
        denyCompilationTest.addStep("Open WAB", lambda: openWAB())
        denyCompilationTest.addStep("Create an EMPTY app and check it complains of a permission denied")
        denyCompilationTest.setCleanup(closeWAB)
        tests.append(denyCompilationTest)
        localTimeoutCompilationTest = Test("Verfiy compilation timeout due to local settings")
        localTimeoutCompilationTest.addStep("Reset project", iface.newProject)
        localTimeoutCompilationTest.addStep('Enter EnterpriseTestDesktop Connect credentials and accept dialog by pressing "Login" button.\n'
                                    'Check that Connect is logged showing EnterpriseTestDesktop@boundlessgeo.com in the bottom',
                            prestep=lambda: _startConectPlugin(), isVerifyStep=True)
        localTimeoutCompilationTest.addStep("Open WAB", lambda: openWAB())
        localTimeoutCompilationTest.addStep("Setting timeout", lambda: setNetworkTimeout(value=3000))
        localTimeoutCompilationTest.addStep("Create an EMPTY app and check it complains of network timeout", isVerifyStep=True)
        localTimeoutCompilationTest.addStep("Close WAB", closeWAB)
        localTimeoutCompilationTest.setCleanup(resetNetworkTimeout)
        tests.append(localTimeoutCompilationTest)

        successCompilationTest = Test("Verfiy successful compilation with EnterpriseTestDesktop")
        successCompilationTest.addStep("Reset project", iface.newProject)
        successCompilationTest.addStep('Enter EnterpriseTestDesktop Connect credentials and accept dialog by pressing "Login" button.\n'
                                    'Check that Connect is logged showing EnterpriseTestDesktop@boundlessgeo.com in the bottom',
                            prestep=lambda: _startConectPlugin(), isVerifyStep=True)
        successCompilationTest.addStep("Open WAB", lambda: openWAB())
        successCompilationTest.addStep("Create an EMPTY app and check it successfully ends", isVerifyStep=True)
        successCompilationTest.setCleanup(closeWAB)
        tests.append(successCompilationTest)

        # test stopCompilationTest
        def checkStartoStopButton(text=None):
            dlg = getWABDialog()
            tc.assertEqual(dlg.buttonCreateOrStopApp.text(), text)

        def clickStopButton(after=5000):
            QTest.qWait(after)
            dlg = getWABDialog()
            QTest.mouseClick(dlg.buttonCreateOrStopApp, Qt.LeftButton)

        stopCompilationTest = Test("Verify stop compilation with EnterpriseTestDesktop user")
        stopCompilationTest.addStep("Reset project", iface.newProject)
        stopCompilationTest.addStep('Enter EnterpriseTestDesktop Connect credentials and accept dialog by pressing "Login" button.\n'
                                    'Check that Connect is logged showing EnterpriseTestDesktop@boundlessgeo.com in the bottom',
                            prestep=lambda: _startConectPlugin(), isVerifyStep=True)
        stopCompilationTest.addStep("Open WAB", lambda: openWAB())
        stopCompilationTest.addStep("Create an EMPTY app and start compilation, then click on next step!")
        stopCompilationTest.addStep("Verify if stop button is set", lambda: checkStartoStopButton(text='Stop') )
        stopCompilationTest.addStep("Click stop", lambda: clickStopButton(after=1000) )
        stopCompilationTest.addStep("Verify if StartApp button is set", lambda: checkStartoStopButton(text='CreateApp (Beta)') )
        stopCompilationTest.setCleanup(closeWAB)
        tests.append(stopCompilationTest)
    except ImportError:
        pass

    return tests


def unitTests():
    _tests = []
    _tests.extend(settingstest.suite())
    _tests.extend(widgetstest.suite())
    _tests.extend(appdefvaliditytest.suite())
    _tests.extend(layerstest.suite())
    _tests.extend(sdkservicetest.suite())
    return _tests
