from PySide6.QtGui import Qt
import pandas as pd
import sys
import json
sys.path.append('src')
from BWidgetSearch import BWidgetSearch

def asDataFrame(stats):
    #stats = self._parent._stats._detect_stats
    if len(stats) > 0:
        df_indata = {}
        colnames = list(stats[0])
        for colname in colnames:
            df_indata[colname] = []

        for row in stats:
            for col in colnames:
                df_indata[col].append(row[col])
        return pd.DataFrame(data=df_indata)
    return None

stats = [{"name_sv": "apa1", "p": 0.25},{"name_sv": "apa1", "p": 0.5},{"name_sv": "apa2", "p": 1},{"name_sv": "apa3", "p": 0.1},{"name_sv": "apa3", "p": 0.2}]
stats = [ {'name_sci': 'Prunella modularis', 'name_en': 'Dunnock', 'name_sv': 'Järnsparv', 'p': 0.97, 'timestamp': '2021-11-24 10:46:25', 'timeofday': '10:46:25', 'date': '2021-11-24', 'country': 'Sweden'},
{'name_sci': 'Prunella modularis', 'name_en': 'Dunnock', 'name_sv': 'Rödhake', 'p': 0.45, 'timestamp': '2021-11-24 10:46:25', 'timeofday': '10:46:25', 'date': '2021-11-24', 'country': 'Sweden'}]


df = asDataFrame(stats)
json_data = df.groupby(["name_sv"]).mean("p").sort_values(["p"], ascending=False).to_json(orient="table")
print(json.loads(json_data)["data"])
