import os
from BirdifyAPI import detectSpecies, filterDetections, rankResult
from BirdNETLite import loadModel
import librosa

import warnings
warnings.filterwarnings("ignore")

def translate(name, from_lang="sci", to_lang="sv"):
    query = f"name_{from_lang} == '{name}'"
    result = self._df_species.query(query)["name_" + to_lang]
    if len(result) > 0:
        return result.values[0].strip("() 1234567890").capitalize()
    return "(" + name + ")"

#path = "/Users/green/Dev/projects/PythonNotebooks/BirdNETLite/data/file_denmark_2021_11_15_15_30_27.wav"
directory = "/Users/green/Music/Music/Media.localized/Tättingläten/Tättingläten/"
filenames = os.listdir(directory)
sample_rate = 48000
argMap = {"lat": 59.334591, "lon": 18.063240, "week": 20}
model = loadModel()
for filename in filenames[0:5]:
    print(filename)
    filepath = directory + filename
    sig, rate = librosa.load(filepath, sr=sample_rate, mono=True, res_type='kaiser_fast')
    results = filterDetections(detectSpecies(sig, sample_rate, argMap, interpreter=model))
    rankedResult = rankResult(results)
    print(rankedResult)
"""     print("---" + filename)
    top = rankedResult["ranked_list"]
    if (len(top)>0):
        print(round(top[0][0],2), top[0][3])
    else:
        print("No Match!")
    print("---" + filename) """



