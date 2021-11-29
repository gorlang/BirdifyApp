
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
