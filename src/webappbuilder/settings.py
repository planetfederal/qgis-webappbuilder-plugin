import os

elements = ["Attributes table", "Attribution", "Full screen", "Layers list", "Legend",
           "Mouse position", "North arrow", "Overview map", "Scale bar",
           "Zoom controls", "Zoom slider", "Zoom to extent", "3D view", "Edit tool",
           "Text panel", "Export as image", "Measure tool", "Geolocation", "Geocoding",
           "Chart tool", "Header", "Footer", "General", "Popup"]

def getAllCssForElement(elem):
    path = os.path.join(os.path.dirname(__file__), "templates", elem.replace(" ", "-").lower() + ".css")
    try:
        css = getCssFromFile(path)
    except:
        return None
    return css

def getCssFromFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    css = {}
    style = None
    for line in lines:
        if line.startswith("/*"):
            style = line.strip()[2:-2]
            css[style] = []
        elif style is not None:
            css[style].append(line)
    for style in css:
        css[style] = "".join(css[style])
    return css

def getDefaultCss():
    css = {}
    for e in elements:
        elemCss = getAllCssForElement(e)
        if elemCss:
            if "Basic" in elemCss:
                css[e] = elemCss["Basic"]
            else:
                css[e] = elemCss[elemCss.keys()[0]]
    return css


defaultCssStyles = getDefaultCss()
cssStyles = dict(defaultCssStyles)

defaultPanelContent = "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>"

defaultWidgetsParams = {"Text panel": {"HTML content": defaultPanelContent},
          "Overview map": {"collapsed":True},
          "Scale bar": {"minWidth": 64,
                        "units": ("metric", ("metric", "degrees", "imperial", "nautical", "us"))
                        },
          "Zoom controls": {"duration": 250, "zoomInLabel": "+", "zoomOutLabel": "-",
                           "zoomInTipLabel": "Zoom in", "zoomOutTipLabel": "Zoom out", "delta": 1.2},
          "Mouse position": {"coordinateFormat": "ol.coordinate.createStringXY(4)",
                             "projection": "EPSG:4326", "undefinedHTML": "&nbsp;"},
          "Layers list": {"tipLabel": "Layers"}}

widgetsParams = dict(defaultWidgetsParams)

defaultAppSettings = {
                "Use layer scale dependent visibility": True,
                "Extent": ("Canvas extent", ("Canvas extent", "Fit to layers extent")),
                "Restrict to extent": False,
                "Max zoom level": 28,
                "Min zoom level": 1,
                "Show popups on hover": False,
                "Highlight features on hover": False,
                "Select by rectangle": ("Not enabled", ("Not enabled", "Using Alt key", "Using Shift key", "Without using additional key"))}

appSettings = dict(defaultAppSettings)