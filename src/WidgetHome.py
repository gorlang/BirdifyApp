from PySide6.QtCharts import QChartView
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QVBoxLayout, QWidget
from BLabel import BLabel
from DetectedChart import DetectedChart
from DetectQualityChart import DetectQualityChart

class WidgetHome(QWidget):
    def __init__(self, parent):
        super().__init__()

        layout = QVBoxLayout()
        parent._home_label_top = BLabel("", 12)
        layout.addWidget(parent._home_label_top)
        layout.addWidget(parent._amplitude_monitor._chart_view, stretch=2)

        parent._most_freq_chart = DetectedChart(parent)
        chart_view = QChartView(parent._most_freq_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view, stretch=3)

        parent._detect_quality_chart = DetectQualityChart(parent)
        quality_chart_view = QChartView(parent._detect_quality_chart)
        quality_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(quality_chart_view, stretch=1)

        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)