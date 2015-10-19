from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class LayersList(WebAppWidget):

    _parameters = {"tipLabel": "Layers",
                    "showOpacity": False,
                    "showZoomTo": False,
                    "showDownload": False,
                    "allowReordering": False,
                    "allowFiltering": True,
                    "expandOnHover": True}

    def write(self, appdef, folder, app, progress):
        def p(name):
            return str(self._parameters[name]).lower()
        app.panels.append(("<div id='layerlist'><LayerList showOpacity={%s} showDownload={%s}"
                           "showGroupContent={true} showZoomTo={%s} allowReordering={%s} "
                           "allowFiltering={%s} map={map}/></div>")
                            % (p("showOpacity"),p("showDownload"), p("showZoomTo"),
                               p("allowReordering"), p("allowFiltering")))
        app.imports.append("import LayerList from './components/LayerList.jsx';")
    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "layer-list.png"))

    def description(self):
        return "Layers list"
