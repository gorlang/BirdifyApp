from PySide6 import QtCore
from PySide6.QtWidgets import QListWidget, QListWidgetItem, QMessageBox

class WidgetDragDropFile(QListWidget):

    fileDropped = QtCore.Signal(list)
    fileSelected = QtCore.Signal(list)

    # def __init__(self, type, parent=None):
    # super(WidgetDragDropFile, self).__init__(parent)
    def __init__(self, parent):
        super().__init__()
        self._config = parent._config
        self.audio_file_types = " or ".join(self._config.AUDIO_FILE_TYPES)
        self.setAcceptDrops(True)
        self.setIconSize(QtCore.QSize(72, 72))
        self.addItem(QListWidgetItem("Drag audio files here!"))
        self.currentTextChanged.connect(self.itemSelected)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def isAudio(self, file_path):
        file_type = file_path.split(".")[-1]
        if file_type in self._config.AUDIO_FILE_TYPES:
            return True
        return False

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                localFile = str(url.toLocalFile())
                if self.isAudio(localFile):
                    links.append(localFile)
                else:
                    QMessageBox.warning(None, "", f"Only files of type {self.audio_file_types} are supported!"),
            self.fileDropped.emit(links)
        else:
            event.ignore()

    def itemSelected(self, item):
        self.fileSelected.emit([item])

