import numpy as np

class Sites():
    def __init__(self, df_sites):
        self._df_sites = df_sites

    def df(self):
        return self._df_sites

    def findByName(self, name):
        result = self._df_sites.query(f"name == '{name}'")
        if (len(result) > 0):
            return result
        return None

    def hasCoords(self, result):
        if np.isnan(result["latitude"].values[0]):
            return False
        if np.isnan(result["longitude"].values[0]):
            return False
        return True

    def getCoords(self, name):
        result = self._df_sites.query(f"name == '{name}'");
        if (len(result) > 0 and self.hasCoords(result)):
            return [result["latitude"].values[0], result["longitude"].values[0]]
        return None
