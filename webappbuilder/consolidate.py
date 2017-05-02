from appcreator import saveAppdef
try:
    from qconsolidate import consolidatethread
except:
    pass
import os
from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.utils import iface
import shutil

def consolidate(folder, appdef):
    tmpFolder = os.path.join(folder, "temp")
    if os.path.exists(tmpFolder):
        shutil.rmtree(tmpFolder)
    os.mkdir(tmpFolder)
    # copy project file
    projectFile = QgsProject.instance().fileName()
    f = QFile(projectFile)
    newProjectFile = tmpFolder + "/" + QFileInfo(projectFile).fileName()
    f.copy(newProjectFile)

    # start consolidate thread that does all real work
    loop = QEventLoop()
    workThread = consolidatethread.ConsolidateThread(iface, tmpFolder, newProjectFile)
    def processFinished():
        workThread.stop()
        QApplication.restoreOverrideCursor()
        appdefFile = os.path.join(tmpFolder, os.path.basename(projectFile) + ".appdef")
        saveAppdef(appdef, appdefFile)
        shutil.make_archive(os.path.join(folder, "webapp"), 'zip', tmpFolder)
        shutil.rmtree(tmpFolder)
        loop.exit()
    def processError(message):
        QApplication.restoreOverrideCursor()
        QMessageBox.warning(None,
                        "QConsolidate: Error",
                        message
                       )
    def silent(*args, **kw):
        pass

    workThread.rangeChanged.connect(silent)
    workThread.updateProgress.connect(silent)
    workThread.processFinished.connect(processFinished)
    workThread.processInterrupted.connect(silent)
    workThread.processError.connect(processError)
    workThread.start()

    loop.exec_(flags = QEventLoop.ExcludeUserInputEvents)





