import sys
import pandas as pd
import json
from PySide6 import QtCore
from PySide6.QtCore import SIGNAL, SLOT, Slot, qWarning
from PySide6.QtMultimedia import QAudio
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from AmplitudeMonitor import AmplitudeMonitor
from AppConfig import AppConfig
from AppController import AppController
from AudioBuffer import AudioBuffer
from AudioDevices import AudioDevices
from BLabel import BLabel
from BStackedWidget import BStackedWidget
from BToolBar import BToolBar
from BTheme import BTheme
from BirdifyAPI import getWeek
from DetectorFileProcessThread import DetectorFileProcessThread
from DetectorProcessThread import DetectorProcessThread
from Sites import Sites
from Species import Species
from Countries import Countries
from Stats import Stats
from AppLog import Log
log = Log()

class MainWindow(QMainWindow):
    def __init__(self, config, device_in, device_out, df_species, df_countries, df_sites):
        super().__init__()
        self._config = config
        self._device_in = device_in
        self._device_out = device_out
        self._species = Species(df_species)
        self._countries = Countries(df_countries)
        self._sites = Sites(df_sites)
        self._stats = Stats(self)
        self._country = "South Africa"
        self._site_name = "Africam Tembe Elephant Park"
        self._site_url = "https://www.youtube.com/watch?v=2bV6sJFixFI"
        self._lang = "en"
        self._coords = self._countries.getCoords(self._country)
        self._current_week = getWeek()
        self._week = self._current_week
        self._filter_p = 0.1
        self._footer_labels = []
        self._share_labels = []
        self._detect_counter = 0
        self._result_size = 10 # not used at the moment

        self._app_controller = AppController(self)
        self._audio_sources = self._app_controller._audio_sources
        self._audio_buffer = AudioBuffer(self)
        self._amplitude_monitor = AmplitudeMonitor(self)
        self._detector = DetectorProcessThread(self)
        self._detector.detect_result.connect(self.updateDetected)
        self._detector_file = DetectorFileProcessThread(self)

        if not AppConfig().isTest():
            self._app_controller.startAudio()
            self._app_controller.startDetection()
        else:
            pass
        
        self.addToolBar(QtCore.Qt.LeftToolBarArea, BToolBar(self))
        self.stacked = BStackedWidget(self)
        self.setCentralWidget(self.stacked)

        log.info(f"BirdifyAppGUI().MainWindow(), app started, TEST={AppConfig().isTest()}")

    def updateQualityStats(self):
        self._stats.calcDetectQuality()

    def updateFooterLabels(self, txt):
        for label in self._footer_labels:
            label.setText(txt)
        values = [self._site_name]
        for i, label in enumerate(self._share_labels):
            label.setText(values[i])

    def updateSettings(self):
        coords_site = self._sites.getCoords(self._site_name)
        if coords_site != None:
            self._coords = coords_site
        else:
            self._coords = self._countries.getCoords(self._country)
        coords = f"Lat={self._coords[0]}, Lon={self._coords[1]}"
        footer_txt = f"{self._country}, w{self._week}, {coords}"
        self.updateFooterLabels(footer_txt)

    def updateDetected(self, result_json):
        self._detect_counter += 1
        item = json.loads(result_json)
        self._result_table.insertData(0, [item], None)
        self._stats.addDetected(item)
        self._stats.calcMostFreq()

    def clearDetected(self):
        self._stats.clearDetected()
        self._result_table.setData(0, [], None)
        log.info("Detected cleared!")

    @Slot()
    def detect(self):
        self._detector.detect(self._result_size)

    @Slot()
    def updateBuffer(self):
        self._audio_buffer.update(self)

    def closeEvent(self, event):
        self._audio_sources.stopAll()
        event.accept()
        log.info("BirdifyAppGUI().closeEvent(), closing audio devices.")

    state_map = {
        QAudio.ActiveState: "ActiveState",
        QAudio.SuspendedState: "SuspendedState",
        QAudio.StoppedState: "StoppedState",
        QAudio.IdleState: "IdleState"}
    
    @Slot(QAudio.State)
    def handle_state_changed(self, state):
        state = self.state_map.get(state, 'Unknown')
        log.debug(f"state = {state}")

    @Slot()
    def updateAmplitudeChart(self):
        self._amplitude_monitor.update()


if __name__ == "__main__":

    log.info("BirdifyAppGUI().__main__, starting app!")
    
    config = AppConfig()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    theme = BTheme().getDark() if config.THEME == "DARK" else BTheme().getFugue()
    app.setPalette(theme)

    input = AudioDevices(config).getExistingDeviceIn()
    if input == None:
        QMessageBox.warning(None, f"No Suitable audio", "INPUT device {config.DEVICE_NAMES_IN} is available. Connect it and restart.")
        sys.exit(-1)
    
    output = AudioDevices(config).getExistingDeviceOut()
    output_name = output.description()
    if output == None:
        QMessageBox.warning(None, "audio", f"No suitable OUTPUT device {config.DEVICE_NAMES_OUT} is avaialble. Connect it and restart.")
        sys.exit(-1)
    elif output_name == 'Built-in Output':
        QMessageBox.information(None, "audio", f"Selected ouput is {output_name}. Verify that headphones are connected!")
      

    log.info("BirdifyAppGUI(), loading data...")

    df_species = pd.read_csv(config.BASE_PATH + "data/species_list.csv")
    df_countries = pd.read_csv(config.BASE_PATH + "data/countries.csv")
    df_sites = pd.read_csv(config.BASE_PATH + "data/sites.csv")

    main_win = MainWindow(config, input, output, df_species, df_countries, df_sites)
    main_win.setWindowTitle(config.APP_NAME)

    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * config.WINDOW_SIZE_SCALE
    main_win.resize(size, size)

    main_win.show()
    r = app.exec()
    main_win._detector.stop()
    main_win._detector_file.stop()
    sys.exit(r)