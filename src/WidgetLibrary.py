from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout, QWidget
from BLabel import BLabel
from PFilterDial import PFilterDial
from ResultTable import ResultTable
from AppLog import Log
log = Log()


class WidgetLibrary(QWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self._filter_p = None # if == None => use parent._filter_p as targer in PFilterDial()

        parent._result_table = ResultTable(parent, ["" for i in range(1,100)])
        
        layout = QVBoxLayout()
        layout.addWidget(BLabel(parent._config.BUTTON_LIBRARY, 14))
        layout.addWidget(parent._result_table)

        # search buttons
        layout_buttons = QHBoxLayout()
        search_button_1 = QPushButton("Google Search")
        search_button_1.clicked.connect(self.doGoogleSearch)
        layout_buttons.addWidget(search_button_1)

        search_button_2 = QPushButton("Xeno-Canto Search")
        search_button_2.clicked.connect(self.doXenoCantoSearch)
        layout_buttons.addWidget(search_button_2)
        layout.addLayout(layout_buttons)

        # filter dial
        self._label_filter_dial = BLabel(parent._config.DIAL_FILTER_P + "=" + str(parent._filter_p), 14)
        layout.addWidget(self._label_filter_dial)
        layout.addWidget(PFilterDial(parent, self))

        reset_button = QPushButton("Clear Detected")
        reset_button.clicked.connect(self.dialogClearDetected)
        layout.addWidget(reset_button)
        
        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)

    def dialogClearDetected(self):
        msg = QMessageBox()
        msg.setText("Click OK to remove all detected!")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.clearDetected)
        msg.exec_()

    def clearDetected(self, i):
        action = i.text()
        if action == "OK":
            self._parent.clearDetected()

    def getSelectedNames(self):
        selectedNames = []
        for i, selectedIndex in enumerate(self._parent._result_table.selectedIndexes()):
            if selectedIndex.data() != None:
                words = selectedIndex.data().split(" ")[1:-1]
                names = " ".join(words).split("/")
                selectedNames.append(names)
        return selectedNames

    def doGoogleSearch(self):
        names = self.getSelectedNames()
        if len(names) > 0:
            search_url = "https://www.google.com/search?q="
            search_str = '" +"'.join(names[0])
            search_str = '"' +  search_str + '"'
            log.info(f"search_str={search_str}")
            QDesktopServices.openUrl(QUrl(search_url + search_str, QUrl.TolerantMode))
        else:
            QMessageBox.warning(None, "", "Select a species!")

    def doXenoCantoSearch(self):
        names = self.getSelectedNames()
        if len(names) > 0:
            search_url = "https://xeno-canto.org/species/"
            search_str = names[0][1].replace(" ", "-")
            log.info(f"search_str={search_str}")
            QDesktopServices.openUrl(QUrl(search_url + search_str, QUrl.TolerantMode))
        else:
            QMessageBox.warning(None, "", "Select a species!")