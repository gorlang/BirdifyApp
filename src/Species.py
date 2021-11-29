import numpy as np

class Species():
    def __init__(self, df_species):
        self._df_species = df_species

    def translate(self, name, from_lang="sci", to_lang="sv"):
        """Available lang codes are ['sci', 'sv', 'en']"""
        query = f"name_{from_lang} == '{name}'"
        result = self._df_species.query(query)["name_" + to_lang]
        if len(result) > 0:
            return result.values[0].strip("() 1234567890").capitalize()
        return "(" + name + ")"
    
    def getRandName(self, lang="en"):
        ix = np.random.randint(len(self._df_species)-1)
        result = self._df_species.query(f"index == {ix}")["name_" + lang]
        return result.values[0].strip("() 1234567890")