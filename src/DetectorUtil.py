class DetectorUtil():
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

    def asDict(self, item, ts, source="live"):
        time_slot = item[0].split(";")
        return {"name_sci": item[3], 
                "name_en": item[2],
                "name_sv": self._parent._species.translate(item[3]),
                "start": time_slot[0],
                "end": time_slot[1],
                "p": str(round(item[1], 3)),
                "timestamp": ts,
                "timeofday": ts.split(" ")[1],
                "date": ts.split(" ")[0],
                "country": self._parent._country,
                "source": source
                }
