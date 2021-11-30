import time
from AppLog import Log
log = Log()

def parseArgs(args):
    pass

def loadModel():
    log.debug(f"BirdNETLiteMOCK.loadModel()")
    pass

def prepareAudioSignal(ig, rate, overlap):
    log.debug(f"BirdNETLiteMOCK.prepareAudioSignal()")
    pass
    
def analyzeAudioData(chunks, lat, lon, week, sensitivity, overlap, interpreter, callbackProgress):
    if (callbackProgress != None):
        log.debug(f"BirdNETLiteMOCK.analyzeAudioData, callbackProgress={callbackProgress}")
        callbackProgress(time.localtime().tm_sec)