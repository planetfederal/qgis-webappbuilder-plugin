from builtins import str
import os
from qgis.PyQt.QtCore import Qt, QMetaObject
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import (QDialog,
                                 QHBoxLayout,
                                 QDialogButtonBox,
                                 QTableWidget,
                                 QAbstractItemView,
                                 QPushButton,
                                 QHeaderView,
                                 QTableWidgetItem,
                                 QVBoxLayout,
                                 QLabel,
                                 QLineEdit
                                )
from webappbuilder.webbappwidget import WebAppWidget

class Links(WebAppWidget):

    _parameters = {"links":{}}

    def write(self, appdef, folder, app, progress):
        links = self._parameters["links"]
        items = []
        for name, url in list(links.items()):
            items.append('React.createElement(MenuItem, {primaryText: "%s", href:"%s"})' % (name, url))
        app.tools.append('''React.createElement(IconMenu, {iconButtonElement: React.createElement(Button, {label: "Links"})},
                                        %s
                                    )''' % ",\n".join(items))

    def icon(self):
        return QIcon(os.path.join(os.path.dirname(__file__), "links.png"))

    def iconFile(self):
        return os.path.join(os.path.dirname(__file__), "links.png")

    def description(self):
        return "Links"

    def configure(self):
        dlg = LinksDialog(self._parameters["links"])
        dlg.exec_()
        if dlg.ok:
            self._parameters["links"] = dlg.links



class LinksDialog(QDialog):
    def __init__(self, links):
        QDialog.__init__(self, None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.links = dict(links)
        self.ok = False
        self.setupUi()

    def setupUi(self):
        self.resize(500, 350)
        self.setWindowTitle("Links")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setMargin(0)
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.addRowButton = QPushButton()
        self.addRowButton.setText("Add link")
        self.editRowButton = QPushButton()
        self.editRowButton.setText("Edit link")
        self.removeRowButton = QPushButton()
        self.removeRowButton.setText("Remove link")
        self.buttonBox.addButton(self.addRowButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.editRowButton, QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.removeRowButton, QDialogButtonBox.ActionRole)
        self.setTableContent()
        self.horizontalLayout.addWidget(self.table)
        self.horizontalLayout.addWidget(self.buttonBox)
        self.setLayout(self.horizontalLayout)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.okPressed)
        self.editRowButton.clicked.connect(self.editRow)
        self.addRowButton.clicked.connect(self.addRow)
        self.removeRowButton.clicked.connect(self.removeRow)
        QMetaObject.connectSlotsByName(self)
        self.editRowButton.setEnabled(False)
        self.removeRowButton.setEnabled(False)

    def setTableContent(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(["Name", "URL"])
        self.table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        self.table.setRowCount(len(self.links))
        for i, name in enumerate(self.links):
            url = self.links[name]
            self.table.setRowHeight(i, 22)
            item = QTableWidgetItem(name, 0)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(i, 0, item)
            item = QTableWidgetItem(url, 0)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
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

class NewLinkDialog(QDialog):

    def __init__(self, name = None, url = None, parent = None):
        super(NewLinkDialog, self).__init__(parent)
        self.ok = False
        self.name = name
        self.url = url
        self.initGui()

    def initGui(self):
        self.setWindowTitle('New link')
        layout = QVBoxLayout()
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Close)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)
        nameLabel = QLabel('Link name')
        nameLabel.setMinimumWidth(120)
        nameLabel.setMaximumWidth(120)
        self.nameBox = QLineEdit()
        if self.name is not None:
            self.nameBox.setText(self.name)
        horizontalLayout.addWidget(nameLabel)
        horizontalLayout.addWidget(self.nameBox)
        layout.addLayout(horizontalLayout)

        horizontalLayout = QHBoxLayout()
        horizontalLayout.setSpacing(30)
        horizontalLayout.setMargin(0)
        urlLabel = QLabel('Url')
        urlLabel.setMinimumWidth(120)
        urlLabel.setMaximumWidth(120)
        self.urlBox = QLineEdit()
        if self.url is not None:
            self.urlBox.setText(self.url)
        horizontalLayout.addWidget(urlLabel)
        horizontalLayout.addWidget(self.urlBox)
        layout.addLayout(horizontalLayout)

        layout.addWidget(buttonBox)
        self.setLayout(layout)

        buttonBox.accepted.connect(self.okPressed)
        buttonBox.rejected.connect(self.cancelPressed)

        self.resize(400, 200)

    def okPressed(self):
        self.name = str(self.nameBox.text()).strip()
        if self.name == "":
            self.nameBox.setStyleSheet("QLineEdit{background: yellow}")
            return
        else:
            self.nameBox.setStyleSheet("QLineEdit{background: white}")

        self.url = str(self.urlBox.text()).strip()
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
