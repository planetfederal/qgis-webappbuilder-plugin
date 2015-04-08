from PyQt4.Qsci import QsciScintilla, QsciLexerCSS, QsciLexerHTML
from PyQt4 import QtGui, QtCore
from qgis.core import *
from settings import *
from functools import partial

CSS = 0
HTML = 1

class TextEditorDialog(QtGui.QDialog):

    def __init__(self, text, textType, elementName = None, parent = None):
        super(TextEditorDialog, self).__init__(parent)

        self.text = text

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Edit CSS" if textType == CSS else "Edit HTML")

        layout = QtGui.QVBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.editor = TextEditorWidget(text, textType)
        if textType == CSS and elementName is not None:
            allCss = getAllCssForElement(elementName)
            if allCss:
                self.button = QtGui.QToolButton()
                self.button.setAutoRaise(True)
                self.button.setText("Predefined styles")
                menu = QtGui.QMenu()
                for css in allCss:
                    menu.addAction(css, partial(self.editor.setText, allCss[css]))
                self.button.setMenu(menu)
                layout.addWidget(self.button)

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
        else:
            lexer = QsciLexerHTML()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        self.setText(text)


