import sys
sys.path.append('src')
from datetime import datetime as dt
from AppConfig import AppConfig
from Stats import Stats

class MockChart():
    def __init__(self):
        self.update = lambda x: print("MockChart().update()")

class MockParent():
    def __init__(self):
        super().__init__()
        self._config = AppConfig()
        self._detect_quality_chart = MockChart()

class TestStats():
    def __init__(self):
        super().__init__()
        self.stats = Stats(MockParent())
        ts = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats._detect_stats = [{"timestamp": ts, "p": 0.3, "name_sv": "bofink"}, {"timestamp": ts, "p": 0, "name_sv": "bofink"}, {"timestamp": ts, "p": 1, "name_sv": "bofink"}]
       
    def test_calcDetectQuality(self):
        self.stats.calcDetectQuality()
        result = self.stats._detect_quality_stats
        expected = [1,1,0,1]
        print("result=",result, "expected=", expected)
        assert expected == result


if __name__ == "__main__":
    t = TestStats()
    t.test_calcDetectQuality()
