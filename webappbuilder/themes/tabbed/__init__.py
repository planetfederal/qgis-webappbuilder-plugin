def checkProblems(appdef, problems):
    widgetsInTab = ["aboutpanel", "attributestable", "bookmarks", "charttool",
           "geocoding"]

    for w in widgetsInTab:
        if w in appdef["Widgets"].keys():
            return

    problems.append("Tabbed them is used, but no component that requires the tab panel is used.")