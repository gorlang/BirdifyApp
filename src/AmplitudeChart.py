from PySide6.QtCharts import QChart, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF
from PySide6.QtGui import QBrush, QColor, QPen

class AmplitudeChart(QChart):
    def __init__(self, config):
        super().__init__()

        color_grid = QColor(config.COLOR_GRID)
        self.setTitleBrush(QBrush(QColor(config.COLOR_FONT)))
        self._series = QLineSeries()

        self.setContentsMargins(-12,-12,-12,-12)
        self.setBackgroundRoundness(10)
        self.setBackgroundBrush(QBrush(QColor(config.COLOR_BG)))

        pen = QPen(config.COLOR_GREEN)
        self._series.setPen(pen)

        self.addSeries(self._series)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, config.SAMPLE_COUNT)
        self._axis_x.setLabelFormat("%g")
        self._axis_x.setTitleText("Samples")
        self._axis_x.setGridLineColor(color_grid)
        self._axis_x.setVisible(False)
    
        self._axis_y = QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setTitleText("Audio level")
        self._axis_y.setGridLineColor(color_grid)
        self._axis_y.setVisible(False)

        self.setAxisX(self._axis_x, self._series)
        self.setAxisY(self._axis_y, self._series)
        self.legend().hide()
        self.setTitle("")
