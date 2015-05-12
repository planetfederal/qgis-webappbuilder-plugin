from PyQt4 import QtCore, QtGui

class LinksDialog(QtGui.QDialog):
    def __init__(self, links, parent):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.links = dict(links)
        self.ok = False
        self.setupUi()

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Links")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QtGui.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.table = QtGui.QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.addRowButton = QtGui.QPushButton()
        self.addRowButton.setText("Add link")
        self.editRowButton = QtGui.QPushButton()
        self.editRowButton.setText("Edit link")
        self.removeRowButton = QtGui.QPushButton()
        self.removeRowButton.setText("Remove link")
        self.buttonBox.addButton(self.addRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.editRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.removeRowButton, QtGui.QDialogButtonBox.ActionRole)
        self.setTableContent()
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.okPressed)
        self.editRowButton.clicked.connect(self.editRow)
        self.addRowButton.clicked.connect(self.addRow)
        self.removeRowButton.clicked.connect(self.removeRow)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.editRowButton.setEnabled(False)
        self.removeRowButton.setEnabled(False)

    def setTableContent(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(["Name", "URL"])
        self.table.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.table.setRowCount(len(self.links))
        for i, name in enumerate(self.links):
            url = self.links[name]
            self.table.setRowHeight(i, 22)
            item = QtGui.QTableWidgetItem(name, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.table.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(url, 0)
            item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            self.table.setItem(i, 1, item)

        self.table.itemSelectionChanged.connect(self.selectionChanged)

    def selectionChanged(self):
        enabled = len(self.table.selectedItems()) > 0
        self.editRowButton.setEnabled(enabled)
        self.removeRowButton.setEnabled(enabled)

    def editRow(self):
        item = self.table.item(self.table.currentRow(), 0)
        if item is not None:
            name = item.text()
            url = self.table.item(self.table.currentRow(), 1).text()
            dlg = NewLinkDialog(name, url, self)
            dlg.exec_()
            if dlg.ok:
                self.links[name] = url
                self.setTableContent()


    def removeRow(self):
        item = self.table.item(self.table.currentRow(), 0)
        if item is not None:
            name = item.text()
            del self.links[name]
            self.setTableContent()

    def addRow(self):
        dlg = NewLinkDialog(parent = self)
        dlg.exec_()
        if dlg.ok:
            self.links[dlg.name] = dlg.url
            self.setTableContent()

    def okPressed(self):
        self.ok = True
        self.close()

class NewLinkDialog(QtGui.QDialog):

    def __init__(self, name = None, url = None, parent = None):
        super(NewLinkDialog, self).__init__(parent)
        self.ok = False
        self.name = name
        self.url = url
        self.initGui()

    def initGui(self):
        self.setWindowTitle('New link')
        layout = QtGui.QVBoxLayout()
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Close)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)
        nameLabel = QtGui.QLabel('Link name')
        nameLabel.setMinimumWidth(120)
        nameLabel.setMaximumWidth(120)
        self.nameBox = QtGui.QLineEdit()
        if self.name is not None:
            self.nameBox.setText(self.name)
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)

        horizontalLayout = QtGui.QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)
        urlLabel = QtGui.QLabel('Url')
        urlLabel.setMinimumWidth(120)
        urlLabel.setMaximumWidth(120)
        self.urlBox = QtGui.QLineEdit()
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        layout.addLayout(horizontalLayout)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

        self.resize(400, 200)

    def okPressed(self):
        self.name = unicode(self.nameBox.text()).strip()
        if self.name == "":
            self.nameBox.setStyleSheet("QLineEdit{background: yellow}")
            return
        else:
            self.nameBox.setStyleSheet("QLineEdit{background: white}")

        self.url = unicode(self.urlBox.text()).strip()
        if self.url == "":
            self.urlBox.setStyleSheet("QLineEdit{background: yellow}")
            return
        else:
            self.urlBox.setStyleSheet("QLineEdit{background: white}")
        self.ok = True
        self.close()

    def cancelPressed(self):
        self.name = None
        self.url = None
        self.close()
