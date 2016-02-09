from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Wfst(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('<ul className="pull-right"><BUTTON.DefaultButton onClick={this._toggleWFST.bind(this)} title="WFS-T">WFS-T</UI.DefaultButton></ul>')
        app.panels.append("<div id='wfst' ref='wfstPanel'><WFST map={map} /></div>")
        app.toolsjs.append('''React.createElement("ul", {className: 'pull-right'},
                                React.createElement(BUTTON.DefaultButton, {onClick: this._toggleWFST.bind(this), title: 'WFS-T'},
                                  'WFS-T'
                                )
                              )''')
        app.panelsjs.append(''' React.createElement("div", {id: 'wfst', ref: 'wfstPanel'},
                                      React.createElement(WFST, {map: map})
                                    )''')
        self.addReactComponent(app, "Edit")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "edit.png"))

    def description(self):
        return "WFS-T"