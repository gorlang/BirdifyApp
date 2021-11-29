from PySide6.QtGui import QColor, QPalette, Qt
from AppConfig import AppConfig

class BTheme(QPalette):
    def __init__(self):
        super().__init__()

        self._config = AppConfig()
        self._gray = QColor(self._config.COLOR_FONT)

        self._dark = QPalette()
        self._dark.setColor(QPalette.Window, QColor(43, 43, 43)) #  QColor(53, 53, 53)
        self._dark.setColor(QPalette.WindowText, self._gray) # Qt.white
        self._dark.setColor(QPalette.Base, QColor(33, 33, 33)) # QColor(25, 25, 25)
        self._dark.setColor(QPalette.AlternateBase, QColor(43, 43, 43)) #  QColor(53, 53, 53)
        self._dark.setColor(QPalette.ToolTipBase, Qt.black)
        self._dark.setColor(QPalette.ToolTipText, self._gray) # Qt.white
        self._dark.setColor(QPalette.Text, self._gray) # Qt.white, table text
        self._dark.setColor(QPalette.Button, QColor(53, 53, 53))
        self._dark.setColor(QPalette.ButtonText, self._gray) # Qt.white
        self._dark.setColor(QPalette.BrightText, Qt.red)
        self._dark.setColor(QPalette.Link, QColor(0, 153, 204)) # 42, 130, 218
        self._dark.setColor(QPalette.Highlight, QColor(0, 153, 204)) # 42, 130, 218
        self._dark.setColor(QPalette.HighlightedText, Qt.black)

    def getDark(self):
        return self._dark
