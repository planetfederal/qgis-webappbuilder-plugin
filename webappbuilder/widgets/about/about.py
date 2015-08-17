from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class AboutPanel(WebAppWidget):

    _parameters = {"content": "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>",
                    "isClosable": True,
                    "showNavBarLink": True}

    def write(self, appdef, folder, app, progress):
        closer = ('<a class="closer-icon" id="closer-icon" onclick="toggleAboutPanel(false)">&times;</a>'
                 if self._parameters["isClosable"] else "")
        app.mappanels.append('''<div class="about-panel" id="about-panel">
                        %s
                        %s</div>''' % (closer, self._parameters["content"]))
        if self._parameters["showNavBarLink"]:
            app.tools.append('<li><a onclick="toggleAboutPanel(true)" href="#" id="about-panel-link">About</a></li>')

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "about-panel.png"))

    def description(self):
        return "About"