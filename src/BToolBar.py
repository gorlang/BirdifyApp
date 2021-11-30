from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow, QSizePolicy, QToolBar
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt
from AppLog import Log
log = Log()

class BToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._config = parent._config
        self.setIconSize(QSize(24,24))
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) # ToolButtonTextBesideIcon | ToolButtonTextUnderIcon
        for button_name in self._config.BUTTONS:
            button = QAction(QIcon(self.getIcon(button_name)), button_name, self)
            button.triggered.connect(self.toggleView)
            button.setCheckable(True)
            self.addAction(button)

    def getIcon(self, name):
        iconpath = self._config.BASE_PATH + "icons/" + self._config.ICONS[name]
        return iconpath

    def toggleView(self):
        source = self.sender()
        log.debug(f"BToolBar().toggleView(), button={source.text()}")
        self._parent.stacked.setCurrentIndex(self._config.BUTTONS.index(source.text()))
        for a in self.actions():
            a.setChecked(False)
            if a.text() == source.text():
                a.setChecked(True)
