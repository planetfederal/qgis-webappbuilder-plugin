from webappbuilder.webbappwidget import WebAppWidget
import os
from PyQt4.QtGui import QIcon
from PyQt4.Qt import QDir
from webappbuilder.utils import safeName, replaceInTemplate
import shutil
import codecs

class Help(WebAppWidget):

    def write(self, appdef, folder, app, progress):
        self.writeHelpFiles(appdef, folder)
        app.tools.append("React.createElement(Button, {buttonType: 'Icon', iconClassName: 'headerIcons ms ms-help', tooltip: 'Help', onTouchTap: function(){window.open('help/help.html','_blank')}})")

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "help.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "help.png")

    def description(self):
        return "Help"

    def writeHelpFiles(self, appdef, folder):
        helpFolder = os.path.join(folder, "help")
        if not QDir(helpFolder).exists():
            QDir().mkpath(helpFolder)
        content = ""
        sections = ""
        for widget in appdef["Widgets"].values():
            helpContent = widget.widgetHelp()
            if helpContent is not None:
                helpImageFiles = widget.widgetHelpFiles()
                content += '<a name="%s"></a>' % widget.name()
                content += '<h2>%s</h2>' % widget.description()
                content += helpContent
                sections += '<li><a href="#%s">%s</a></li>' % (widget.name(), widget.description())
                for f in helpImageFiles:
                    shutil.copy2(f, helpFolder)

        values = {"@SECTIONS@": sections, "@TITLE@": appdef["Settings"]["Title"],
                  "@CONTENT@": content}
        templatePath = os.path.join(os.path.dirname(__file__), "base.html")
        html = replaceInTemplate(templatePath, values)

        with codecs.open(os.path.join(helpFolder, "help.html"), "w", encoding="utf-8") as f:
            f.write(html)
