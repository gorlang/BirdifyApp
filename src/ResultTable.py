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
        value = self._data[index.row()]
        values = value.split(" ")
        p_value = values[0]
        float_p_value = self.tryFloat(p_value)

        if role == Qt.DisplayRole:
            if float_p_value > self._parent._filter_p:
                return " ".join(values[1:])

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

    def setData(self, index, data, role):
        count = len(self._model._data)
        self._model._data = data
        self.rowCountChanged(count, count + len(data))
        return False

    def insertData(self, index, data, role):
        #print("insertData(), data=", data)
        new_data = data + self._model._data
        self.setData(index, new_data, role)
        return False