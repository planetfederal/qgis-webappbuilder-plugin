from PyQt4.QtGui import *
from PyQt4.QtCore import *
from texteditor import TextEditorDialog, JSON
from settings import WrongValueException

class TreeSettingItem(QTreeWidgetItem):

    comboStyle = '''QComboBox {
                 border: 1px solid gray;
                 border-radius: 3px;
                 padding: 1px 18px 1px 3px;
                 min-width: 6em;
             }

             QComboBox::drop-down {
                 subcontrol-origin: padding;
                 subcontrol-position: top right;
                 width: 15px;
                 border-left-width: 1px;
                 border-left-color: darkgray;
                 border-left-style: solid;
                 border-top-right-radius: 3px;
                 border-bottom-right-radius: 3px;
             }
            '''

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
            self.combo = QComboBox()
            self.combo.setStyleSheet(self.comboStyle)
            for option in value[1]:
                self.combo.addItem(option)
            self.tree.setItemWidget(self, 1, self.combo)
            idx = self.combo.findText(value[0])
            self.combo.setCurrentIndex(idx)
        elif "\n" in unicode(value):
            self.label = QLabel()
            self.label.setText("<a href='#'>Edit</a>")
            self.newValue = value
            def edit():
                dlg = TextEditorDialog(unicode(value), JSON)
                dlg.exec_()
                self.newValue = dlg.text
            self.label.connect(self.label, SIGNAL("linkActivated(QString)"), edit)
            self.tree.setItemWidget(self, 1, self.label)
        else:
            self.setFlags(self.flags() | Qt.ItemIsEditable)
            self.setText(1, unicode(value))


    def value(self):
        self.setBackgroundColor(0, Qt.white)
        self.setBackgroundColor(1, Qt.white)
        try:
            if isinstance(self._value, bool):
                return self.checkState(1) == Qt.Checked
            elif isinstance(self._value, (int,long)):
                return long(self.text(1))
            elif isinstance(self._value, float):
                return float(self.text(1))
            elif isinstance(self._value, tuple):
                return self.combo.currentText()
            elif "\n" in unicode(self._value):
                return self.newValue
            else:
                return self.text(1)
        except:
            self.setBackgroundColor(0, Qt.yellow)
            self.setBackgroundColor(1, Qt.yellow)
            raise WrongValueException()

    def setValue(self, value):
        if isinstance(self._value, bool):
            if value:
                self.setCheckState(1, Qt.Checked)
            else:
                self.setCheckState(1, Qt.Unchecked)
        elif isinstance(self._value, tuple):
            idx = self.combo.findText(value)
            self.combo.setCurrentIndex(idx)
        elif "\n" in unicode(self._value):
            self.newValue = value
        else:
            self.setText(1, unicode(value))
