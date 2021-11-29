from PySide6.QtMultimedia import QAudioSink, QAudioSource
from AudioFormats import AudioFormats

class AudioSources():
    def __init__(self, parent):
        super().__init__()
        self._parent = parent

        self._io_device_1 = None
        self._io_device_2 = None
        self.m_audioSink = None
        self._io_device_3 = None

    def connectAll(self):

        self._audio_input_1 = QAudioSource(self._parent._device_in, AudioFormats().getLowQuality(), self._parent)
        self._audio_input_2 = QAudioSource(self._parent._device_in, AudioFormats().getHighQuality(), self._parent)
        self.m_audioSink = QAudioSink(self._parent._device_out, AudioFormats().getHighQuality(), self._parent)
        self.m_audioSink.stateChanged.connect(self._parent.handle_state_changed)
        self._audio_input_3 = QAudioSource(self._parent._device_in, AudioFormats().getHighQuality(), self._parent)

    def startAll(self):
        
        self._io_device_1 = self._audio_input_1.start()
        self._io_device_2 = self._audio_input_2.start()
        self.m_audioSink.start(self._io_device_2)
        self._io_device_3 = self._audio_input_3.start()
        print("AudioSources().startAll()")
       
    def stopAll(self):
        if self._audio_input_1 is not None:
            self._audio_input_1.stop()
        if self._audio_input_2 is not None:
            self._audio_input_2.stop()
        if self._audio_input_3 is not None:
            self._audio_input_3.stop()
        if self.m_audioSink is not None:
            self.m_audioSink.stop()
        print("AudioSources().closeAll()")

    

    


