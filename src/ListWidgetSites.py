from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget

class ListWidgetSites(QListWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._sites_df = self._parent._sites.df()
        self.addItems(self._sites_df["name"].sort_values().values)

        self.currentItemChanged.connect(self.index_changed)
        self.currentTextChanged.connect(self.text_changed)

        items = self.findItems(self._parent._site_name, Qt.MatchContains)
        items[0].setSelected(True)

    def index_changed(self, item):
        pass

    def text_changed(self, item):
        self._parent._site_name = item
        site = self._parent._sites.findByName(item)
        self._parent._site_url = site["url"].values[0]
        self._parent._country = site["country"].values[0]
        self._parent.updateSettings()
