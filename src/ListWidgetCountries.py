from PySide6.QtCore import QItemSelectionModel
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget

class ListWidgetCountries(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._countries_df = self._parent._countries.df()
        self.addItems(self._countries_df["name"].sort_values().array)
        self.currentItemChanged.connect(self.index_changed)
        self.currentTextChanged.connect(self.text_changed)
        items = self.findItems(self._parent._country, Qt.MatchContains)
        items[0].setSelected(True)
        self.setCurrentItem(items[0], QItemSelectionModel.ClearAndSelect)
        self.repaint()

    def index_changed(self, item):
        self._parent._country = item
        self._parent.updateSettings()

    def text_changed(self, item):
        self._parent._country = item
        self._parent.updateSettings()

