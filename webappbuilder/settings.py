# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from builtins import str
from builtins import range
import os
import copy
from qgis.core import *
import importlib
import glob
import inspect
import codecs


def loadWidgets():
    _widgets = {}
    basePath = os.path.join(os.path.dirname(__file__), "widgets")
    widgetFolders = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for folder in widgetFolders:
        for f in glob.glob(folder + "/*.py"):
            moduleName = os.path.splitext(os.path.basename(f))[0]
            pkgName = os.path.basename(folder)
            module = importlib.import_module("webappbuilder.widgets.%s.%s" % (pkgName, moduleName))
            for c in inspect.getmembers(module):
                if inspect.isclass(c[1]):
                    bases = [b.__name__ for b in c[1].__bases__]
                    if (c[1].__module__ == "webappbuilder.widgets.%s.%s" % (pkgName, moduleName)
                                and "WebAppWidget" in bases):
                        obj = c[1]()
                        _widgets[obj.name()] = obj

    return _widgets


def loadBaseLayers():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baselayers.txt")
    with codecs.open(path, encoding="utf-8") as f:
        text = "".join(f.readlines())
    return splitElements(text)

def loadBaseOverlays():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baseoverlays.txt")
    with codecs.open(path, encoding="utf-8") as f:
        text = "".join(f.readlines())
    return splitElements(text)

def splitElements(s):
    lines = s.splitlines()
    elements = {}
    element = None
    for line in lines:
        if line.strip().startswith("/*"):
            element = line.strip()[2:-2]
            elements[element] = []
        elif element is not None:
            elements[element].append(line)
    for element in elements:
        elements[element] = "\n".join(elements[element])
    return elements


baseLayers = loadBaseLayers()
baseOverlays = loadBaseOverlays()
webAppWidgets = loadWidgets()

zoomLevels = list((str(i) for i in range(1,33)))
precisionLevels = list((str(i) for i in range(6)))
defaultAppSettings = {
                "Use layer scale dependent visibility": True,
                "Extent": ("Canvas extent", ("Canvas extent", "Fit to layers extent")),
                "Precision for GeoJSON export": ("2", precisionLevels),
                "Restrict to extent": False,
                "Max zoom level": ("32", zoomLevels),
                "Min zoom level": ("1", zoomLevels),
                "Show popups on hover": False,
                "App view CRS": "EPSG:3857",
                "Use view CRS for WFS connections": True,
                "Use JSONP for WFS connections": False,
                "Group base layers": True,
                "Minify JavaScript": False,
                "Add permalink functionality": True,
                "Open hyperlinks in": ("Same window/tab", ("Same window/tab", "New window/tab"))}



def initialize():
    global appSettings
    for w in list(webAppWidgets.values()):
        w.resetParameters()
    appSettings = copy.deepcopy(defaultAppSettings)

initialize()
