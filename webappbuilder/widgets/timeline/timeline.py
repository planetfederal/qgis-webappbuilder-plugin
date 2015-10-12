from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from PyQt4.QtCore import QDate, QDateTime
from PyQt4.Qt import Qt

class Timeline(WebAppWidget):

    _parameters = {"interval": 500, "numIntervals": 100, "autoPlayFromStartup": False}

    def write(self, appdef, folder, app, progress):
        timelineOptions = self.getTimelineOptions(appdef);
        app.mappanels.append("<div id='timeline'><Playback map={map} minDate={%s} maxDate={%s} /></div>"
                            % (timelineOptions[0], timelineOptions[1]))


    '''def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "timeline.png"))'''

    def description(self):
        return "Timeline"

    def getTimelineOptions(self, appdef):
        layers = appdef["Layers"]
        times = set()
        for layer in layers:
            if layer.timeInfo is not None:
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