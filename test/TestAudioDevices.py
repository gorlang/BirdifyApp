import sys
sys.path.append('src')

from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtMultimedia import QAudio, QAudioSink, QAudioSource

from AppConfig import AppConfig
from AudioFormats import AudioFormats
from AudioDevices import AudioDevices

class MainWindow(QMainWindow):
    def __init__(self, device_in, device_out):
        super().__init__()

        print("MainWindow(), device_in=", device_in, "device_in=", device_in)

        self._audio_input_1 = QAudioSource(device_in, AudioFormats().getHighQuality(), self)
        print("self._audio_input_1", self._audio_input_1)

        self._audio_output_1 = QAudioSource(device_out, AudioFormat().getHighQuality(), self)
        print("self._audio_output_1", self._audio_output_1)

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    config = AppConfig()

    input = AudioDevices(config).getExistingDeviceIn()
    if input == None:
        QMessageBox.warning(None, "audio", "There is no suitable audio INPUT device available (VB-Cable).")
        sys.exit(-1)

    output = AudioDevices(config).getExistingDeviceOut()
    if output == None:
        QMessageBox.warning(None, "audio", "There is no suitable audio OUTPUT device available (Raindrops or Built-In).")
        sys.exit(-1)

    main_win = MainWindow(input, output)

    main_win.setWindowTitle("in=" + input.description() + " out=" + output.description())
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 0.5
    main_win.resize(size, size)
    main_win.show()
    r = app.exec()
    sys.exit(r)
    