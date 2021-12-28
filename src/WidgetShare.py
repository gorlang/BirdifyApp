import json
from datetime import datetime as dt

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout, QWidget
from AppConfig import AppConfig
from AppLog import Log
from BLabel import BLabel
from PFilterDial import PFilterDial
from SearchTable import SearchTable
from WidgetUtil import asDataFrame, dfToJson
from AppLog import Log
log = Log()

class WidgetShare(QWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self._json_data = None

        self._filter_p = 0.5 # if has value => use this ref in PFilterDial()

        # used for dev/test
        if AppConfig().isTest():
            ts = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            self._parent._stats._detect_stats = [{"timestamp": ts, "p": 0.3, "name_sci":"sciname1", "name_sv": "Baratt's warbler", "name_en": "Baratt's warbler"}, {"timestamp": ts, "p": 0.5, "name_sci":"sciname2", "name_sv": "bofink", "name_en": "booofink"}, {"timestamp": ts, "p": 1, "name_sci":"sciname2", "name_sv": "bofink", "name_en": "booofink"}]
      
        layout = QVBoxLayout()
        for value in [parent._site_name]:
            label = BLabel(value, 14)
            self._parent._share_labels.append(label)
            layout.addWidget(label)
        
        self.table = SearchTable(parent, ["" for i in range(1,100)])
        layout.addWidget(self.table)

        # search buttons - start
        layout_buttons_search = QHBoxLayout()
        search_button_1 = QPushButton("Google Search")
        search_button_1.clicked.connect(self.doGoogleSearch)
        layout_buttons_search.addWidget(search_button_1)

        search_button_2 = QPushButton("Xeno-Canto Search")
        search_button_2.clicked.connect(self.doXenoCantoSearch)
        layout_buttons_search.addWidget(search_button_2)
        layout.addLayout(layout_buttons_search)
        # search buttons - end

        self._label_filter_dial = BLabel(parent._config.DIAL_FILTER_P + "=" + str(self._filter_p), 14)
        layout.addWidget(self._label_filter_dial)
        layout.addWidget(PFilterDial(parent, self))
        
        layout_buttons = QHBoxLayout()
        button_refresh = QPushButton("Refresh List")
        button_refresh.clicked.connect(self.updateList)
        layout_buttons.addWidget(button_refresh)

        button = QPushButton("Share!")
        button.clicked.connect(self.share)
        layout_buttons.addWidget(button)

        layout.addLayout(layout_buttons)

        # footer
        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        self._parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)

        self.updateList()

    def getTopList(self, df, lang):
        col_names = list(map(lambda x: "name_" + x, self._parent._config.LANGS))
        df_result = df.groupby(col_names).max("p").sort_values(["p"], ascending=False)
        df_result = df_result[df_result["p"] > self._filter_p]
        return dfToJson(df_result)

    def updateList(self):
        stats = self._parent._stats._detect_stats
        if len(stats) > 0:
            df = asDataFrame(stats)
            self._json_data = self.getTopList(df, self._parent._lang)
            self.table.setData(0, self._json_data, None)
            log.debug(f"self._json_data={self._json_data}")
        else:
            self.table.setData(0, [], None)

    def getSelectedNames(self):
        selectedNames = {}
        for i, selectedIndex in enumerate(self.table.selectedIndexes()):
            name = " ".join(selectedIndex.data().split(" ")[0:-1])
            selectedNames[name] = name
        return selectedNames

    def getQueryUrl(self, baseUrl, site_name, site_url, country):
        selectedNamesLookup = self.getSelectedNames()
        json_out = []
        for item in self._json_data:
            name_lang = "name_" + self._parent._lang
            if item[name_lang] in selectedNamesLookup:
                item["site"] = site_name
                item["url"] = site_url
                item["country"] = country
                json_out.append(json.dumps(item))
        json_str = "".join(["[", ",".join(json_out), "]"])
        return baseUrl + "?json=" + json_str

    def share(self):
        if self._json_data != None and len(self._json_data) > 0:
            if len(self.table.selectedIndexes()) > 0:
                url = self.getQueryUrl(
                    self._parent._config.BIRDIFY_WEB_URL,
                    self._parent._site_name, 
                    self._parent._site_url,
                    self._parent._country
                    )
                #log.info(f"url={url}")
                QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))
            else:
                QMessageBox.warning(None, "", "Select one or more species to share!")
        else:
            QMessageBox.warning(None, "", "Species list is empty!")

    def getSelectedNames(self):
        selectedNames = []
        for i, selectedIndex in enumerate(self.table.selectedIndexes()):
            if selectedIndex.data() != None:
                words = selectedIndex.data().split(" ")[0:-1]
                name = " ".join(words)
                selectedNames.append(name)
        return selectedNames

    def doGoogleSearch(self):
        names = self.getSelectedNames()
        if len(names) > 0:
            search_url = "https://www.google.com/search?q="
            search_str = '"' +  names[0] + '"'
            log.info(f"search_str={search_str}")
            QDesktopServices.openUrl(QUrl(search_url + search_str, QUrl.TolerantMode))
        else:
            QMessageBox.warning(None, "", "Select a species!")

    def doXenoCantoSearch(self):
        names = self.getSelectedNames()
        if len(names) > 0:
            search_url = "https://xeno-canto.org/explore?query="
            search_str = names[0]
            log.info(f"search_str={search_str}")
            QDesktopServices.openUrl(QUrl(search_url + search_str, QUrl.TolerantMode))
        else:
            QMessageBox.warning(None, "", "Select a species!")