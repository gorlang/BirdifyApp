from PySide6.QtCore import QItemSelectionModel
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget

class ListWidgetLangs(QListWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self._langs = parent._config.LANGS
        self.addItems(self._langs)
        
        self.currentItemChanged.connect(self.index_changed)
        self.currentTextChanged.connect(self.text_changed)

        items = self.findItems(self._parent._lang, Qt.MatchContains)
        items[0].setSelected(True)
        self.setCurrentItem(items[0], QItemSelectionModel.ClearAndSelect)
        self.repaint()

    def index_changed(self, item):
        pass

    def text_changed(self, item):
        self._parent._lang = item
        self._parent.updateSettings()