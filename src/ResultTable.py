from PySide6 import QtGui
from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtWidgets import QHeaderView, QTableView

class ResultTableModel(QAbstractTableModel):
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

    def data(self, index, role=Qt.DisplayRole):

        row = self._data[index.row()]
        if row != None and len(row) > 0:
            float_p_value = self.tryFloat(row["p"])
            lang = self._parent._lang

            if role == Qt.DisplayRole:
                if float_p_value > self._parent._filter_p:
                    return  " ".join([row["timeofday"], row["name_" + lang] + "/" + row["name_sci"], row["p"]])

            if role == Qt.DecorationRole:
                if float_p_value > self._parent._filter_p:
                    return QtGui.QColor(self.getColor(float_p_value))

class ResultTable(QTableView):
    def __init__(self, parent, data):
        super().__init__()
        self._parent = parent
        self._model = ResultTableModel(self._parent, data)
        self.setModel(self._model)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

    def hideRows(self):
        for i, data in enumerate(self._model._data):
            if data != None and len(data) > 0:
                p = self._model.tryFloat(data["p"])
                if p < self._parent._filter_p:
                    self.setRowHidden(i, True)
                else:
                    self.setRowHidden(i, False)

    def setData(self, index, data, role):
        count = len(self._model._data)
        self._model._data = data
        self.rowCountChanged(count, count + len(data))
        self.hideRows()
        return False

    def insertData(self, index, data, role):
        new_data = data + self._model._data
        self.setData(index, new_data, role)
        return False