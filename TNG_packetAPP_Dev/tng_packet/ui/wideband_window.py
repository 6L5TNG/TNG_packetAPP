from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from tng_packet.core.i18n import Translator
from tng_packet.core.theme_manager import ThemeManager
from PyQt6.QtWidgets import QApplication

class WidebandWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle("Wide Graph - TNG_PacketAPP")
        self.resize(800, 600)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # 1. Spectrum Plot (PyQtGraph)
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('k')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)
        self.plot_widget.setLabel('bottom', 'Frequency', units='Hz')
        self.plot_widget.setLabel('left', 'dB')
        self.plot_widget.setYRange(-120, 0)
        self.plot_widget.setXRange(0, self.settings.get('max_freq', 3000))
        self.plot_widget.setMinimumHeight(150)
        layout.addWidget(self.plot_widget)
        
        # 2. Waterfall Image (PyQtGraph)
        self.img_widget = pg.ImageView(view=pg.PlotItem())
        self.img_widget.ui.histogram.hide()
        self.img_widget.ui.roiBtn.hide()
        self.img_widget.ui.menuBtn.hide()
        self.img_widget.view.setAspectLocked(False)
        self.img_widget.view.setRange(xRange=[0, self.settings.get('max_freq', 3000)])
        layout.addWidget(self.img_widget)
        
        # Apply initial theme
        ThemeManager.apply_theme(QApplication.instance(), None, self.settings.get('theme', 'light'))
        self.update_style()

    def update_style(self):
        is_dark = (self.settings.get('theme', 'light') == 'dark')
        if is_dark:
            self.plot_widget.setBackground((30, 30, 30))
        else:
            self.plot_widget.setBackground((240, 240, 240))
