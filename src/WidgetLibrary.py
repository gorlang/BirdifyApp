from PySide6.QtWidgets import QMessageBox, QPushButton, QVBoxLayout, QWidget
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

