from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from tng_packet.core.i18n import Translator
from tng_packet.core.theme_manager import ThemeManager
from PyQt6.QtWidgets import QApplication

class WidebandWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setWindowTitle("Wide Graph - TNG_PacketAPP")
        self.resize(800, 600)
        
        central = QFrame()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        
        # Spectrum Area
        self.spectrum_label = QLabel(Translator.tr("lbl_spectrum"))
        self.spectrum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spectrum_label.setFixedHeight(150)
        layout.addWidget(self.spectrum_label)
        
        # Waterfall Area
        self.waterfall_label = QLabel(Translator.tr("lbl_waterfall"))
        self.waterfall_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.waterfall_label)
        
        # Apply initial theme
        ThemeManager.apply_theme(QApplication.instance(), None, self.settings.get('theme', 'light'))
        self.update_style()

    def update_style(self):
        is_dark = (self.settings.get('theme', 'light') == 'dark')
        if is_dark:
            self.setStyleSheet("background-color: black;")
            self.spectrum_label.setStyleSheet("color: yellow; border-bottom: 1px dashed #333; font-size: 14px;")
            self.waterfall_label.setStyleSheet("color: cyan; font-size: 16px;")
        else:
            self.setStyleSheet("background-color: #e0e0e0;")
            self.spectrum_label.setStyleSheet("color: blue; border-bottom: 1px dashed #ccc; font-size: 14px;")
            self.waterfall_label.setStyleSheet("color: black; font-size: 16px;")
