import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QPushButton, QVBoxLayout, QWidget
import pandas as pd
from BLabel import BLabel
from SearchTable import SearchTable
from WidgetUtil import asDataFrame, dfToJson
from AppLog import Log
log = Log()

class WidgetSearch(QWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self.select_options = ["Show Check List", "Show Top List"]
        self.selected_list = self.select_options[0]
        
        layout = QVBoxLayout()
        layout.addWidget(BLabel(parent._config.BUTTON_SEARCH, 14))

        self.selectList = QComboBox()
        self.selectList.addItems(self.select_options)
        self.selectList.currentTextChanged.connect(self.selectListEvent)
        layout.addWidget(self.selectList)

        button = QPushButton("Refresh List")
        button.clicked.connect(self.refreshList)
        layout.addWidget(button)

        self.table = SearchTable(parent, ["" for i in range(1,100)])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def getCheckList(self, df, lang):
        df_result = df.groupby(["name_" + lang]).mean("p").sort_values(["p"], ascending=False)
        return dfToJson(df_result)
        
    def getTopList(self, df, lang):
        df_result = df.groupby(["name_" + lang]).max("p").sort_values(["p"], ascending=False)
        return dfToJson(df_result)
 
    def refreshList(self): 
        self.selectListEvent(self.selected_list)
        
    def selectListEvent(self, selected_item):
        self.selected_list = selected_item
        stats = self._parent._stats._detect_stats
        if len(stats) > 0:
            df = asDataFrame(stats)
            lang = self._parent._lang
            if self.selected_list == self.select_options[0]:
                self.table.setData(0, self.getCheckList(df, lang), None)
            elif self.selected_list == self.select_options[1]:
                self.table.setData(0, self.getTopList(df, lang), None)
        else:
            log.debug("No stats available!")

