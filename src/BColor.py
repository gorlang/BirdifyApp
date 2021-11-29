from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget

class BColor(QWidget):
    
    def __init__(self, color):
        super(BColor, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)