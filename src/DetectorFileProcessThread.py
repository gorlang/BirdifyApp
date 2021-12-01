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

class DetectorFileProcessThread(QThread):

    detect_result = Signal(QMetaType.QJsonObject, str) # defines a signal pipline and type

    def __init__(self, parent):
        super().__init__()
        log.debug("DetectorFileProcessThread().__init__")
        self._parent = parent
        self._result_size = 10
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.restart = False
        self.abort = False
        self._decoder = Decoder()
        self._detector_util = DetectorUtil(parent)
        self._callbackProgress = None
        self._progress = 0
        self._tflite_model = loadModel()

    def setProgress(self, value):
        self._progress = value

    def getProgress(self):
        return self._progress

    def stop(self):
        log.debug("Thread().stop()")
        self.mutex.lock()
        self.abort = True
        self.condition.wakeOne()
        self.mutex.unlock()
        self.wait(2000)

    def detect(self, resultSize=1, file_path=None):
        self.setProgress(0)
        locker = QMutexLocker(self.mutex)
        self._result_size = resultSize
        self._file_path = file_path

        if (file_path != None):
            if not self.isRunning():
                self.start(QThread.LowPriority)
            else:
                self.restart = True
                self.condition.wakeOne()
        else:
            log.debug("No file_path selected = ", file_path)

    def run(self):
        timer = QElapsedTimer()
        log.debug("Thread().run()")
        parent = self._parent
        min_detect_samples = parent._config.MIN_FILE_SIZE_SEC * parent._config.SAMPLE_RATE_DETECT
        while True:
            self.mutex.lock()
            resultSize = self._result_size # not used
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
                mono_signal, sr = librosa.load(
                    self._file_path, 
                    sr=parent._config.SAMPLE_RATE_DETECT,
                    mono = True,
                    duration=parent._config.MAX_FILE_SIZE_SEC, 
                    res_type='kaiser_best')
                if (len(mono_signal) >= min_detect_samples):
                    argMap = getNewArgMap(parent._coords[0], parent._coords[1], parent._week)
                    detections = detectSpecies(
                        mono_signal, 
                        parent._config.SAMPLE_RATE_DETECT,
                        argMap,
                        self._tflite_model,
                        self.setProgress)
                    resultList = filterDetections(detections, p_limit=parent._config.P_DEFAULT)
                    filteredList = resultList["filtered_list"]
                    if (len(filteredList) > 0):
                        for listItem in filteredList:
                            result_dict = self._detector_util.asDict(listItem, resultList["timestamp"], source="file")
                            result.append(result_dict)
                    else:
                        log.debug("no results!")
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
                        self.detect_result.emit(json.dumps(result))
                    curpass += 1
            self.mutex.lock()
            if not self.restart:
                self.condition.wait(self.mutex)
            self.restart = False
            self.mutex.unlock()


