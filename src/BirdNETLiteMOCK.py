import time

def parseArgs(args):
    pass

def loadModel():
    pass

def prepareAudioSignal(ig, rate, overlap):
    pass
    
def analyzeAudioData(chunks, lat, lon, week, sensitivity, overlap, interpreter, callbackProgress):
    if (callbackProgress != None):
        print("-------analyzeAudioData, callbackProgress()", "")
        callbackProgress(time.localtime().tm_sec)