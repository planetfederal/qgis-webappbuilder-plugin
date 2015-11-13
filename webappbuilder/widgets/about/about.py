from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class AboutPanel(WebAppWidget):

    _parameters = {"content": "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>",
                    "isClosable": True}

    order = 0

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append(("<UI.Tab eventKey={%i} title='About'><div id='about-tab-panel' className='about-tab-panel'>"
                              + "%s</div></UI.Tab>") % (idx, self._parameters["content"]))
        else:
            closer = ('<a className="about-closer-icon" id="about-closer-icon" onClick="{this._toggleAboutPanel.bind(this)}">&times;</a>'
                     if self._parameters["isClosable"] else "")
            app.mappanels.append('''<div className="about-panel" id="about-panel">
                            %s
                            %s</div>''' % (closer, self._parameters["content"]))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "about-panel.png"))

    def description(self):
        return "About"