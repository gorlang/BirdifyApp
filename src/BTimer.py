from PySide6 import QtCore

class BTimer(QtCore.QTimer):
    def __init__(self, parent, callee, interval):
        super().__init__(parent)
        self.connect(self, QtCore.SIGNAL("timeout()"), parent, QtCore.SLOT(callee))
        self.start(interval)