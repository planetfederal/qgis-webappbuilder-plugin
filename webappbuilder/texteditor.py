# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
from functools import partial

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QToolButton
from qgis.PyQt.QtGui import QFont, QFontMetrics, QColor
from qgis.PyQt.Qsci import QsciScintilla

CSS = 0
HTML = 1
JSON = 2

class TextEditorDialog(QDialog):

    def __init__(self, text, textType, parent = None):
        super(TextEditorDialog, self).__init__(parent)

        self.text = text

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | Qt.WindowSystemMenuHint |
                                                Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Editor")

        layout = QVBoxLayout()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.editor = TextEditorWidget(text, textType)
        layout.addWidget(self.editor)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def openText(self, event):
        QToolButton.mousePressEvent(self.button, event)

    def okPressed(self):
        self.text = self.editor.text()
        self.close()

    def cancelPressed(self):
        self.close()



class TextEditorWidget(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, text, textType, parent=None):
        super(TextEditorWidget, self).__init__(parent)

        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("00000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#cccccc"))

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#ffe4e4"))

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
