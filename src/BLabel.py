        
from PySide6.QtWidgets import QLabel, QWidget
from PySide6.QtGui import QColor, QPalette, Qt

from BTheme import BTheme

class BLabel(QLabel):
    def __init__(self, text, size, bgcolor=None, color=None):
        super().__init__()
        self.setText(text)
        font = self.font()
        font.setPointSize(size)   
        self.setFont(font)
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setAutoFillBackground(True)
        style = []
        if bgcolor != None:
            style.append("QLabel {background-color:" + bgcolor + "}")
        if color != None:
            style.append("QLabel {color:" + color + "}")
        self.setStyleSheet("".join(style))
