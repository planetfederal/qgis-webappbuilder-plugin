from PyQt4.Qt import QIcon, QDir
import os
from parameditor import ParametersEditorDialog
import inspect
import shutil

class WebAppWidget(object):

    _parameters = {}

    def __init__(self):
        self.defaultParameters = self._parameters.copy()

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "icons", "puzzle.png"))

    def name(self):
        return self.__class__.__name__.lower()

    def description(self):
        return "Base widget"

    def write(self, appdef, tools, panels, mappanels, scripts, scriptsBottom):
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
        self._parameters = self.defaultParameters

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
            with open(path) as f:
                text = f.read()
        else:
            text = "Help not available"
        html = "<h2>%s</h2><p>%s</p>" % (self.description(), text)
        return html

    def widgetHelpFiles(self):
        return []

    def checkProblems(self, appdef, problems):
        pass

    def copyToResources(self, name, folder):
        resourcesFolder = os.path.join(folder, "resources")
        if not QDir(resourcesFolder).exists():
            QDir().mkpath(resourcesFolder)
        f = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), name)
        shutil.copy2(f, resourcesFolder)

    def addScript(self, name, folder, app):
        self.copyToResources(name, folder)
        app.scripts.append('<script src="./resources/%s"></script>' % name)

    def addCss(self, name, folder, app):
        self.copyToResources(name, folder)
        app.scripts.append('<link href="./resources/%s" rel="stylesheet" type="text/css"/>' % name)
