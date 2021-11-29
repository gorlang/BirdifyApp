class Countries():
    def __init__(self, df_countries):
        self._df_countries = df_countries

    def df(self):
        return self._df_countries

    def getCoords(self, name):
        result = self._df_countries.query(f"name == '{name}'");
        if (len(result) > 0):
            return [result["latitude"].values[0], result["longitude"].values[0]]
        return [None, None]