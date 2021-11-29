from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PySide6.QtWidgets import (QWidget, QHBoxLayout)
import librosa
import librosa.display

from AppConfig import AppConfig

class SpectogramWidget(QWidget):
    def __init__(self):
        super().__init__()

        config = AppConfig()
        self._hide_axes = False
        self._font_small = 9
        self._font_large = 10
        self._color = config.COLOR_FONT_DARK
        self._bg_color = config.COLOR_BG

        fig = Figure(figsize=(6, 4))
        fig.set_facecolor("none")
        if self._hide_axes:
            fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
        self.view = FigureCanvas(fig)

        self.view.setStyleSheet(f"background-color:{self._bg_color};")

        self.axes = self.view.figure.subplots()
        self.axes.xaxis.label.set_color(self._color)
        self.axes.yaxis.label.set_color(self._color)
        self.axes.spines['bottom'].set_color(self._color)
        self.axes.spines['left'].set_color(self._color)
        self.axes.tick_params(axis='both', colors=self._color)
        self.axes.tick_params(axis='both', labelsize=self._font_small)
        self.axes.title.set_color(self._color)

        layout = QHBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def plot(self, filepath=None, mel_spec=True, window=None):

        offset = 0 if window == None else window[0]
        duration = 3 if window == None else window[1]-window[0]

        xc, sr = librosa.load(filepath, offset=offset, duration=duration, res_type='kaiser_best')
        X = librosa.feature.melspectrogram(y=xc, sr=sr) if mel_spec else librosa.stft(xc)
        Xdb = librosa.amplitude_to_db(abs(X))
        librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz', ax=self.axes)

        title = filepath.split("/")[-1]
        self.axes.set_title(f"{title} ({window[0]}-{window[1]}s)", fontsize=self._font_large)
        self.axes.set_xlabel("Time (s)", fontsize=self._font_small)
        self.axes.set_ylabel("Frequency (Hz)", fontsize=self._font_small)
