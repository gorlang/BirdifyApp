
from PySide6.QtMultimedia import QAudioFormat
from AppConfig import AppConfig

class AudioFormats():
    def __init__(self):
        self._config = AppConfig()

    def getLowQuality(self):
        format = QAudioFormat()
        format.setSampleRate(self._config.SAMPLE_RATE_LOW)
        format.setChannelCount(self._config.CHANNELS_MONO)
        format.setSampleFormat(QAudioFormat.UInt8)
        return format

    def getHighQuality(self):
        format = QAudioFormat()
        format.setSampleRate(self._config.SAMPLE_RATE_HIGH)
        format.setChannelCount(self._config.CHANNELS_STEREO)
        format.setSampleFormat(QAudioFormat.Int16)
        return format