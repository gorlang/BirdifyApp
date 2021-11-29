import sys
from PySide6.QtCore import SLOT, QTimer
sys.path.append('src')
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from AppConfig import AppConfig
from AudioBuffer import AudioBuffer
from DetectorFileProcessThread import DetectorFileProcessThread
from Species import Species
import pandas as pd
from BirdNETLite import loadModel

class MockParent():
    def __init__(self):
        super().__init__()
        self._config = AppConfig()
        df_species = pd.read_csv( self._config.BASE_PATH + "data/species_list.csv")
        self._species = Species(df_species)
        self._tflite_model = loadModel()
        self._coords = [60.128161,18.643501] # sweden
        self._week = 20
        self._country = "Sweden"

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        print("MainWindow()")
        #self._file_path =  "/Users/green/Music/Music/Media.localized/Tättingläten/Tättingläten/65 svartmes.mp3"
        self._file_path = "/Users/green/Music/Music/Media.localized/Göran/Görans album/SOUNDSCAPE.mp3"
        self._detector = DetectorFileProcessThread(MockParent())
        self._detector.detect_result.connect(self.updateDetected)
        QTimer.singleShot(100, self, SLOT("detect()"))

    def updateDetected(self, result_json):
        items = json.loads(result_json)
        print("updateDetected()")
        result = ""
        for item in items:
            result += " ".join([item["start"], "-", item["end"], item["name_sv"], item["p"]])
            result += "\n"
        #QMessageBox.information(None, f"msg", result)
        print("---result---")
        print(result)

    def detect(self):
        self._detector.detect(1, self._file_path)

    
if __name__ == "__main__":
    
    config = AppConfig()
    app = QApplication(sys.argv)
    main_win = MainWindow(config)
    #main_win.show()
    r = app.exec()
    main_win._detector.stop()
    sys.exit(r)