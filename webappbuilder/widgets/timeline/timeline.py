import os

from PyQt4.QtGui import QIcon
from PyQt4.QtCore import Qt, QDate, QDateTime

from qgis.core import QgsMapLayer

from webappbuilder.webbappwidget import WebAppWidget


class Timeline(WebAppWidget):

    _parameters = {"interval": 500, "numIntervals": 100, "autoPlayFromStartup": False}

    def write(self, appdef, folder, app, progress):
        timelineOptions = self.getTimelineOptions(appdef);
        app.mappanels.append('''React.createElement("div", {id: 'timeline'},
                                    React.createElement(Playback, {map: map, minDate:%s, maxDate:%s,
                                    interval:%s, numIntervals:%s, autoPlay:%s})
                                  )''' % (timelineOptions[0], timelineOptions[1],
                                          str(self._parameters["interval"]), str(self._parameters["numIntervals"]),
                                          str(self._parameters["autoPlayFromStartup"]).lower()))
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
                if isinstance(layer.timeInfo[0], basestring):
                    features = layer.layer.getFeatures()
                    for feature in features:
                        for field in layer.timeInfo:
                            try:
                                value = feature[field]
                                if isinstance(value, QDate):
                                    t = QDateTime()
                                    t.setDate(value)
                                else:
                                    t = QDateTime.fromString(unicode(value), Qt.ISODate)
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
