import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QRectF
from tng_packet.core.audio_stream import AudioMonitor

class WidebandWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle("Wide Graph")
        self.resize(800, 600)
        
        central = QFrame()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # Spectrum
        self.plot_spec = pg.PlotWidget()
        self.plot_spec.showAxis('bottom', False)
        self.plot_spec.showAxis('left', False)
        self.plot_spec.setXRange(0, 6000)
        self.plot_spec.setYRange(0, 100)
        self.plot_spec.hideButtons()
        self.plot_spec.setMouseEnabled(x=False, y=False)
        self.curve_spec = self.plot_spec.plot(pen='y')
        layout.addWidget(self.plot_spec, stretch=1)

        # Waterfall
        self.plot_wf = pg.PlotWidget()
        self.plot_wf.showAxis('bottom', False)
        self.plot_wf.showAxis('left', False)
        self.plot_wf.setXRange(0, 6000)
        self.plot_wf.hideButtons()
        self.plot_wf.setMouseEnabled(x=False, y=False)
        self.img_wf = pg.ImageItem()
        self.plot_wf.addItem(self.img_wf)
        
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img_wf)
        
        layout.addWidget(self.plot_wf, stretch=2)

        # Audio
        self.monitor = AudioMonitor(self.settings.get('audio_in_idx'))
        self.monitor.data_signal.connect(self.update_plots)
        
        self.history_len = 300
        self.wf_data = np.zeros((self.history_len, 513))
        
        # Initialize
        self.refresh_settings()

    def refresh_settings(self):
        """Apply all settings immediately without restarting."""
        # 1. Colormap
        cmap_name = self.settings.get('colormap', 'magma')
        if cmap_name == 'gray': cmap_name = 'grey'
        try:
            self.hist.gradient.loadPreset(cmap_name)
        except KeyError:
            self.hist.gradient.loadPreset('thermal')
            
        # 2. Theme (Colors)
        is_dark = (self.settings.get('theme', 'light') == 'dark')
        bg_color = '#000000' if is_dark else '#ffffff'
        self.plot_spec.setBackground(bg_color)
        self.plot_wf.setBackground(bg_color)
        if is_dark:
            self.curve_spec.setPen(pg.mkPen('y', width=1))
        else:
            self.curve_spec.setPen(pg.mkPen('b', width=1))
            
        # 3. Audio Device (Restart if changed)
        new_idx = self.settings.get('audio_in_idx')
        if self.monitor.device_index != new_idx:
            self.monitor.stop()
            self.monitor.device_index = new_idx
            if self.isVisible():
                self.monitor.start()

    def showEvent(self, event):
        super().showEvent(event)
        if not self.monitor.running: self.monitor.start()

    def closeEvent(self, event):
        self.monitor.stop()
        super().closeEvent(event)

    def update_plots(self, chunk):
        gain = self.settings.get('spec_gain', 1.0)
        
        win = np.hanning(len(chunk))
        fft_res = np.fft.rfft(chunk * win)
        mag = np.abs(fft_res)
        mag = 20 * np.log10(mag + 1e-9)
        mag = np.clip(mag + 50, 0, 100) * gain
        
        freqs = np.fft.rfftfreq(len(chunk), 1.0/12000.0)
        self.curve_spec.setData(freqs, mag)
        
        self.wf_data = np.roll(self.wf_data, -1, axis=0)
        self.wf_data[-1] = mag[:513]
        
        self.img_wf.setImage(self.wf_data.T, autoLevels=False, levels=(0, 80))
        self.img_wf.setRect(QRectF(0, 0, 6000, self.history_len))
