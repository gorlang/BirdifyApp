import sys
sys.path.append('src')
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import (QComboBox, QMainWindow, QApplication)
from AppConfig import AppConfig
from PySide6.QtCharts import QChartView

from DetectQualityChart import DetectQualityChart

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def selectionChanged(self, item_name):
        print("changeEvent(), item_name=", item_name)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    config = AppConfig()
    w = MainWindow()
    w._config = config
   
    selectList = QComboBox()
    selectList.addItems(["optionA", "optionB"])
    selectList.currentTextChanged.connect(w.selectionChanged)

    w.setCentralWidget(selectList)
    w.resize(420, 300)
    w.show()
  
    sys.exit(app.exec())