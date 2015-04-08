from PyQt4.QtGui import *
from PyQt4.QtCore import *

class TreeSettingItem(QTreeWidgetItem):

    def __init__(self, parent, tree, name, value):
        QTreeWidgetItem.__init__(self, parent)
        self.parent = parent
        self.tree = tree
        self.name = name
        self._value = value
        self.setText(0, name)
        if isinstance(value, bool):
            if value:
                self.setCheckState(1, Qt.Checked)
            else:
                self.setCheckState(1, Qt.Unchecked)
        elif isinstance(value, tuple):
            self.popupCombo = QComboBox()
            for option in value[1]:
                self.popupCombo.addItem(option)
            self.tree.setItemWidget(self, 1, self.popupCombo)
        else:
            self.setFlags(self.flags() | Qt.ItemIsEditable)
            self.setText(1, unicode(value))

    def value(self):
        if isinstance(self._value, bool):
            return self.checkState(1) == Qt.Checked
        elif isinstance(self._value, (int,float)):
            return float(self.text(1))
        elif isinstance(self._value, tuple):
            return self.popupCombo.currentText()
        else:
            return self.text(1)

    def setValue(self, value):
        pass
