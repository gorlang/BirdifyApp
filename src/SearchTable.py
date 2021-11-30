from PySide6 import QtGui
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QHeaderView, QTableView
import json

class SearchTableModel(QAbstractTableModel):
    def __init__(self, parent, data=[]):
        super().__init__()
        self._parent = parent
        self._data = data
   
    def getColor(self, p_value):
        return self._parent._config.COLOR_SCALE[int(p_value * 4)]

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 1

    def tryFloat(self, value):
        try:
            return float(value)
        except ValueError:
            return int(0)

    def asIntStr(self, value):
        try:
            return str(int(float(value)))
        except ValueError:
            return "?"

    def data(self, index, role=Qt.DisplayRole):

        data = self._data[index.row()]
        display_row = ""
        p = 0
        lang = self._parent._lang
        name_col = "name_" + lang
        if data != "" and (name_col in data):
            cols = []
            p = round(self.tryFloat(data["p"]), 2)
            if "start" in data:
                start = self.asIntStr(data["start"])
                end = self.asIntStr(data["end"])
                cols.append(start + "-" + end + "s")
            cols.append(data[name_col])
            cols.append(str(p))
            display_row = " ".join(cols)
           
        if role == Qt.DisplayRole:
            return display_row

        if role == Qt.DecorationRole:
            if p > 0:
                return QtGui.QColor(self.getColor(p))

class SearchTable(QTableView):
    def __init__(self, parent, data):
        super().__init__()
        self._parent = parent
        self._model = SearchTableModel(self._parent, data)
        self.setModel(self._model)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

    def setData(self, index, data, role):
        #count = len(self._model._data)
        self._model._data = data
        self.rowCountChanged(0, len(data))
        return False

    def insertData(self, index, data, role):
        new_data = data + self._model._data
        self.setData(index, new_data, role)
        return False
