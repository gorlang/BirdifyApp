import numpy as np

class Decoder():
    def __init__(self, channels=2, _bytes=2, dtype='int16'):
        self._dtype = dtype
        self._channels = channels
        self._bytes = _bytes

    def decode(self, in_data):
        """
        Convert a byte stream into a 2D numpy array with 
        shape (chunk_size, channels)

        Samples are interleaved, so for a stereo stream with left channel 
        of [L0, L1, L2, ...] and right channel of [R0, R1, R2, ...], the output 
        is ordered as [L0, R0, L1, R1, ...]
        """
        
        if (len(in_data) % (self._channels)) != 0:
            in_data = in_data[0:-1]
        if (len(in_data) % (self._channels * self._bytes)) != 0:
            in_data = in_data[0:-2]

        result = np.frombuffer(in_data, dtype=self._dtype)
        chunk_length = len(result)/self._channels
        assert chunk_length == int(chunk_length)

        result = np.reshape(result, (int(chunk_length), self._channels))
        return result