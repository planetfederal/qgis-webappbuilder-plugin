from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class AboutPanel(WebAppWidget):

    _parameters = {"content": "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>"}

    order = 0

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        content = self._parameters["content"].replace('\n', '<br>').replace('\r', '')
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(Tab, {value:%i, label:'About'},
                                    React.createElement("div", {id:'about-tab-panel', className:'about-tab-panel'},
                                        React.createElement("div", {dangerouslySetInnerHTML:{__html: '%s'}})
                                    )
                                )''' % (idx, content))
        else:
            app.mappanels.append('''React.createElement("div", {id: 'about-panel', className:'about-panel'},
                                        React.createElement("div", {dangerouslySetInnerHTML:{__html: '%s'}})
                                    )''' %  content)



    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "about-panel.png"))

    def description(self):
        return "About"
