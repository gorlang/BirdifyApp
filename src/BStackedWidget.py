from PySide6.QtWidgets import QStackedWidget
from WidgetHome import WidgetHome
from WidgetLibrary import WidgetLibrary
from WidgetLocation import WidgetLocation
from WidgetSearch import WidgetSearch
from WidgetSettings import WidgetSettings
from WidgetFiles import WidgetFiles
from WidgetShare import WidgetShare

class BStackedWidget(QStackedWidget):
    def __init__(self, parent):
        super().__init__()
        self.addWidget(WidgetHome(parent))
        self.addWidget(WidgetLibrary(parent))
        self.addWidget(WidgetSearch(parent))
        self.addWidget(WidgetLocation(parent))
        self.addWidget(WidgetShare(parent))
        self.addWidget(WidgetFiles(parent))
        self.addWidget(WidgetSettings(parent))
        self.setCurrentIndex(0)