from PyQt4.Qt import QIcon, QDir
import os
from parameditor import ParametersEditorDialog
import inspect
import shutil
from texteditor import TextEditorDialog, CSS

class WebAppWidget(object):

    _parameters = {}
    _css = ""

    def __init__(self):
        path = inspect.getfile(self.__class__)
        path = ".".join(path.split(".")[:-1]) + ".css"
        if os.path.exists(path):
            with open(path) as f:
                s = f.read()
                self._css = s

        self.defaultParameters = self._parameters.copy()
        self.defaultCss = self._css

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "icons", "puzzle.png"))

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

    def editCss(self):
        dlg = TextEditorDialog(self._css, CSS)
        dlg.exec_()
        self._css = dlg.text

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

    def resetCss(self):
        self._css = self.defaultCss

    def setCss(self, css):
        self._css = css

    def css(self):
        return self._css

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

    def addScript(self, name, folder, app, toBottom = False):
        self.copyToResources(name, folder)
        if toBottom:
            app.scriptsBottom.append('<script src="./resources/%s"></script>' % name)
        else:
            app.scripts.append('<script src="./resources/%s"></script>' % name)

    def addCss(self, name, folder, app):
        if os.path.basename(inspect.getfile(self.__class__)).split(".")[0] == name.split(".")[0]:
            resourcesFolder = os.path.join(folder, "resources")
            if not QDir(resourcesFolder).exists():
                QDir().mkpath(resourcesFolder)
            path = os.path.join(resourcesFolder, name)
            with open(path, "w") as f:
                f.write(self._css)
        else:
            self.copyToResources(name, folder)
        app.scripts.append('<link href="./resources/%s" rel="stylesheet" type="text/css"/>' % name)

    def addImport(self, name, fromJsx, app):
        app.imports.append("from %s import '%s'" % (name, fromJsx))

    def addReactRender(self, s, app):
        app.react.append("React.render(%s)" % s)


