from PyQt4 import QtGui, QtCore

class ListSelectorDialog(QtGui.QDialog):

    def __init__(self, options, parent=None):
        super(ListSelectorDialog, self).__init__(parent)
        self.selected = []
        self.setWindowTitle("Select bookmarks")
        layout = QtGui.QVBoxLayout()

        self.optionsList = QtGui.QListWidget()
        for b in options:
            item = QtGui.QListWidgetItem()
            item.setText(b)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.optionsList.addItem(item)
        layout.addWidget(self.optionsList)

        self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.buttonBox.accepted.connect(self.okPressed)
        self.buttonBox.rejected.connect(self.cancelPressed)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.resize(500, 400)

    def okPressed(self):
        self.selected = []
        for i in xrange(self.optionsList.count()):
            item = self.optionsList.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                self.selected.append(item.text())
        self.close()

    def cancelPressed(self):
        self.selected = []
        self.close()
