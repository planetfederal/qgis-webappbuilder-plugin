from PyQt4.Qsci import QsciScintilla, QsciLexerCSS, QsciLexerHTML
from PyQt4 import QtGui, QtCore


class HtmlEditorDialog(QtGui.QDialog):

    def __init__(self, html, parent = None):
        super(HtmlEditorDialog, self).__init__(parent)

        self.html = html

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle('Edit style')

        layout = QtGui.QVBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.editor = HtmlEditorWidget(html)
        layout.addWidget(self.editor)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def okPressed(self):
        self.html = self.editor.text()
        self.close()

    def cancelPressed(self):
        self.html()



class HtmlEditorWidget(QsciScintilla):
    ARROW_MARKER_NUM = 8

    def __init__(self, text, parent=None):
        super(HtmlEditorWidget, self).__init__(parent)

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

        lexer = QsciLexerHTML()
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        self.setText(text)




