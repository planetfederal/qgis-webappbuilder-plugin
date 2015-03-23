import os

def getAllCssForElement(elem):
    allCss = {}
    basePath = os.path.join(os.path.dirname(__file__), "templates")
    templates = [os.path.join(basePath,o) for o in os.listdir(basePath)
                 if os.path.isdir(os.path.join(basePath,o))]
    for template in templates:
        templateName = os.path.basename(template)
        path = os.path.join(template, "widgets.css")
        css = getCssFromTemplate(path)
        if elem in css:
            allCss[templateName] = css[elem]
        path = os.path.join(template, "index.css")
        css = getCssFromTemplate(path)
        if elem in css:
            allCss[templateName] = css[elem]
    return allCss

def getCssFromTemplate(template):
    with open(template) as f:
        lines = f.readlines()
    css = {}
    widget = None
    for line in lines:
        if line.startswith("/*"):
            widget = line.strip()[2:-2]
            css[widget] = []
        elif widget is not None:
            css[widget].append(line)
    for widget in css:
        css[widget] = "".join(css[widget])
    return css

widgetsTemplate = os.path.join(os.path.dirname(__file__), "templates", "basic", "widgets.css")
widgetsCss = getCssFromTemplate(widgetsTemplate)

baseTemplate = os.path.join(os.path.dirname(__file__), "templates", "basic", "index.css")
baseCss = getCssFromTemplate(baseTemplate)

defaultPanelContent = "<h1>Panel Title</h1>\n<p>This is the description of my web app</p>"

widgetsParams = {"Text panel": {"HTML content": defaultPanelContent},
          "Overview map": {"collapsed":True},
          "Scale bar": {"minWidth": 64,
                        "units": ("metric", ("metric", "degrees", "imperial", "nautical", "us"))
                        },
          "Zoom controls": {"duration": 250, "zoomInLabel": "+", "zoomOutLabel": "-",
                           "zoomInTipLabel": "Zoom in", "zoomOutTipLabel": "Zoom out", "delta": 1.2},
          "Mouse position": {"coordinateFormat": "ol.coordinate.createStringXY(4)",
                             "projection": "EPSG:4326", "undefinedHTML": "&nbsp;"},
          "Layers list": {"tipLabel": "Layers"}}

appSettings = {
                "Use layer scale dependent visibility": True,
                "Extent": ("Canvas extent", ("Canvas extent", "Fit to layers extent")),
                "Restrict to extent": False,
                "Max zoom level": 28,
                "Min zoom level": 1,
                "Show popups on hover": False,
                "Highlight features on hover": False}