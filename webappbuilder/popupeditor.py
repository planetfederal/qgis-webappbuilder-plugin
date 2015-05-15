from PyQt4 import QtGui, QtCore
from qgis.core import *
from settings import *

class PopupEditorDialog(QtGui.QDialog):

    def __init__(self, text, fields):
        super(PopupEditorDialog, self).__init__()

        self.text = text
        self.fields = fields

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Editor")

        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel()
        label.setWordWrap(True);
        label.setText("Enter the expression to use for popup texts.\n"
                      "Use [field_name] to use the value of a given field.\n\n"
                      "Available fields:" + ", ".join(fields))
        addAllButton = QtGui.QPushButton()
        addAllButton.setText("Add all attributes")
        addAllButton.clicked.connect(self.addAllAttributes)
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(addAllButton)
        hlayout.addWidget(buttonBox)
        self.editor = QtGui.QPlainTextEdit()
        self.editor.setPlainText(text)
        layout.addWidget(label)
        layout.addWidget(self.editor)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def addAllAttributes(self):
        t = "<br>".join(["<b>%s</b>: [%s]" % (f,f) for f in self.fields])
        self.editor.setPlainText(t)

    def openText(self, event):
        QtGui.QToolButton.mousePressEvent(self.button, event)


    def okPressed(self):
        self.text = self.editor.toPlainText()
        self.close()

    def cancelPressed(self):
        self.close()
