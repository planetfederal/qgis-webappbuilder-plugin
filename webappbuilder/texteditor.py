from PyQt4.Qsci import QsciScintilla, QsciLexerCSS, QsciLexerHTML,\
    QsciLexerJavaScript
from PyQt4 import QtGui, QtCore
from qgis.core import *
from settings import *
from functools import partial

CSS = 0
HTML = 1
JSON = 2

class TextEditorDialog(QtGui.QDialog):

    def __init__(self, text, textType, parent = None):
        super(TextEditorDialog, self).__init__(parent)

        self.text = text

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Editor")

        layout = QtGui.QVBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.editor = TextEditorWidget(text, textType)
        layout.addWidget(self.editor)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def openText(self, event):
        QtGui.QToolButton.mousePressEvent(self.button, event)


    def okPressed(self):
        self.text = self.editor.text()
        self.close()

    def cancelPressed(self):
        self.close()



class TextEditorWidget(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, text, textType, parent=None):
        super(TextEditorWidget, self).__init__(parent)

        font = QtGui.QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        fontmetrics = QtGui.QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QtGui.QColor("#cccccc"))

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QtGui.QColor("#ffe4e4"))

        if textType == CSS:
            lexer = QsciLexerCSS()
        elif textType == JSON:
            lexer =QsciLexerJavaScript()
        else:
            lexer = QsciLexerHTML()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        self.setText(text)


