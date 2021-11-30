import json
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QPushButton, QVBoxLayout, QWidget
import pandas as pd
from BLabel import BLabel
from SearchTable import SearchTable
from AppLog import Log
log = Log()

class WidgetSearch(QWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self.check_list = True
        self.filteredData = [{"name_sv": "hej1", "p": "0.5", "name_en": "hello"}]
        
        layout = QVBoxLayout()
        layout.addWidget(BLabel(parent._config.BUTTON_SEARCH, 14))

        checkList = QCheckBox("Show Check List")
        checkList.setCheckState(Qt.Unchecked)
        checkList.stateChanged.connect(self.checkListEvent)
        layout.addWidget(checkList)

        button = QPushButton("Refresh List")
        button.clicked.connect(self.refreshList)
        layout.addWidget(button)

        self.table = SearchTable(parent, ["" for i in range(1,100)])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def asDataFrame(self, stats):
        if len(stats) > 0:
            df_indata = {}
            colnames = list(stats[0])
            log.debug(f"colnames={colnames}")
            for colname in colnames:
                df_indata[colname] = []
            for row in stats:
                for col in colnames:
                    df_indata[col].append(row[col])
            return pd.DataFrame(data=df_indata)
        return None

    def getCheckList(self, df):
        df['p'] = df['p'].astype(float)
        lang = self._parent._lang
        df_result = df.groupby(["name_" + lang]).mean("p").sort_values(["p"], ascending=False)
        json_result = df_result.to_json(orient="table")
        data = json.loads(json_result)["data"]
        return data

    def refreshList(self, i):
        self.checkListEvent(None)
        log.debug("refresh")
        
    def checkListEvent(self, i):
        if i != None:
            self.check_list = False if i == 0 else True
        log.debug(f"checked, {i},{self.check_list}")
        if self.check_list:
            stats = self._parent._stats._detect_stats
            if self._parent._config.TEST:
                log.debug(f"TEST! stats={stats}")
                stats = [{"name_sv": "apa1", "name_en": "apa1e", "p": "0.25999"},{"name_sv": "apa1", "name_en": "apa1e", "p": "0.5"},{"name_sv": "apa2", "name_en": "apa2e", "p": "1"},{"name_sv": "apa3", "name_en": "apa3e", "p": "0.1"},{"name_sv": "apa3", "name_en": "apa3e", "p": "0.2"}]
            if len(stats) > 0:
                df = self.asDataFrame(stats)
                search_result = self.getCheckList(df)
                self.filteredData = search_result
                self.table.setData(0, self.filteredData, None)
            else:
                log.debug("No searchresult!")

