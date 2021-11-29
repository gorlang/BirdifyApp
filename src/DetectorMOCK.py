import json
from PySide6.QtCore import QMetaType, Signal, Slot
import random
from BirdifyAPI import rankResult

#
# MOCK Class for development
#

class DetectorMOCK():

    #detect_result = Signal(QMetaType.QJsonObject, str) # defines a signal pipline and type

    def __init__(self, parent):
        self._parent = parent

    @Slot()
    def detect(self, result_size, file_path):
        parent = self._parent
        MOCK_DATA = [
            [{'ranked_list': [[1.6691264510154724, [0.5070121, 0.5206054, 0.64150894], 'Thrush Nightingale', 'Luscinia luscinia'], [0.7542640566825867, [0.75426406], 'Willow Warbler', 'Phylloscopus trochilus']], 'timestamp': '2021-11-20 19:17:17', 'lat': 59.334591, 'lon': 18.06324}],
            [{'ranked_list': [[5.408018946647644, [0.90090543, 0.5295538, 0.969927, 0.7071651, 0.8291179, 0.9254608, 0.5458889], 'Hawfinch', 'Coccothraustes coccothraustes']], 'timestamp': '2021-11-20 19:17:20', 'lat': 59.334591, 'lon': 18.06324}],
            [{'ranked_list': [[1.6691264510154724, [0.5070121, 0.5206054, 0.64150894], 'Thrush Nightingale', 'Luscinia luscinia'], [0.7542640566825867, [0.75426406], 'Willow Warbler', 'Phylloscopus trochilus']], 'timestamp': '2021-11-20 19:17:17', 'lat': 59.334591, 'lon': 18.06324}],
            [{'ranked_list': [[5.6568403244018555, [0.89116544, 0.9258461, 0.96231425, 0.9300823, 0.97526336, 0.97216886], 'Dusky Warbler', 'Phylloscopus fuscatus']], 'timestamp': '2021-11-20 19:17:20', 'lat': 59.334591, 'lon': 18.06324}],
            [{'ranked_list': [[12.051815152168274, [0.998315, 0.9998982, 0.99932456, 0.9914328, 0.9924958, 0.99979657, 0.9842609, 0.5708404, 0.99983287, 0.99689204, 0.9997732, 0.998782, 0.52017087], 'Collared Flycatcher', 'Ficedula albicollis']], 'timestamp': '2021-11-20 19:17:19', 'lat': 59.334591, 'lon': 18.06324}]
            ]
        results = MOCK_DATA#[random.randint(0,len(MOCK_DATA)-1)]
        for result in results:
            item = result[0]
            time = item["timestamp"]
            ranked_list = item["ranked_list"]
            f_ranked_list = list(map(lambda x: x[3], ranked_list))
            #result = {"species_names": f_ranked_list, "detection_time": time}
            #self._parent._detect_stats.append(result)
        print("DetectorMOCK().Detect()")
        result = {"mock": "mock"}
        #self.detect_result.emit(json.dumps(result))

    def stop(self):
        pass


class parentMOCK():
    def __init__(self):
        self._species_list = []

#mock = parentMOCK()
#dm = DetectorMOCK(mock)
#dm.detect(10)
#   print(mock._species_list)
