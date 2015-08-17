from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Analysis(WebAppWidget):

    _parameters = {"Add random points layer": False,
                  "Buffer": False,
                  "Extract selected features from layer": False,
                  "Aggregate": False,
                  "Density layer (heatmap)": False,
                  "Select within": False,
                  "Count features": False,
                  "Calculate line length": False,
                  "Nearest point": False,
                  }

    def write(self, appdef, folder, app, progress):
        allAnalysisTools = {"Add random points layer": "addRandomLayer()",
                         "Buffer": "buffer()",
                         "Extract selected features from layer": "extractSelected()",
                         "Aggregate": "aggregatePoints()",
                         "Density layer (heatmap)": "addDensityLayer()",
                         "Select within": "selectWithin()",
                         "Count features": "countFeatures()",
                         "Calculate line length": "lineLength()",
                         "Nearest point": "nearestPoint()"}
        analysisTools = []
        for toolName, tool in allAnalysisTools.iteritems():
            if self._parameters[toolName]:
                analysisTools.append([tool, toolName])
        if analysisTools:
            li = "\n".join(['<li><a onclick="runAlgorithm(new %s)" href="#">%s</a></li>' % (t[0], t[1]) for t in analysisTools])
            app.tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            Analysis <span class="caret"><span></a>
                            <ul class="dropdown-menu">
                              %s
                            </ul>
                          </li>''' % li)
            self.addScript("analysis.js", folder, app)
            self.addScript("turf.min.js", folder, app)
            self.addScript("bootbox.min.js", folder, app)


    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "analysis.png"))

    def description(self):
        return "Analysis"

    def checkProblems(self, appdef, problems):
        if not any(self._parameters.values()):
            problems.append("Analysis component has been added, but no analysis functionality has been selected for it.")