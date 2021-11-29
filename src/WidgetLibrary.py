from PySide6.QtWidgets import QVBoxLayout, QWidget
from BLabel import BLabel
from PFilterDial import PFilterDial
from ResultTable import ResultTable

class WidgetLibrary(QWidget):
    def __init__(self, parent):
        super().__init__()
        parent._result_table = ResultTable(parent, ["" for i in range(1,100)])
        
        layout = QVBoxLayout()
        layout.addWidget(BLabel(parent._config.BUTTON_LIBRARY, 14))
        layout.addWidget(parent._result_table)

        filter_p_value = str(int(parent._filter_p * 100))
        parent._label_filter_dial = BLabel(parent._config.DIAL_FILTER_P + "=" + filter_p_value, 14)
        layout.addWidget(parent._label_filter_dial)
        layout.addWidget(PFilterDial(parent))
        
        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)