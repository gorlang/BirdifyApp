from PySide6.QtGui import QBrush, QColor
from PySide6.QtCharts import (QBarCategoryAxis, QBarSet, QChart, QHorizontalPercentBarSeries)

class DetectQualityChart(QChart):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self.quality_levels = parent._config.QUALITY_LEVELS
        self.color_scale = parent._config.COLOR_SCALE

        self.setContentsMargins(-12,-12,-12,-12)
        self.setBackgroundRoundness(1)
        self.setBackgroundBrush(QBrush(QColor(parent._config.COLOR_BG)))
        self.setAnimationOptions(QChart.SeriesAnimations)
        series = self.update([0,0,0,0])
    
        categories = ["Quality"]
        axis = QBarCategoryAxis()
        axis.append(categories)
        self.createDefaultAxes()
        self.setAxisY(axis, series)

        self.legend().setVisible(False)
        self.axisY().setVisible(False)
        self.axisX().setVisible(False)
        self.setTitleBrush(QBrush(QColor(parent._config.COLOR_FONT)))
        self.setTitle("Detect Quality (60s)")

    def update(self, data):
        data_sets = []
        for i, quality_level in enumerate(self.quality_levels):
            qbs = QBarSet(quality_level)
            qbs.append(data[i])
            qbs.setColor(self.color_scale[i])
            qbs.setBorderColor(QColor(self._parent._config.COLOR_BG))
            data_sets.append(qbs)
        series = QHorizontalPercentBarSeries()
        for s in data_sets:
            series.append(s)
        self.removeAllSeries()
        self.addSeries(series)
        return series