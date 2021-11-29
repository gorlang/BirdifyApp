DEPENDENCIES 
Used for input/output audio.

- portaudio (low level audio package)
- pyaudio (python interface for portaudio)
- VB-cable (to create loop back, seems to work fine on OS-X Mojave)

INSTALLATION

1 Install brew, see brew homepage for instructions https://brew.sh.
Brew is used to install portaudio.

NOTE! If brew not working correctly, you might need to uninstall and reinstall it.
Cleanup after reinstalling brew by doing (installation root-path migh vary):
rm -rf /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core; brew update

2 Install portaudio with brew:
brew install portaudio

3 Install pyaudio (needs portaudio & Xcode command line tools)
pip install pyaudio

4 Install VB-cable
Download installer from, https://vb-audio.com/Cable/index.htm, 
and set VB-Cable as the primary system input/output sound devices.

5 pip install tensorflow

6 pip install librosa