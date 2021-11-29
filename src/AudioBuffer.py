import math
from Decoder import Decoder
import numpy as np

class AudioBuffer():
    def __init__(self, parent):
        super().__init__()
        self._config = parent._config
        self._decoder = Decoder()
        self._detect_interval_s = self._config.DETECT_INTERVAL_MS/1000
        self._stereo_signal = np.zeros((0,2)) # audio data to analyze
        self._min_detect_samples = math.ceil(self._detect_interval_s * self._config.SAMPLE_RATE_HIGH)

    def update(self, parent):
        if parent._audio_sources._io_device_3 != None:
            data = parent._audio_sources._io_device_3.readAll()
            self._stereo_signal = np.append(self._stereo_signal, self._decoder.decode(data), axis=0)
            if (len(self._stereo_signal) > self._min_detect_samples):
                self._stereo_signal = self._stereo_signal[-self._min_detect_samples:]