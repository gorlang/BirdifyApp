from AudioSources import AudioSources
from BTimer import BTimer
from AppLog import Log
log = Log()

class AppController():
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._audio_sources = AudioSources(parent)
        self._timers = []
        self._detection_on = False
        self._audio_on = False

    def startDetection(self):
        config = self._parent._config
        self.stopDetection()
        self._timers.append(BTimer(self._parent, "detect()", config.DETECT_INTERVAL_MS))
        self._timers.append(BTimer(self._parent, "updateAmplitudeChart()", config.CHART_REFRESH_RATE_MS))
        self._timers.append(BTimer(self._parent, "updateBuffer()", config.DETECT_BUFFFER_REFRESH_RATE))
        self._timers.append(BTimer(self._parent, "updateQualityStats()", config.STATS_QUALITY_REFRESH_RATE))
        self._detection_on = True

    def stopDetection(self):
        for timer in self._timers:
            timer.stop()
        self._timers = []
        self._detection_on = False

    def startAudio(self):
        try:
            self._audio_sources.connectAll()
            self._audio_sources.startAll()
            self._audio_on = True
            log.debug("Audio connection success!")
        except:
            log.debug("Audio connection failed!")

    def stopAudio(self):
        try:
            self._audio_sources.stopAll()
            self._audio_on = False
            log.debug("Audio connections stopped!")
        except:
            log.debug("Audio connections failed to stop!")
