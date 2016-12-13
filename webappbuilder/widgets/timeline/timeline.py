from builtins import str
import os

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import Qt, QDate, QDateTime

from qgis.core import QgsMapLayer

from webappbuilder.webbappwidget import WebAppWidget


class Timeline(WebAppWidget):

    _parameters = {"interval": 500, "numIntervals": 100, "autoPlayFromStartup": False}

    def write(self, appdef, folder, app, progress):
        timelineOptions = self.getTimelineOptions(appdef);
        app.mappanels.append('''React.createElement("div", {id: 'timeline'},
                                    React.createElement(Playback, {map: map, minDate:%s, maxDate:%s})
                                  )''' % (timelineOptions[0], timelineOptions[1]))
        self.addReactComponent(app, "Playback")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "timeline.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "timeline.png")

    def description(self):
        return "Timeline"

    def getTimelineOptions(self, appdef):
        layers = appdef["Layers"]
        times = set()
        for layer in layers:
            if layer.timeInfo is not None and layer.layer.type() == QgsMapLayer.VectorLayer:
                if isinstance(layer.timeInfo[0], str):
                    features = layer.layer.getFeatures()
                    for feature in features:
                        for field in layer.timeInfo:
                            try:
                                value = feature[field]
                                if isinstance(value, QDate):
                                    t = QDateTime()
                                    t.setDate(value)
                                else:
                                    t = QDateTime.fromString(str(value), Qt.ISODate)
                                if t.isValid():
                                    times.add(t.toMSecsSinceEpoch())
                            except:
                                pass
                else:
                    times.add(layer.timeInfo[0])
                    times.add(layer.timeInfo[1])

        if times:
            return [min(times), max(times)]
        else:
            return [0,1]
