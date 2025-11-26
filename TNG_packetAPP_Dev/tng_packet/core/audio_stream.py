import sounddevice as sd
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal, QThread

class AudioMonitor(QObject):
    data_signal = pyqtSignal(np.ndarray)

    def __init__(self, device_index=None):
        super().__init__()
        self.device_index = device_index
        self.running = False
        self.stream = None

    def start(self):
        if self.running: return
        try:
            # Sample Rate 12000 is enough for visualization (0-6kHz)
            # Block size 1024 or 2048 for smooth update
            self.stream = sd.InputStream(
                device=self.device_index,
                channels=1,
                samplerate=12000,
                blocksize=1024,
                callback=self._audio_callback
            )
            self.stream.start()
            self.running = True
        except Exception as e:
            print(f"Audio Stream Error: {e}")

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        self.running = False

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        # indata is (frames, channels)
        # Emit the first channel data
        self.data_signal.emit(indata[:, 0].copy())
