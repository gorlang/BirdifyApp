import json
import pandas as pd

def dfToJson(df):
    json_result = df.to_json(orient="table")
    return json.loads(json_result)["data"]

def asDataFrame(stats):
    if len(stats) > 0:
        df_indata = {}
        colnames = list(stats[0])
        for colname in colnames:
            df_indata[colname] = []
        for row in stats:
            for col in colnames:
                df_indata[col].append(row[col])
        df = pd.DataFrame(data=df_indata)
        df['p'] = df['p'].astype(float)
        return df
    return None