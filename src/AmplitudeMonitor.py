from PySide6.QtCharts import QChartView
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPen
from AmplitudeChart import AmplitudeChart


class AmplitudeMonitor():
    def __init__(self, parent):
        super().__init__()
        self._config = parent._config
        self._parent = parent

        self._chart = AmplitudeChart(self._config)
        self._chart_view = QChartView(self._chart)
        self._buffer = [QPointF(x, 0) for x in range(self._config.SAMPLE_COUNT)]
        self._chart._series.append(self._buffer)

    def update(self):
        
        config = self._config
        data = self._parent._audio_sources._io_device_1.readAll()
        available_samples = data.size()
        start = 0

        if (available_samples < config.SAMPLE_COUNT):
            start = config.SAMPLE_COUNT - available_samples
            for s in range(start):
                self._buffer[s].setY(self._buffer[s + available_samples].y())

        data_index = 0
        for s in range(start, config.SAMPLE_COUNT):
            value = (ord(data[data_index]) - 128) / 128
            self._buffer[s].setY(value)
            data_index = data_index + config.RESOLUTION
            if (data_index > len(data)-1):
                data_index = 0
        
        self._chart._series.replace(self._buffer)
        sound_level = sum(list(map(lambda item: abs(item.y()), self._chart._series.points()[-config.LEVEL_SAMPLES:])))/config.LEVEL_SCALE
        color = config.COLOR_RED if sound_level > 1 else config.COLOR_GREEN
        self._chart._series.setPen(QPen(color))