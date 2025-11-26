from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QTextEdit, QSplitter, QFrame, QApplication, QSlider, QGridLayout, QLineEdit)
from PyQt6.QtCore import Qt, QTimer, QTime
from tng_packet.core.theme_manager import ThemeManager
from tng_packet.ui.settings_dialog import SettingsDialog
from tng_packet.core.settings import save_settings
from tng_packet.core.i18n import Translator
from tng_packet.ui.visual_widget import VisualWidget

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.settings['theme'] = 'dark' # Force Dark Mode
        Translator.load(self.settings.get('lang', 'en'))
        self.resize(1280, 800)
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_status); self.timer.start(1000)
        self.is_tx_enabled = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"TNG_PacketAPP - MPDA v4.1.0 [{self.settings.get('callsign', 'NOCALL')}]")
        if self.centralWidget(): self.centralWidget().deleteLater()
        central = QWidget(); self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0,0,0,0); main_layout.setSpacing(0)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # LEFT PANEL
        left_panel = QFrame(); left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 5)
        
        # Header
        self.top_qso = QFrame(); qso_layout = QGridLayout(self.top_qso); qso_layout.setContentsMargins(5,5,5,5)
        self.txt_dx_call = QLineEdit(); self.txt_dx_call.setPlaceholderText("DX CALL")
        self.txt_rst_s = QLineEdit("599"); self.txt_rst_s.setFixedWidth(60)
        self.track_combo = QComboBox(); self.track_combo.addItems(["4 Tracks", "8 Tracks"])
        qso_layout.addWidget(QLabel("DX Call:"), 0, 0); qso_layout.addWidget(self.txt_dx_call, 0, 1)
        qso_layout.addWidget(QLabel("RST:"), 0, 2); qso_layout.addWidget(self.txt_rst_s, 0, 3)
        qso_layout.addWidget(self.track_combo, 0, 4)
        left_layout.addWidget(self.top_qso)
        
        # TX Input
        self.msg_input = QTextEdit(); self.msg_input.setPlaceholderText("Type Message...")
        left_layout.addWidget(self.msg_input, stretch=3)
        
        # Controls
        self.ctrl_frame = QFrame(); ctrl_layout = QGridLayout(self.ctrl_frame)
        self.btn_tx = QPushButton("Enable TX"); self.btn_tx.setCheckable(True); self.btn_tx.setFixedHeight(50); self.btn_tx.clicked.connect(self.on_tx_clicked)
        self.btn_halt = QPushButton("HALT"); self.btn_halt.setFixedHeight(50); self.btn_halt.clicked.connect(self.on_halt_clicked)
        self.btn_tune = QPushButton("TUNE"); self.btn_tune.setCheckable(True); self.btn_tune.setFixedHeight(50); self.btn_tune.clicked.connect(self.on_tune_clicked)
        self.slider_pwr = QSlider(Qt.Orientation.Horizontal); self.slider_pwr.setRange(0, 100); self.slider_pwr.setValue(int(self.settings.get('tx_power', 50)))
        self.lbl_pwr = QLabel(f"PWR: {self.slider_pwr.value()}%"); self.slider_pwr.valueChanged.connect(lambda v: [self.lbl_pwr.setText(f"PWR: {v}%"), self.settings.update({'tx_power': v})])
        
        ctrl_layout.addWidget(self.btn_tx, 0, 0, 1, 2)
        ctrl_layout.addWidget(self.btn_tune, 0, 2)
        ctrl_layout.addWidget(self.btn_halt, 0, 3)
        ctrl_layout.addWidget(self.lbl_pwr, 1, 0)
        ctrl_layout.addWidget(self.slider_pwr, 1, 1, 1, 3)
        left_layout.addWidget(self.ctrl_frame)
        
        # Log
        self.log_view = QTextEdit(); self.log_view.setReadOnly(True)
        left_layout.addWidget(self.log_view, stretch=3)
        self.status_bar = QLabel("Initializing..."); self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter); self.status_bar.setFixedHeight(25)
        left_layout.addWidget(self.status_bar)
        
        # RIGHT PANEL
        right_panel = QFrame(); right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0); right_layout.setSpacing(0)
        self.rx_text = QTextEdit(); self.rx_text.setReadOnly(True); self.rx_text.setPlaceholderText("RX Stream...")
        right_layout.addWidget(self.rx_text, stretch=3)
        self.visuals = VisualWidget(self.settings)
        right_layout.addWidget(self.visuals, stretch=2)
        
        self.splitter.addWidget(left_panel); self.splitter.addWidget(right_panel)
        self.splitter.setStretchFactor(0, 3); self.splitter.setStretchFactor(1, 4)
        main_layout.addWidget(self.splitter)
        
        self._create_menu()
        ThemeManager.apply_theme(QApplication.instance(), self)
        self.visuals.start()

    def apply_style(self):
        # This method is called by ThemeManager to apply window-specific styles
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QLabel { color: #eee; font-size: 13px; }
            QLineEdit, QTextEdit, QComboBox { background-color: #333; color: #eee; border: 1px solid #555; selection-background-color: #0078d7; }
            QSplitter::handle { background-color: #444; }
            QPushButton { background-color: #444; color: white; border: 1px solid #555; border-radius: 3px; font-weight: bold; }
            QPushButton:hover { background-color: #555; }
            QPushButton:checked#btnTx { background-color: #d32f2f; border-color: #b71c1c; }
            QPushButton:checked#btnTune { background-color: #f57c00; border-color: #e65100; }
            QLabel#statusBar { background-color: #222; color: #aaa; }
        """)
        self.top_qso.setStyleSheet("")
        self.ctrl_frame.setStyleSheet("")

    def _create_menu(self):
        mb = self.menuBar()
        mb.clear() # FIX: Remove duplicates
        f = mb.addMenu(Translator.tr("menu_file"))
        f.addAction(Translator.tr("menu_settings"), self.open_settings)
        f.addAction(Translator.tr("menu_exit"), self.close)
        mb.addMenu(Translator.tr("menu_view"))
        mb.addMenu(Translator.tr("menu_help"))

    def on_tx_clicked(self, checked):
        if checked: self.btn_tx.setText("TX ENABLED"); self.is_tx_enabled = True; self.btn_tune.setChecked(False)
        else: self.btn_tx.setText("Enable TX"); self.is_tx_enabled = False
    def on_halt_clicked(self): self.btn_tx.setChecked(False); self.btn_tx.setText("Enable TX"); self.btn_tune.setChecked(False); self.is_tx_enabled = False
    def on_tune_clicked(self, checked): 
        if checked and self.btn_tx.isChecked(): self.btn_tx.setChecked(False); self.btn_tx.setText("Enable TX")
    def update_status(self): self.status_bar.setText(f"UTC: {QTime.currentTime().toString('HH:mm:ss')} | Mode: MPDA | Status: Ready")

    def open_settings(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec():
            new_s = dlg.get_settings()
            lang_changed = (new_s.get('lang') != self.settings.get('lang'))
            self.settings.update(new_s)
            save_settings(self.settings)
            if lang_changed: Translator.load(self.settings.get('lang', 'en')); self.init_ui()
            else: ThemeManager.apply_theme(QApplication.instance(), self)
            self.visuals.refresh_settings()
    
    def closeEvent(self, event): self.visuals.stop(); save_settings(self.settings); super().closeEvent(event)
