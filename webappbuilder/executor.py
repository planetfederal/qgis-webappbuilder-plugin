# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from qgis.utils import iface
from qgis.core import *
from PyQt4 import QtGui, QtCore
import subprocess
import os
import traceback


class ExecutorThread(QtCore.QThread):

    finished = QtCore.pyqtSignal()

    def __init__(self, command):
        QtCore.QThread.__init__(self, iface.mainWindow())
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
        except Exception, e:
            self.exception = e
            self.finished.emit()

def execute(command):
    global _dialog
    try:
        QtCore.QCoreApplication.processEvents()
        t = ExecutorThread(command)
        loop = QtCore.QEventLoop()
        t.finished.connect(loop.exit, QtCore.Qt.QueuedConnection)
        QtGui.QApplication.processEvents()
        t.start()
        loop.exec_(flags = QtCore.QEventLoop.ExcludeUserInputEvents)
        if t.exception is not None:
            raise t.exception
        return t.returnValue
    finally:
        QtCore.QCoreApplication.processEvents()
