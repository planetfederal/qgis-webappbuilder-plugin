# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import subprocess
import traceback

from qgis.PyQt.QtCore import pyqtSignal, Qt, QThread, QCoreApplication, QEventLoop
from qgis.PyQt.QtWidgets import QApplication
from qgis.utils import iface


class ExecutorThread(QThread):

    finished = pyqtSignal()

    def __init__(self, command):
        QThread.__init__(self, iface.mainWindow())
        self.command = command
        self.returnValue = None
        self.exception = None

    def run (self):
        try:
            commands = self.command.split(" ")
            proc = subprocess.Popen(
                commands,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=open(os.devnull),
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )
            stdout = proc.stdout
            lines = []
            try:
                for line in iter(stdout.readline, ''):
                    lines.append(line)
            except:
                pass
            #if proc.returncode:
            self.exception= Exception("Error while building using Node.js:\n%s" % "".join(lines))
            self.finished.emit()
        except Exception as e:
            self.exception = e
            self.finished.emit()

def execute(command):
    global _dialog
    try:
        QCoreApplication.processEvents()
        t = ExecutorThread(command)
        loop = QEventLoop()
        t.finished.connect(loop.exit, Qt.QueuedConnection)
        QApplication.processEvents()
        t.start()
        loop.exec_(flags = QEventLoop.ExcludeUserInputEvents)
        if t.exception is not None:
            raise t.exception
        return t.returnValue
    finally:
        QCoreApplication.processEvents()
