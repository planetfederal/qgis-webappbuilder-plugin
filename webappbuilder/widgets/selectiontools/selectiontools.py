from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class SelectionTools(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        pullRight = "" if len(app.tools) else "pullRight"
        app.tools.append("<ul className='pull-right' id='toolbar-select'><Select toggleGroup='navigation' map={map} %s/></ul>" % pullRight)
        app.tools.append("<ul className='pull-right' id='toolbar-navigation'><BUTTON.DefaultButton title='Switch to map navigation (pan and zoom)' onClick={this._navigationFunc}>Navigation</BUTTON.DefaultButton></ul>")
        app.toolsjs.append('''React.createElement("ul", {id:'toolbar-select', className:'pull-right'},
                                    React.createElement(Select, {toggleGroup:'navigation', map:map})
                                  )''')
        app.toolsjs.append('''React.createElement("ul", {id:'toolbar-navigation', className:'pull-right'},
                                    React.createElement(BUTTON.DefaultButton, {title:'Switch to map navigation (pan and zoom)', onClick:this._navigationFunc},
                                        "Navigation"
                                    )
                                  )''')

        self.addReactComponent(app, "Select")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "selection-tool.png"))

    def description(self):
        return "Selection"