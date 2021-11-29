import datetime
from functools import cmp_to_key
from datetime import datetime as dt
from AppConfig import AppConfig

if not AppConfig().isTest():
    from BirdNETLite import analyzeAudioData, prepareAudioSignal, parseArgs
else:
    from BirdNETLiteMOCK import analyzeAudioData, prepareAudioSignal, parseArgs

def getWeek():
    dtn = dt.now()
    return datetime.date(dtn.year, dtn.month, dtn.day).isocalendar().week

def getTimestamp():
    return dt.now().strftime("%Y-%m-%d %H:%M:%S")

def getDate():
    return getTimestamp().split(" ")[0]

def getTime():
    return getTimestamp().split(" ")[1]

def getNewArgMap(lat, lon, week=None):
    argMap =  {"lat": 0, "lon": 0, "week": getWeek(), "overlap": 0.0}
    if (lat != None):
        argMap["lat"] = lat
    if (lon != None):
        argMap["lon"] = lon
    if (week != None):
        argMap["week"] = week
    return argMap

def parseArgMap(argMap):
    """
    input args as a map {"lat": 1, "lon": 2, "week": 3, "overlap": 0}
    """
    argv = []
    for a in argMap:
        argv.append("--" + a)
        argv.append(str(argMap[a]))
    return argv


def detectSpecies(sig=None, rate=None, argMap=None, interpreter=None, callbackProgress=None):

    parsedArgMap = parseArgMap(argMap)
    args = parseArgs(parsedArgMap)
    if (interpreter == None):
        assert interpreter != None

    audioData = prepareAudioSignal(sig, rate, args.overlap)
    week = max(1, min(args.week, 48))
    sensitivity = max(0.5, min(1.0 - (args.sensitivity - 1.0), 1.5))
    detections = analyzeAudioData(audioData, args.lat, args.lon, week, sensitivity, args.overlap, interpreter, callbackProgress)

    return {"detections": detections, "timestamp": getTimestamp(), "lat": args.lat, "lon": args.lon}


def filterDetections(detections_result, p_limit=0.1, lang="en"):
    count_total = 0
    count = 0
    detections = detections_result["detections"]
    filtered_list = []
    for d in detections:
        detection = detections[d]
        for item in detection:
            count_total += 1
            names, p = item
            if (p > p_limit):
                count += 1
                values = names.split("_")
                filtered_list.append([d, p, values[1], values[0]])
    return {"count_total": count_total, 
            "p_limit": p_limit, 
            "count": count, 
            "filtered_list": filtered_list, 
            "timestamp": detections_result["timestamp"],
            "lat": detections_result["lat"],
            "lon": detections_result["lon"]
            }

def compare_sum(a,b):
    return a[0]-b[0]

def rankResult(filtered_result, desc=True):
    filtered_detections = filtered_result["filtered_list"]
    sci_ix = 3
    sci_names = set(map(lambda x: x[sci_ix], filtered_detections))
    rank_list = []
    for sci_name in sci_names:
        detections_species = list(filter(lambda x: x[sci_ix] == sci_name, filtered_detections))
        p = []
        for d in detections_species:
            p.append(d[1])
        rank_list.append([sum(p), p, detections_species[0][2], detections_species[0][3]])
    rank_list.sort(key=cmp_to_key(compare_sum), reverse=desc)
    return {"ranked_list": rank_list,
            "timestamp": filtered_result["timestamp"], 
            "lat": filtered_result["lat"], 
            "lon": filtered_result["lon"]}
