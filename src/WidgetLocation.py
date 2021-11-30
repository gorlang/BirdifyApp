from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from BLabel import BLabel
from ListWidgetCountries import ListWidgetCountries
from ListWidgetSites import ListWidgetSites

class WidgetLocation(QWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        layout = QVBoxLayout()

        layout.addWidget(BLabel("Country", 14))
        layout.addWidget(ListWidgetCountries(parent))

        layout.addWidget(BLabel("Site", 14))
        layout.addWidget(ListWidgetSites(parent))

        button = QPushButton("Open Nature Live Stream in External Web-Browser")
        button.clicked.connect(self.openSite)
        layout.addWidget(button)

        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        self._parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)
    
    def openSite(self):
        url = self._parent._site_url
        if url != None and url != "":
            QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))
        else:
            log.debug("No url!")