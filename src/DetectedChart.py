from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtGui import QBrush, QColor, QPainter, Qt
from PySide6.QtGui import QPen
from functools import cmp_to_key

class DetectedChart(QChart):

    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._config = parent._config

        self.setTitleBrush(QBrush(QColor(self._config.COLOR_FONT)))
        self.setBackgroundBrush(QBrush(QColor(self._config.COLOR_BG)))
        self._series = QPieSeries()
        self.addSeries(self._series)
        self.setTitle(f'Species Distribution (30s)')
        self.legend().hide()
        self.zoom(1.5)

    def setSlices(self, rank_index):
        if len(rank_index) > 0:
            index = rank_index[0][1]
            for s in self._series.slices():
                s.setPen(QPen(QColor(self._config.COLOR_BG), 0))
            slice = self._series.slices()[index]
            slice.setExploded()
            slice.setPen(QPen(Qt.magenta, 3))
            slice.setBrush(Qt.magenta)
            for i, values in enumerate(rank_index):
                if i < 2:
                    slice2 = self._series.slices()[values[1]]
                    slice2.setLabelVisible()
                    slice2.setLabelColor(QColor(self._config.COLOR_FONT))


    def update(self):
        self._series.clear()
        latest_stats = self._parent._stats._most_freq_stats[-1]
        rank_index = []
        for i, item in enumerate(latest_stats):
            value = latest_stats[item]
            rank_index.append([value, i])
            self._series.append(item, value)
        rank_index = sorted(rank_index, reverse=True)
        self.setSlices(rank_index)