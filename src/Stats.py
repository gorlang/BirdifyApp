from datetime import datetime as dt
from datetime import timedelta

class Stats():
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._most_freq_stats = []
        self._detect_stats = []
        self._most_freq_stats_secs = 30
        self._detect_quality_stats_secs = 60
        self._q_steps = len(self._parent._config.QUALITY_LEVELS)
        self._q_range = [s/self._q_steps for s in range(1, self._q_steps + 1)]
        self._detect_quality_stats = [0 for s in range(0, self._q_steps)]

    def addDetected(self, item):
        self._detect_stats.append(item)

    def calcMostFreq(self):
        parent = self._parent
        if len(self._detect_stats) > 0:
            end = dt.now() - timedelta(seconds=self._most_freq_stats_secs)
            t_minus_30 = end.strftime("%Y-%m-%d %H:%M:%S")
            top_items = list(filter(lambda x: x["timestamp"] > t_minus_30 and float(x["p"]) > parent._filter_p, self._detect_stats))
            top_list = {}
            for item in top_items:
                name = item["name_" + self._parent._lang]
                if not name in top_list:
                    top_list[name] = 1
                else:
                    top_list[name] += 1
            self._most_freq_stats.append(top_list)
            if len(self._most_freq_stats) > 120:
                self._most_freq_stats.pop(0)
            self._parent._most_freq_chart.update()

    def calcDetectQuality(self):
        if len(self._detect_stats) > 0:
            end = dt.now() - timedelta(seconds=self._detect_quality_stats_secs)
            t_minus_60 = end.strftime("%Y-%m-%d %H:%M:%S")
            items = list(filter(lambda x: x["timestamp"] > t_minus_60, self._detect_stats))
            self._detect_quality_stats = [0 for s in range(0, self._q_steps)]
            for p_value in list(map(lambda x: float(x["p"]), items)):
                for i, q_step in enumerate(self._q_range):
                    if p_value <= q_step:
                        self._detect_quality_stats[i] += 1
                        break
            self._parent._detect_quality_chart.update(self._detect_quality_stats)

