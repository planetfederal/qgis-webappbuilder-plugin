from PyQt4.Qsci import QsciScintilla, QsciLexerCSS
from PyQt4 import QtGui, QtCore
from qgis.core import *
import settings


class ThemeEditorDialog(QtGui.QDialog):

    def __init__(self, parent = None):
        super(ThemeEditorDialog, self).__init__(parent)

        self.styles = settings.splitElements(settings.currentCss)
        self.currentItem = None

        self.resize(600, 600)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Edit Theme")

        layout = QtGui.QVBoxLayout()
        hlayout = QtGui.QHBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.list = QtGui.QListWidget()
        self.list.addItems(self.styles.keys())
        self.list.sortItems(True)
        self.list.itemSelectionChanged.connect(self.selectionChanged)
        layout.addWidget(self.list)
        self.editor = TextEditorWidget()
        layout.addWidget(self.editor)

        resetButton = QtGui.QPushButton()
        resetButton.setText("Reset default values")
        resetButton.clicked.connect(self.resetDefaultValues)
        hlayout.addWidget(resetButton)
        hlayout.addWidget(buttonBox)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def resetDefaultValues(self):
        settings.currentCss =  settings.themes[settings.currentTheme]
        self.styles = settings.splitElements(settings.currentCss)
        self.editor.setText(self.styles[self.currentItem.text()])

    def selectionChanged(self):
        if self.currentItem:
            self.styles[self.currentItem.text()] = self.editor.text()
        self.currentItem = self.list.currentItem()
        self.editor.setText(self.styles[self.currentItem.text()])

    def okPressed(self):
        if self.currentItem:
            self.styles[self.currentItem.text()] = self.editor.text()
        settings.currentCss = settings.joinElements(self.styles)
        self.close()

    def cancelPressed(self):
        self.close()



class TextEditorWidget(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
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

        lexer = QsciLexerCSS()

        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')



