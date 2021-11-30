import json
import os
from PySide6 import QtCore, QtGui
from PySide6.QtWidgets import QHBoxLayout, QListWidgetItem, QMessageBox, QProgressBar, QProgressDialog, QPushButton, QVBoxLayout, QWidget
from BLabel import BLabel
from SearchTable import SearchTable
from SpectogramWidget import SpectogramWidget
from WidgetDragDropFile import WidgetDragDropFile
from AppLog import Log
log = Log()

class WidgetFiles(QWidget):
    def __init__(self, parent):
        super().__init__()

        self._parent = parent
        self._config = parent._config

        self._selected_file_path = None
        self._file_urls = {}
        self._file_id = 0
        self._parent._detector_file.detect_result.connect(self.updateResultTable)
        self._progress_value = 0
        self._spectogram_list = []

        layout = QVBoxLayout()
        layout.addWidget(BLabel(self._config.BUTTON_IMPORT, 14))
        
        self.view = WidgetDragDropFile(parent)
        self.view.fileDropped.connect(self.fileDropped)
        self.view.fileSelected.connect(self.fileSelected)
        layout.addWidget(self.view, stretch=1)

        # buttons
        layout_h = QHBoxLayout()
        self.button = QPushButton("Run Detection")
        self.button.clicked.connect(self.analyzeFile)

        self.buttonClear = QPushButton("Clear Filelist")
        self.buttonClear.clicked.connect(self.clearFileList)

        layout_h.addWidget(self.button)
        layout_h.addWidget(self.buttonClear)
        layout.addLayout(layout_h)

         # result table
        self.table_size = int(self._config.MAX_FILE_SIZE_SEC/self._config.FILE_DETECT_CHUNK_SEC)
        self.table = SearchTable(parent, ["" for i in range(1, self.table_size)])
        layout.addWidget(self.table, stretch=2)

        # button spectogram
        self.buttonSpectogram = QPushButton("Show Spectogram")
        self.buttonSpectogram.clicked.connect(self.showSpectogram)
        self.buttonSpectogram.setVisible(False)
        layout.addWidget(self.buttonSpectogram)

        # progress bar
        css = []
        css.append("QProgressBar {text-align: center; padding: 1px; background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #bbb, stop: 0.4999 #999, stop: 0.5 #888, stop: 1 #999 ); width: 15px;}")
        css.append("QProgressBar::chunk {background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #777, stop: 0.4999 #444, stop: 0.5 #555, stop: 1 #222 ); border-bottom-right-radius: 1px; border-bottom-left-radius: 0px; border: 0px solid black;}")
        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        self.progressBar.setStyleSheet(" ".join(css))
        self.progressBar.setVisible(False)
        layout.addWidget(self.progressBar)

        # progress label
        self.progressLabel = BLabel("", 10, None, parent._config.COLOR_FONT_DARK)
        self.progressLabel.setVisible(False)
        layout.addWidget(self.progressLabel)

        # footer
        label = BLabel("", 12, None, parent._config.COLOR_FONT_DARK)
        self._parent._footer_labels.append(label)
        layout.addWidget(label)

        self.setLayout(layout)

        # timer for updating progress bar
        self.timer = QtCore.QTimer()
        self.timer.connect(self.timer, QtCore.SIGNAL("timeout()"), self, QtCore.SLOT("updateProgressBar()"))
        self.timer.setInterval(400)

    def addSpectogram(self, spectogram):
        self._spectogram_list.append(spectogram)
        if len(self._spectogram_list) > 2:
            self._spectogram_list.pop(0)

    def getSpectogram(self):
        return self._spectogram_list[-1]

    def getTimeWindow(self, max_slots=10):
        timeslots = []
        for i, selectedIndex in enumerate(self.table.selectedIndexes()):
            if (i < max_slots):
                coldata = selectedIndex.data().split(" ")
                timeslot = coldata[0].replace("s", "").split("-")
                timeslot = list(map(lambda x: int(float(x)), timeslot))
                timeslots.append(timeslot)
        max_sec = max_slots * 3
        start = timeslots[0][0]
        end = timeslots[-1][1]
        if end - start > max_sec:
            return [start, start + max_sec]
        return [start, end]

    def showSpectogram(self, i):
        filepath = self._selected_file_path
        if len(self.table.selectedIndexes()) > 0 and filepath != None:
            timeWindow = self.getTimeWindow()
            self.addSpectogram(SpectogramWidget())
            self.getSpectogram().plot(filepath=filepath, mel_spec=True, window=timeWindow)
            self.getSpectogram().show()
        else:
            QMessageBox.warning(None, "", "No file selected!")

    def emptyResultTable(self):
        data = ["" for i in range(1, self.table_size)]
        self.table.setData(0, data, None)

    def getUniqueFilename(self, url):
        self._file_id += 1
        return str(self._file_id) + ". " + url.split("/")[-1]

    def getIcon(self, name):
        base_path = self._config.BASE_PATH + "icons/"
        icon_path = self._config.ICONS[name]
        return QtGui.QIcon(base_path + icon_path)

    def clearFileList(self):
        self._file_urls = {}
        self.view.clear()

    def fileDropped(self, l):
        for url in l:
            if os.path.exists(url):
                log.debug(url)
                filename = self.getUniqueFilename(url)
                self._file_urls[filename] = url
                self._selected_file_path = url
                item = QListWidgetItem(filename, self.view)
                item.setIcon(self.getIcon(self._config.BUTTON_IMPORT))
                item.setStatusTip(url)
    
    def fileSelected(self, l):
        for filename in l:
            if filename in self._file_urls:
                file_path = self._file_urls[filename]
                if os.path.exists(file_path):
                    self._selected_file_path = file_path

    def toggleVisibility(self, widgetList):
        for w in widgetList:
            w.setVisible(not w.isVisible())

    def updateProgressBar(self):
        value = self._parent._detector_file.getProgress()
        if value == 0:
            self._progress_value += 1
            self.progressLabel.setText("Loading file...")
        else:
            self._progress_value = value
            self.progressLabel.setText("Processing data...")
        self.progressBar.setValue(self._progress_value)
        if value >= 100:
            self.timer.stop()
            self.progressLabel.setText("")
            self.toggleVisibility([self.progressLabel, self.progressBar])
            self.buttonSpectogram.setVisible(True)

    def analyzeFile(self, i):
        log.debug(f"WidgetFiles().analyzeFile(), file={self._selected_file_path}")
        if (self._selected_file_path != None):
            self.emptyResultTable()
            self._progress_value = 0
            self.toggleVisibility([self.progressLabel, self.progressBar])
            self.buttonSpectogram.setVisible(False)
            self.timer.start()
            self._parent._detector_file.detect(1, self._selected_file_path)
        else:
            QMessageBox.warning(None, "", "Select a file to analyze!")

    def updateResultTable(self, result_json):
        items = json.loads(result_json)
        self.table.setData(0, items, None)