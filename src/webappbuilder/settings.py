import os

def loadThemes():
    allCss = {}
    basePath = os.path.join(os.path.dirname(__file__), "themes")
    templates = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for template in templates:
        themeName = os.path.basename(template)
        path = os.path.join(template, themeName + ".css")
        with open(path) as f:
            allCss[themeName] = "".join(f.readlines())
    return allCss

def splitCssElements(s):
    with open(filename) as f:
        lines = s.splitlines()
    css = {}
    element = None
    for line in lines:
        if line.startswith("/*"):
            element = line.strip()[2:-2]
            css[element] = []
        elif element is not None:
            css[element].append(line)
    for element in css:
        css[element] = "".join(css[element])
    return css


themes = loadThemes()
currentTheme = "basic" if "basic" in themes else themes.keys()[0]
currentCss =  themes[currentTheme]

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