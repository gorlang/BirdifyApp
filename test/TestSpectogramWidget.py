import sys
sys.path.append('src')
from PySide6.QtWidgets import QApplication
from SpectogramWidget import SpectogramWidget
from AppConfig import AppConfig
from BTheme import BTheme

class ParentMock():
    def __init__(self):
        super().__init__()
        self._config = AppConfig()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(BTheme().getDark())

    w = SpectogramWidget()
    file = "/Users/green/Music/Music/Media.localized/Tättingläten/Tättingläten/65 svartmes.mp3"
    file = "/Users/green/Music/Music/Media.localized/Tättingläten/Tättingläten/44 lundsångare.mp3"
    w.plot(filepath=file, mel_spec=True, window=[4,15])
    w.show()
    sys.exit(app.exec())