## DESCRIPTION

Birdify will assist you on your virtual birding tours. It listens to the laptop audio output, analyzes the signal and detects any bird sounds.

When you visit your favorite nature YT-streams it can help you to identify a large number of the birds of the world (if the audio is of reasonably good quality).

Birdify can also detect bird sounds in audio files loaded from disk and plot spectograms.

Birdify is a desktop-app created with Qt/Pyside6 and the AI functionality is powered by BirdNET:s TensorFlow model BirdNETLite, developed at The Cornell Lab of Ornithology and Chemnitz University of Technology.

More info with screen shots here:

(https://knutas.com/birdify/)

## DEPENDENCIES

- Python 3.9.1
- pip 21.3.1

- VB-cable (or other similar software, to create audio loop back)
Download installer from, https://vb-audio.com/Cable/index.htm, 
and set 'VB-Cable' as the primary system input and output devices.

## INSTALLATION

```bash
$ mkdir BirdifyApp
$ cd BirdifyApp
$ python -m venv env
$ source env/bin/activate
$ pip install pandas
$ pip install pyside6
$ pip install tensorflow
$ pip install matplotlib
$ pip install librosa
```

Start the app by running the main module:

```bash
$ ./env/bin/python src/BirdifyAppGUI.py
```

TODO
Add missing pieces...

## LICENSE

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-nc-sa/4.0/)

## ATTRIBUTIONS

1. The BirdNETLite Tensorflow model is developed at The Cornell Lab of Ornithology and Chemnitz University of Technology. Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (https://creativecommons.org/licenses/by-nc-sa/4.0/)

2. Fugue Icons (C) 2013 Yusuke Kamiyamane. All rights reserved. Icons are licensed under a Creative Commons Attribution 3.0 License. (http://creativecommons.org/licenses/by/3.0/)