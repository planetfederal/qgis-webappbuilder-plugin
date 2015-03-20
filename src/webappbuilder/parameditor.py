from PyQt4 import QtGui, QtCore
from treesettingsitem import TreeSettingItem


class ParametersEditorDialog(QtGui.QDialog):

    def __init__(self, params, parent = None):
        super(ParametersEditorDialog, self).__init__(parent)

        self.params = params

        self.resize(600, 350)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowSystemMenuHint |
                                                QtCore.Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle('Edit widget parameters')

        layout = QtGui.QVBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.tree = QtGui.QTreeWidget()
        layout.addWidget(self.tree)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

        self.mainItem = QtGui.QTreeWidgetItem()
        self.mainItem.setText(0, "Parameters")
        for name, value in params.iteritems():
            subitem = TreeSettingItem(self.mainItem, self.tree, name, value)
            self.mainItem.addChild(subitem)
        self.tree.addTopLevelItem(self.mainItem)
        self.mainItem.sortChildren(0,QtCore.Qt.AscendingOrder)
        self.tree.expandAll()
        self.tree.headerItem().setText(0, "Parameter")
        self.tree.headerItem().setText(1, "Value")
        self.tree.resizeColumnToContents(0)
        self.tree.resizeColumnToContents(1)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

    def okPressed(self):
        for i in xrange(self.mainItem.childCount()):
            item = self.mainItem.child(i)
            if isinstance(self.params[item.name], tuple):
                self.params[item.name] = (item.value(), self.params[item.name][1])
            else:
                self.params[item.name] = item.value()
        self.close()

    def cancelPressed(self):
        self.close()
