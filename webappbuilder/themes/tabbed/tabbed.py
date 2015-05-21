import os
import json
import shutil
from bs4 import BeautifulSoup as bs
from webappbuilder.utils import SHOW_BOOKMARKS_IN_MENU, safeName, replaceInTemplate

def writeWebApp(appdef, folder):
    layers = appdef["Layers"]
    widgets = appdef["Widgets"]
    tools = []
    initialize = []
    tabs =[]
    panels = []
    imports = []
    importsAfter = []
    if "About panel" in widgets:
        params = widgets["About panel"]
        tabs.append('<li><a href="#about-tab" role="tab" data-toggle="tab">About</a></li>')
        panels.append('''<div class="tab-pane" id="about-tab">
                        <div class="about-panel" id="about-panel">%s</div>
                        </div>''' % params["content"])
    if "Geocoding" in widgets:
        tabs.append('<li><a href="#geocoding-tab" role="tab" data-toggle="tab">Geocoding</a></li>')
        panels.append('''<div class="tab-pane" id="geocoding-tab">
                            <div class="input-group">
                               <input class="form-control" id="geocoding-search" onkeypress="searchBoxKeyPressed(event);" placeholder="Search placename..." type="text"/>
                               <div class="input-group-btn">
                                <button class="btn btn-default" onclick="searchAddress()">
                                 <span>
                                  &nbsp;
                                 </span>
                                 <i class="glyphicon glyphicon-search">
                                 </i>
                                </button>
                               </div>
                            </div>
                            <div class="geocoding-results" id="geocoding-results">
                            </div>
                          </div>  ''');

    if "Links" in widgets:
        links = widgets["Links"]["links"]
        for name, url in links.iteritems():
            tools.append('<li><a href="%s">%s</a></li>' % (url, name))
    if "Selection tools" in widgets:
        params = widgets["Selection tools"]
        selectTools = []
        if params["Select single feature"]:
            selectTools.append(["selectSingleFeature()", "Select single feature"])
        if params["Select by polygon"]:
            selectTools.append(["selectByPolygon()", "Select by polygon"])
        if params["Select by point and radius"]:
            selectTools.append(["selectByPointAndRadius()", "Select by point and radius"])
        if params["Select by rectangle"]:
            selectTools.append(["selectByRectangle()", "Select by rectangle"])
        if selectTools:
            li = "\n".join(['<li><a onclick="%s" href="#">%s</a></li>' % (sel[0], sel[1]) for sel in selectTools])
            tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                            Selection <span class="caret"><span></a>
                            <ul class="dropdown-menu">
                              %s
                            </ul>
                          </li>''' % li)

    if "Query" in widgets:
        imports.append('''<script src="./resources/filtrex.js"></script>''')
        tabs.append('<li><a href="#query-tab" role="tab" data-toggle="tab">Query</a></li>')
        panels.append('''<div class="tab-pane" id="query-tab">
                            <div class="query-panel" id="query-panel">
                               <form class="form-horizontal">
                                <div class="input-group" style="margin-bottom: 25px">
                                 <span class="input-group-addon">Layer</span>
                                 <select class="form-control" id="query-layer"> </select>
                                </div>
                                <div class="input-group" style="margin-bottom: 25px">
                                 <span class="input-group-addon">Filter</span>
                                 <input class="form-control" id="query-expression" placeholder="Type expression..." type="text"/>
                                </div>
                                <div class="form-group" style="margin-top:10px">
                                 <div class="col-sm-12 controls">
                                  <a class="btn btn-primary" href="#" id="btn-query-new">New selection</a>
                                  <a class="btn btn-primary" href="#" id="btn-query-add">Add to current selection</a>
                                  <a class="btn btn-primary" href="#" id="btn-query-in">Select in current selection</a>
                                 </div>
                                </div>
                               </form>
                              </div>
                              </div>''')
        initialize.append("showQueryPanel();")
    if "Export as image" in widgets:
        tools.append('<li><a onclick="saveAsPng()" href="#" id="export-as-image"><i class="glyphicon glyphicon-camera"></i>Export as image</a></li>')
    if "Attributes table" in widgets:
        tabs.append('<li><a href="#attributes-table-tab" role="tab" data-toggle="tab">Attributes table</a></li>')
        panels.append('''<div class="tab-pane" id="attributes-table-tab">
                            <div class="attributes-table"></div>
                        </div>''')
        initialize.append("showAttributesTable();")
    if "Measure tool" in widgets:
        tools.append('''<li class="dropdown">
                            <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Measure <span class="caret"><span> </a>
                            <ul class="dropdown-menu">
                              <li><a onclick="measureTool('distance')" href="#">Distance</a></li>
                              <li><a onclick="measureTool('area')" href="#">Area</a></li>
                              <li><a onclick="measureTool(null)" href="#">Remove measurements</a></li>
                            </ul>
                          </li>''')
    if "Chart tool" in widgets:
        params = widgets["Chart tool"]
        tabs.append('<li><a href="#charts-tab" role="tab" data-toggle="tab">Charts</a></li>')
        imports.append('''<script src="./resources/d3.min.js"></script>
                        <script src="./resources/c3.min.js"></script>
                        <link href="./resources/c3.min.css" rel="stylesheet" type="text/css"/>
                        <script src="./charts.js"></script>''')
        panels.append('''<div class="tab-pane" id="charts-tab">
                            <div class="chart-panel" id="chart-panel">
                            <select id="chart-selector" class="form-control"></select>
                              <div class="chart-panel-info" id="chart-panel-info">
                              </div>
                                <div id="chart">
                                </div>
                             </div>
                          </div>''')
        initialize.append('''sel = document.getElementById("chart-selector");
                              chartNames = Object.keys(charts)
                              for (var i = 0; i < chartNames.length; i++){
                                  var option = document.createElement('option');
                                  option.value = option.textContent = chartNames[i];
                                  sel.appendChild(option);
                              }
                              sel.onchange = function(){
                                  openChart(this.value);
                              };
                              openChart(Object.keys(charts)[0]);''')
        chartsFilepath = os.path.join(folder, "charts.js")
        with open(chartsFilepath, "w") as f:
            f.write("var AGGREGATION_MIN = 0;")
            f.write("var AGGREGATION_MAX = 1;")
            f.write("var AGGREGATION_SUM = 2;")
            f.write("var AGGREGATION_AVG = 3;")
            f.write("var DISPLAY_MODE_FEATURE = 0;")
            f.write("var DISPLAY_MODE_CATEGORY = 1;")
            f.write("var DISPLAY_MODE_COUNT = 2;")
            f.write("var charts = " + json.dumps(params["charts"]))

    if "Help" in widgets:
        tools.append('<li><a href="./help.html"><i class="glyphicon glyphicon-question-sign"></i>Help</a></li>')

    bookmarkEvents = ""
    if "Bookmarks" in widgets:
        params = widgets["Bookmarks"]
        bookmarks = params["bookmarks"]
        if bookmarks:
            importsAfter.append('<script src="./bookmarks.js"></script>')
            if params["format"] != SHOW_BOOKMARKS_IN_MENU:
                itemBase = '''<div class="item %s">
                              <div class="header-text hidden-xs">
                                  <div class="col-md-12 text-center">
                                      <h2>%s</h2>
                                      <p>%s</p>
                                  </div>
                              </div>
                            </div>'''
                bookmarkDivs = itemBase % ("active", params["introTitle"], params["introText"])
                bookmarkDivs += "\n".join([itemBase % ("", b[0], b[2]) for i,b in enumerate(bookmarks)])
                if params["showIndicators"]:
                    li = "\n".join(['<li data-target="#story-carousel" data-slide-to="%i"></li>' % (i+1) for i in xrange(len(bookmarks))])
                    indicators = '''<ol class="carousel-indicators">
                                        <li data-target="#story-carousel" data-slide-to="0" class="active"></li>
                                        %s
                                    </ol>''' % li
                else:
                    indicators = ""
                slide = "slide" if params["interval"] else ""
                interval = str(params["interval"] * 1000) if params["interval"] else "false"
                panels.append('''<div class="tab-pane" id="bookmarks-tab">
                    <div class="story-panel">
                      <div class="row">
                          <div id="story-carousel" class="carousel %s" data-interval="%s" data-ride="carousel">
                            %s
                            <div class="carousel-inner">
                                %s
                            </div>
                          </div>
                          <a class="left carousel-control" href="#story-carousel" data-slide="prev">
                              <span class="glyphicon glyphicon-chevron-left">&nbsp;</span>
                          </a>
                          <a class="right carousel-control" href="#story-carousel" data-slide="next">
                              <span class="glyphicon glyphicon-chevron-right">&nbsp;</span>
                          </a>
                      </div>
                    </div>
                    </div>
                    ''' % (slide, interval, indicators, bookmarkDivs))
                bookmarkEvents = '''\n$("#story-carousel").on('slide.bs.carousel', function(evt) {
                                          %sToBookmark($(evt.relatedTarget).index()-1)
                                    })''' % ["go", "pan", "fly"][params["format"]]
                tabs.append('<li><a href="#bookmarks-tab" role="tab" data-toggle="tab">Bookmarks</a></li>')
            else:
                li = "\n".join(["<li><a onclick=\"goToBookmarkByName('%s')\" href=\"#\">%s</a></li>" % (b[0],b[0]) for b in params["bookmarks"]])
                tools.append('''<li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown"> Bookmarks <span class="caret"><span></a>
                    <ul class="dropdown-menu">
                      %s
                    </ul>
                  </li>''' % li)
            bookmarksFilepath = os.path.join(folder, "bookmarks.js")
            with open(bookmarksFilepath, "w") as f:
                bookmarksWithoutDescriptions = [b[:-1] for b in bookmarks]
                f.write("var bookmarks = " + json.dumps(bookmarksWithoutDescriptions))
                f.write(bookmarkEvents)

    imports.extend(['<script src="layers/lyr_%s.js"></script>' % (safeName(layer.layer.name()))
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])
    imports.extend(['<script src="styles/%s.js"></script>' % (safeName(layer.layer.name()))
                            for layer in layers if layer.layer.type() == layer.layer.VectorLayer])

    if "Layers list" in widgets and widgets["Layers list"]["showOpacity"]:
        imports.append('<script src="./resources/bootstrap-slider.js"></script>')
        imports.append('<link href="./resources/slider.css" rel="stylesheet"/>')
    if "3D view" in widgets:
        imports.append('<script src="./resources/cesium/Cesium.js"></script>')
        imports.append('<script src="./resources/ol3cesium.js"></script>')
        dst = os.path.join(folder, "resources", "cesium")
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(os.path.dirname(__file__), "resources", "cesium"), dst)

    logoImg = appdef["Settings"]["Logo"].strip()
    if logoImg:
        logo = '<img class="pull-left" style="margin:5px;height:calc(100%%-10px);" src="logo.png"></img>'
        ext = os.path.splitext(logoImg)[1]
        shutil.copyfile(logoImg, os.path.join(folder, "logo" + ext))
    else:
        logo = ""

    if panels:
        panels[0] = panels[0].replace("tab-pane", "tab-pane active in")
        tabs[0] = tabs[0].replace("<li>", '<li class="active">')

    values = {"@TITLE@": appdef["Settings"]["Title"],
              "@LOGO@": logo,
                "@IMPORTS@": "\n".join(imports),
                "@IMPORTSAFTER@": "\n".join(importsAfter),
                "@TABS@": "\n".join(tabs),
                "@TABPANELS@": "\n".join(panels),
                "@TOOLBAR@": "\n".join(tools),
                "@INITIALIZE@": "\n".join(initialize)}
    indexFilepath = os.path.join(folder, "index.html")
    template = os.path.join(os.path.dirname(__file__), "tabbed.html")
    html = replaceInTemplate(template, values)
    soup=bs(html)
    pretty=soup.prettify(formatter='html')
    with open(indexFilepath, "w") as f:
        f.write(pretty)
    return indexFilepath