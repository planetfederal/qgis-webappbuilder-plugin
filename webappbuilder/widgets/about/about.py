from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class AboutPanel(WebAppWidget):

    _parameters = {"content": "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>"}

    order = 0

    def write(self, appdef, folder, app, progress):
        theme = appdef["Settings"]["Theme"]
        content = self._parameters["content"].replace('\n', '<br>').replace('\r', '').replace("'", "&#39;")
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(Tab, {key:%i, value:%i, label:'About'},
                                    React.createElement("div", {id:'about-tab-panel', className:'about-tab-panel'},
                                        React.createElement("div", {dangerouslySetInnerHTML:{__html: '%s'}})
                                    )
                                )''' % (idx, idx, content))
        else:
            app.mappanels.append('''React.createElement("div", {id: 'about-panel', className:'about-panel'},
                                        React.createElement("a", {href:'#', id:'about-panel-closer',
                                            className:'about-panel-closer', onClick:this._hideAboutPanel.bind(this)},
                                              "X"
                                        ),
                                        React.createElement("div", {dangerouslySetInnerHTML:{__html: '%s'}})
                                    )''' %  content)



    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "about-panel.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "about-panel.png")

    def description(self):
        return "About"
