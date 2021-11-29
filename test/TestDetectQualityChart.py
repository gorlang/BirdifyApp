import sys
sys.path.append('src')
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QMainWindow, QApplication)
from AppConfig import AppConfig
from PySide6.QtCharts import QChartView

from DetectQualityChart import DetectQualityChart

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    config = AppConfig()
    w = MainWindow()
    w._config = config
    c = DetectQualityChart(w)
    chart_view = QChartView(c)
    chart_view.setRenderHint(QPainter.Antialiasing)
    w.setCentralWidget(chart_view)
    w.resize(420, 300)
    w.show()
    c.removeAllSeries()
    c.update([80,10,10,0])
    sys.exit(app.exec())