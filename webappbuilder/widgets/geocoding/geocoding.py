from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon

class Geocoding(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        app.tools.append('''<div class="navbar-form navbar-right">
                          <div class="input-group">
                              <input type="text" onkeypress="searchBoxKeyPressed(event);" id="geocoding-search" class="form-control" placeholder="Search placename..."/>
                              <div class="input-group-btn">
                                  <button class="btn btn-default" onclick="searchAddress()"><span>&nbsp;</span><i class="glyphicon glyphicon-search"></i></button>
                              </div>
                          </div>
                        </div>''');
        app.mappanels.append('<div id="geocoding-results" class="geocoding-results"></div>')
        self.addScript("geocoding.js", folder, app)
        self.copyToResources("marker.png", folder)

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "geocoding.png"))

    def description(self):
        return "Geocoding"