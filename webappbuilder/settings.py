import os
import copy
from qgis.core import *
import importlib
from webbappwidget import WebAppWidget
import widgets
import glob
import inspect

import sys
sys.path.append('C:\Program Files\Brainwy\LiClipse 1.0.0\plugins\org.python.pydev_3.6.0.201406221719\pysrc')
from pydevd import *

def loadWidgets():
    _widgets = {}
    basePath = os.path.join(os.path.dirname(__file__), "widgets")
    widgetFolders = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for folder in widgetFolders:
        for f in glob.glob(folder + "/*.py"):
            moduleName = os.path.splitext(os.path.basename(f))[0]
            pkgName = os.path.basename(folder)
            module = importlib.import_module("." + moduleName, package="webappbuilder.widgets." + pkgName)
            for c in inspect.getmembers(module):
                if inspect.isclass(c[1]):
                    bases = [b.__name__ for b in c[1].__bases__]
                    if (c[1].__module__ == "webappbuilder.widgets.%s.%s" % (pkgName, moduleName)
                                and "WebAppWidget" in bases):
                        obj = c[1]()
                        _widgets[obj.name()] = obj

    return _widgets

def loadThemes():
    allCss = {}
    basePath = os.path.join(os.path.dirname(__file__), "themes")
    templates = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for template in templates:
        themeName = os.path.basename(template)
        path = os.path.join(template, themeName + ".css")
        with open(path) as f:
            allCss[themeName] = "".join(f.readlines())
    return allCss

def loadBaseLayers():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baselayers.txt")
    with open(path) as f:
        text = "".join(f.readlines())
    return splitElements(text)

def loadBaseOverlays():
    path = os.path.join(os.path.dirname(__file__), "baselayers", "baseoverlays.txt")
    with open(path) as f:
        text = "".join(f.readlines())
    return splitElements(text)

def splitElements(s):
    lines = s.splitlines()
    css = {}
    element = None
    for line in lines:
        if line.strip().startswith("/*"):
            element = line.strip()[2:-2]
            css[element] = []
        elif element is not None:
            css[element].append(line)
    for element in css:
        css[element] = "\n".join(css[element])
    return css

def joinElements(els):
    s = ""
    for el, css in els.iteritems():
        s += "\n\n/*%s*/\n" % el
        s += css
    return s

baseLayers = loadBaseLayers()
baseOverlays = loadBaseOverlays()
themes = loadThemes()
webAppWidgets = loadWidgets()

outputFolders = {}

overviewPanelBaseLayers = ["Use main map base layer"]
overviewPanelBaseLayers.extend(baseLayers.keys())


zoomLevels = list((str(i) for i in xrange(1,33)))
precisionLevels = list((str(i) for i in range(6)))
defaultAppSettings = {
                "Use layer scale dependent visibility": True,
                "Extent": ("Canvas extent", ("Canvas extent", "Fit to layers extent")),
                "Precision for GeoJSON export": ("2", precisionLevels),
                "Restrict to extent": False,
                "Max zoom level": ("32", zoomLevels),
                "Min zoom level": ("1", zoomLevels),
                "Zoom level when zooming to point feature": ("16", zoomLevels),
                "Show popups on hover": False,
                "App view CRS": "EPSG:3857",
                "Use view CRS for WFS connections": True,
                "Group base layers": True,
                "Minify JavaScript": False}



def initialize():
    #global widgetsParams
    global currentCss
    global appSettings
    for w in webAppWidgets.values():
        w.resetParameters()
    #widgetsParams = copy.deepcopy(defaultWidgetsParams)
    currentTheme = "basic" if "basic" in themes else themes.keys()[0]
    currentCss =  themes[currentTheme]
    appSettings = copy.deepcopy(defaultAppSettings)

initialize()