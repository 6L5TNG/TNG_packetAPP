import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel, QFrame
from PyQt6.QtCore import Qt, QRectF
from tng_packet.core.audio_stream import AudioMonitor

class VisualWidget(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.layout = QHBoxLayout(self); self.layout.setContentsMargins(0,0,0,0); self.layout.setSpacing(0)
        
        # Meters Strip
        self.meters_frame = QFrame(); self.meters_frame.setFixedWidth(35)
        m_layout = QVBoxLayout(self.meters_frame); m_layout.setContentsMargins(2,2,2,2); m_layout.setSpacing(2)
        lbl_rx = QLabel("R"); lbl_rx.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl_rx.setStyleSheet("font-size: 10px; font-weight: bold;"); m_layout.addWidget(lbl_rx)
        self.bar_rx = QProgressBar(); self.bar_rx.setOrientation(Qt.Orientation.Vertical); self.bar_rx.setRange(0, 100); self.bar_rx.setTextVisible(False); m_layout.addWidget(self.bar_rx)
        lbl_tx = QLabel("T"); lbl_tx.setAlignment(Qt.AlignmentFlag.AlignCenter); lbl_tx.setStyleSheet("font-size: 10px; font-weight: bold;"); m_layout.addWidget(lbl_tx)
        self.bar_tx = QProgressBar(); self.bar_tx.setOrientation(Qt.Orientation.Vertical); self.bar_tx.setRange(0, 100); self.bar_tx.setValue(0); self.bar_tx.setTextVisible(False); m_layout.addWidget(self.bar_tx)
        self.layout.addWidget(self.meters_frame)
        
        # Graphs Area
        graph_layout = QVBoxLayout(); graph_layout.setSpacing(0)
        
        # Spectrum
        self.plot_spec = pg.PlotWidget()
        self.plot_spec.showAxis('bottom', False); self.plot_spec.showAxis('left', False)
        self.plot_spec.setXRange(0, 3000); self.plot_spec.setYRange(0, 100)
        self.plot_spec.hideButtons(); self.plot_spec.setMouseEnabled(x=False, y=False)
        self.plot_spec.setFixedHeight(100)
        self.curve_spec = self.plot_spec.plot(pen='y')
        graph_layout.addWidget(self.plot_spec)
        
        # Waterfall
        self.plot_wf = pg.PlotWidget()
        self.plot_wf.showAxis('bottom', False); self.plot_wf.showAxis('left', False)
        self.plot_wf.setXRange(0, 3000)
        self.plot_wf.hideButtons(); self.plot_wf.setMouseEnabled(x=False, y=False)
        self.img_wf = pg.ImageItem()
        # Fix Flickering & Aliasing: set pxMode=False (better scaling)
        self.img_wf.setOptions(pxMode=False)
        self.plot_wf.addItem(self.img_wf)
        self.hist = pg.HistogramLUTItem(); self.hist.setImageItem(self.img_wf)
        graph_layout.addWidget(self.plot_wf)
        
        self.layout.addLayout(graph_layout)
        
        self.monitor = AudioMonitor(self.settings.get('audio_in_idx'))
        self.monitor.data_signal.connect(self.update_data)
        self.history_len = 300
        self.wf_data = np.zeros((self.history_len, 513))
        self.refresh_settings()

    def refresh_settings(self):
        # Style
        self.meters_frame.setStyleSheet("background-color: #2b2b2b; color: #aaa; border-right: 1px solid #444;")
        bar_style = "QProgressBar { border: none; background-color: #333; border-radius: 1px; }"
        self.bar_rx.setStyleSheet(bar_style + "QProgressBar::chunk { background-color: #00c853; }")
        self.bar_tx.setStyleSheet(bar_style + "QProgressBar::chunk { background-color: #d50000; }")

        bg = '#000000'
        self.plot_spec.setBackground(bg); self.plot_wf.setBackground(bg)
        
        # Spectrum Settings
        l_width = self.settings.get('spec_line_width', 1)
        do_fill = self.settings.get('spec_fill', False)
        pen = pg.mkPen('y', width=l_width)
        self.curve_spec.setPen(pen)
        if do_fill: self.curve_spec.setFillLevel(0); self.curve_spec.setBrush((255, 255, 0, 50))
        else: self.curve_spec.setBrush(None)

        # Waterfall Settings
        cmap = self.settings.get('colormap', 'magma')
        try: self.hist.gradient.loadPreset(cmap)
        except: self.hist.gradient.loadPreset('thermal')
        
        max_f = self.settings.get('max_freq', 3000)
        self.plot_spec.setXRange(0, max_f)
        self.plot_wf.setXRange(0, max_f)
        
        new_idx = self.settings.get('audio_in_idx')
        if self.monitor.device_index != new_idx:
            self.monitor.stop(); self.monitor.device_index = new_idx; self.monitor.start()

    def start(self): 
        if not self.monitor.running: self.monitor.start()
    def stop(self): 
        self.monitor.stop()
    def update_data(self, chunk):
        # Settings
        gain = self.settings.get('spec_gain', 1.0)
        ref = self.settings.get('ref_level', 0.0)
        dr = self.settings.get('drange', 60.0)
        smooth = self.settings.get('wf_smooth', True)
        
        # Audio Level
        rms = np.sqrt(np.mean(chunk**2))
        db_audio = 20 * np.log10(rms + 1e-9)
        level = np.clip((db_audio + 60) * 2, 0, 100)
        self.bar_rx.setValue(int(level))
        
        # FFT
        win = np.hanning(len(chunk))
        fft_res = np.fft.rfft(chunk * win)
        mag = np.abs(fft_res)
        mag = 20 * np.log10(mag + 1e-9)
        
        # Apply Settings
        mag = (mag + 50 + ref) * gain
        
        # Smoothing for waterfall visual (reduce noise)
        if smooth:
            # Simple moving average
            mag = np.convolve(mag, np.ones(3)/3, mode='same')

        freqs = np.fft.rfftfreq(len(chunk), 1.0/12000.0)
        self.curve_spec.setData(freqs, mag)
        
        # Waterfall Update
        self.wf_data = np.roll(self.wf_data, -1, axis=0)
        self.wf_data[-1] = mag[:513]
        
        self.img_wf.setImage(self.wf_data.T, autoLevels=False, levels=(0, dr + 20))
        self.img_wf.setRect(QRectF(0, 0, 6000, self.history_len))
