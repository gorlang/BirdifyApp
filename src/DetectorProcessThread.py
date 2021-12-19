import librosa
from PySide6.QtCore import (QMetaType, Signal, QMutex, QElapsedTimer, QMutexLocker, QThread, QWaitCondition)
from AppConfig import AppConfig
from BirdifyAPI import detectSpecies, filterDetections, getNewArgMap
from Decoder import Decoder
import json
from DetectorUtil import DetectorUtil
from AppLog import Log
log = Log()

if not AppConfig().isTest():
    from BirdNETLite import loadModel
else:
    from BirdNETLiteMOCK import loadModel

NUM_PASSES = 1
DEFAULT_RESULT_SIZE = 10

class DetectorProcessThread(QThread):

    detect_result = Signal(QMetaType.QJsonObject, str) # defines a signal pipline and type

    def __init__(self, parent):
        super().__init__()
        log.debug("DetectorProcessThread().__init__")
        self._parent = parent
        self._result_size = 10
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.restart = False
        self.abort = False
        self._decoder = Decoder()
        self._detector_util = DetectorUtil(parent)
        self._tflite_model = loadModel()

    def stop(self):
        log.debug("Thread().stop()")
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait(2000)

    def detect(self, resultSize):
        locker = QMutexLocker(self.mutex)
        self._result_size = resultSize
        if not self.isRunning():
            self.start(QThread.LowPriority)
        else:
            self.restart = True
            self.condition.wakeOne()

    def parseFilteredList(self, filteredList, ts, row_index=0):
        item = self._detector_util.asDict(filteredList[row_index], ts)
        lang_ref = "name_" + self._parent._lang
        title = f"{item[lang_ref]}/{item['name_sci']}"
        return item, title

    def run(self):
        timer = QElapsedTimer()
        log.debug("Thread().run()")
        while True:
            self.mutex.lock()
            resultSize = self._result_size
            self.mutex.unlock()
            curpass = 0
            max_iterations = 100 # not used
            result = []
            while curpass < NUM_PASSES:
                timer.restart()
                if self.restart:
                    break
                if self.abort:
                    return
                parent = self._parent
                stereo_signal = parent._audio_buffer._stereo_signal
                min_detect_samples = parent._audio_buffer._min_detect_samples
                if (len(stereo_signal) >= min_detect_samples):
                    mono_signal = librosa.util.normalize(stereo_signal.T[0])
                    resultList = filterDetections(
                        detectSpecies(
                        mono_signal, 
                        parent._config.SAMPLE_RATE_DETECT,
                        getNewArgMap(parent._coords[0], parent._coords[1], parent._week),
                        self._tflite_model), 
                        p_limit = parent._config.P_DEFAULT)
                    filteredList = resultList["filtered_list"]
                    if (len(filteredList) > 0):
                        result_dict, title = self.parseFilteredList(filteredList, resultList["timestamp"])
                        result.append(result_dict)
                        parent._amplitude_monitor._chart.setTitle(title)
                    else:
                        parent._amplitude_monitor._chart.setTitle(f"Listening...")
                # print stats and emit result
                if not self.restart:
                    elapsed = timer.elapsed()
                    unit = 'ms'
                    if elapsed > 2000:
                        elapsed /= 1000
                        unit = 's'
                    stats = f"Pass {curpass+1}/{NUM_PASSES}, max iterations: {max_iterations}, time: {elapsed}{unit}"
                    log.debug(stats)
                    if len(result) > 0:
                        self.detect_result.emit(json.dumps(result[0])) # return only first item
                    curpass += 1
            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()