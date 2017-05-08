from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class LayersList(WebAppWidget):

    buttonIndex = 1
    buttonArea = WebAppWidget.BUTTON_AREA_RIGHT
    cssName = "layerlist"

    _parameters = {"tipLabel": "Layers",
                    "showOpacity": False,
                    "showZoomTo": False,
                    "showDownload": False,
                    "allowReordering": False,
                    "allowFiltering": True,
                    "allowStyling": True,
                    "showUpload": True,
                    "showTable": True,
                    "includeLegend": True,
                    "showNew": True,
                    "downloadFormat": ("GeoJSON", ("GeoJSON", "KML", "GPX"))}

    def write(self, appdef, folder, app, progress):
        self.addReactComponent(app, "LayerList")
        def p(name):
            return str(self._parameters[name]).lower()
        theme = appdef["Settings"]["Theme"]
        if theme == "tabbed":
            idx = len(app.tabs) + 1
            app.tabs.append('''React.createElement(Tab,{key:%i, value:%i, label:"Layer list"},
                                 React.createElement("div",{id: "layerlist"},
                                    React.createElement(LayerList, {showOpacity:%s, showDownload:%s,
                                        inlineDialogs: true,
                                        showGroupContent:true, showZoomTo:%s, allowReordering:%s,
                                        allowFiltering:%s, tipLabel:'%s',
                                        downloadFormat:'%s', showUpload:%s, map:map,
                                        includeLegend:%s, allowStyling:%s, showTable:%s})))'''
                            % (idx, idx, p("showOpacity"),p("showDownload"), p("showZoomTo"),
                               p("allowReordering"), p("allowFiltering"), p("tipLabel"),
                               self._parameters["downloadFormat"][0], p("showUpload"),
                                p("includeLegend"), p("allowStyling"), p("showTable")))
        else:
            app.panels.append('''React.createElement("div",{id: "layerlist"},
                                    React.createElement(LayerList, {showOpacity:%s, showDownload:%s,
                                        showGroupContent:true, showZoomTo:%s, allowReordering:%s,
                                        allowFiltering:%s, tipLabel:'%s',
                                        downloadFormat:'%s', showUpload:%s, map:map,
                                        includeLegend:%s, allowStyling:%s, showTable:%s}))'''
                            % (p("showOpacity"),p("showDownload"), p("showZoomTo"),
                               p("allowReordering"), p("allowFiltering"), p("tipLabel"),
                               self._parameters["downloadFormat"][0], p("showUpload"),
                                p("includeLegend"), p("allowStyling"), p("showTable")))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "layer-list.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "layer-list.png")

    def checkProblems(self, appdef, problems):
        if len(appdef["Layers"]) == 0:
            problems.append("Layer list widget added, but no layers have been included.")

        if self._parameters["showNew"] and "drawfeature" not in appdef["Widgets"]:
            problems.append("Layer list allows creating new layers, but DrawFeature component hasnt' been added")

    def description(self):
        return "Layers list"
