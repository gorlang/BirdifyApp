from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from BLabel import BLabel
from PySide6.QtCore import Qt

class WidgetAbout(QWidget):
    def __init__(self, parent):
        super().__init__()       
        self._config = parent._config

        logo = "birdify-logo-4-2.png"
        imgpath = self._config.BASE_PATH + "icons/" + logo
        label_img = QLabel()
        label_img.setPixmap(QPixmap(imgpath))

        layout_img = QHBoxLayout()
        layout_img.setAlignment(Qt.AlignCenter)
        layout_img.addWidget(label_img)

        layout = QVBoxLayout()
        layout.addLayout(layout_img, stretch=2)
        layout.addWidget(BLabel("Birdify!", 14))
        layout.addWidget(BLabel("Version " + self._config.VERSION, 14))
        layout.addWidget(BLabel("", 14), stretch=2)

        self.setLayout(layout)