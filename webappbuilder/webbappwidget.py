# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from PyQt4.Qt import QIcon, QDir
import os
from parameditor import ParametersEditorDialog
import inspect
import shutil
import codecs

class WebAppWidget(object):

    BUTTON_AREA_NO_BUTTON, BUTTON_AREA_LEFT, BUTTON_AREA_RIGHT = 0,1,2

    buttonIndex = 100
    buttonArea = BUTTON_AREA_NO_BUTTON
    buttonHeight = 40

    _parameters = {}
    order = 100

    def __init__(self):
        import copy
        self.defaultParameters = copy.deepcopy(self._parameters)

    def buttonAreaForTheme(self, theme):
        return self.buttonArea

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
            for k, v, in params.iteritems():
                if isinstance(v, tuple):
                    params[k] = v[0]
            return params
        else:
            return {}

    def resetParameters(self):
        import copy
        self._parameters = copy.deepcopy(self.defaultParameters)

    def setParameters(self, params):
        for paramName, value in params.iteritems():
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

    def checkProblems(self, appdef, problems, forPreview):
        pass

    def copyToResources(self, name, folder):
        resourcesFolder = os.path.join(folder, "resources")
        if not QDir(resourcesFolder).exists():
            QDir().mkpath(resourcesFolder)
        f = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), name)
        if os.path.exists(f):
            shutil.copy2(f, resourcesFolder)

    def addReactComponent(self, app, component):
        app.imports.append("import %(comp)s from '@boundlessgeo/sdk/components/%(comp)s';"
                           % {"comp": component})
