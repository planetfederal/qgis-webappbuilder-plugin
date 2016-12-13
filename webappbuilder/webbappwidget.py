from builtins import object
# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import inspect
import shutil
import codecs

from qgis.PyQt.QtCore import QDir
from qgis.PyQt.QtGui import QIcon
from webappbuilder.parameditor import ParametersEditorDialog

class WebAppWidget(object):

    _parameters = {}
    order = 100

    def __init__(self):
        import copy
        self.defaultParameters = copy.deepcopy(self._parameters)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "icons", "puzzle.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "icons", "puzzle.png")

    def name(self):
        return self.__class__.__name__.lower()

    def description(self):
        return "Base widget"

    def write(self, appdef, tools, app, progress):
        pass

    def configure(self):
        dlg = ParametersEditorDialog(self._parameters)
        dlg.exec_()
        self._parameters = dlg.params

    def parameters(self):
        if self._parameters:
            params = self._parameters.copy()
            for k, v, in list(params.items()):
                if isinstance(v, tuple):
                    params[k] = v[0]
            return params
        else:
            return {}

    def resetParameters(self):
        import copy
        self._parameters = copy.deepcopy(self.defaultParameters)

    def setParameters(self, params):
        for paramName, value in list(params.items()):
            if paramName in self._parameters:
                if isinstance(self._parameters[paramName], tuple):
                    self._parameters[paramName] = (value, self._parameters[paramName][1])
                else:
                    self._parameters[paramName] = value

    def widgetHelp(self):
        path = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), "description.html")
        if os.path.exists(path):
            with codecs.open(path, encoding="utf-8") as f:
                text = f.read()
            return text

    def widgetHelpFiles(self):
        basePath = os.path.dirname(inspect.getfile(self.__class__))
        return [os.path.join(basePath,o) for o in os.listdir(basePath)
                if o.startswith("help") and o.endswith(".png")]

    def checkProblems(self, appdef, problems):
        pass

    def copyToResources(self, name, folder):
        resourcesFolder = os.path.join(folder, "resources")
        if not QDir(resourcesFolder).exists():
            QDir().mkpath(resourcesFolder)
        f = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), name)
        if os.path.exists(f):
            shutil.copy2(f, resourcesFolder)

    def addReactComponent(self, app, component):
        app.imports.append("import %(comp)s from 'boundless-sdk/js/components/%(comp)s.jsx';"
                           % {"comp": component})
