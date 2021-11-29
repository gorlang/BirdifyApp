""" For test purpose only """

import sys
from AppConfig import AppConfig
from PySide6.QtWidgets import QApplication, QMainWindow

app = QApplication(sys.argv)
class MainWindowMOCK(QMainWindow):
    def __init__(self):
        super().__init__()
        self._config = AppConfig()

