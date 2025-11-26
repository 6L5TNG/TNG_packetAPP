from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QTextEdit, QSplitter, QFrame, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from tng_packet.core.theme_manager import ThemeManager
from tng_packet.ui.settings_dialog import SettingsDialog
from tng_packet.core.settings import save_settings
from tng_packet.core.i18n import Translator

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        
        # Load Language
        lang = self.settings.get('lang', 'en')
        Translator.load(lang)
        
        self.resize(1100, 800)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"TNG_PacketAPP - MPDA v4.1.0 [{self.settings.get('callsign', 'NOCALL')}]")

        # Central Widget
        if self.centralWidget():
            self.centralWidget().deleteLater()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)

        # Re-create Menu Bar (to update language)
        self.menuBar().clear()
        menubar = self.menuBar()
        file_menu = menubar.addMenu(Translator.tr("menu_file"))
        
        settings_action = QAction(Translator.tr("menu_settings"), self)
        settings_action.triggered.connect(self.open_settings)
        file_menu.addAction(settings_action)
        
        exit_action = QAction(Translator.tr("menu_exit"), self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu(Translator.tr("menu_view"))
        view_menu.addAction('Waterfall Controls')
        
        help_menu = menubar.addMenu(Translator.tr("menu_help"))
        help_menu.addAction('About')

        # 1. Waterfall Area
        self.scope_container = QFrame()
        self.scope_container.setFrameShape(QFrame.Shape.StyledPanel)
        self.scope_container.setMinimumHeight(250)
        
        scope_layout = QVBoxLayout(self.scope_container)
        scope_layout.setSpacing(0)
        scope_layout.setContentsMargins(0,0,0,0)
        
        self.spectrum_label = QLabel(Translator.tr("lbl_spectrum"))
        self.spectrum_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spectrum_label.setFixedHeight(80)
        
        self.waterfall_label = QLabel(Translator.tr("lbl_waterfall"))
        self.waterfall_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        scope_layout.addWidget(self.spectrum_label)
        scope_layout.addWidget(self.waterfall_label)
        
        main_layout.addWidget(self.scope_container, stretch=3)

        # 2. Middle Section
        mid_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0,0,0,0)
        left_layout.addWidget(QLabel(Translator.tr("grp_activity")))
        self.band_activity = QTextEdit()
        self.band_activity.setReadOnly(True)
        left_layout.addWidget(self.band_activity)
        
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0,0,0,0)
        right_layout.addWidget(QLabel(Translator.tr("grp_rx")))
        self.rx_window = QTextEdit()
        self.rx_window.setReadOnly(True)
        right_layout.addWidget(self.rx_window)

        mid_splitter.addWidget(left_container)
        mid_splitter.addWidget(right_container)
        mid_splitter.setStretchFactor(0, 1)
        mid_splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(mid_splitter, stretch=4)

        # 3. Bottom Section
        bottom_frame = QFrame()
        bottom_layout = QHBoxLayout(bottom_frame)
        bottom_layout.setContentsMargins(5, 5, 5, 5)
        
        settings_group = QFrame()
        settings_layout = QVBoxLayout(settings_group)
        
        self.track_combo = QComboBox()
        self.track_combo.addItems(["4 Tracks", "8 Tracks", "1 Track"])
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["10 Hz", "5 Hz", "15 Hz"])
        
        settings_layout.addWidget(QLabel(Translator.tr("lbl_config")))
        settings_layout.addWidget(self.track_combo)
        settings_layout.addWidget(self.speed_combo)
        settings_layout.addStretch()
        
        bottom_layout.addWidget(settings_group, stretch=1)

        tx_group = QVBoxLayout()
        call_layout = QHBoxLayout()
        self.dx_call = QTextEdit()
        self.dx_call.setFixedHeight(30)
        self.msg_input = QTextEdit()
        self.msg_input.setFixedHeight(30)
        
        call_layout.addWidget(QLabel(Translator.tr("lbl_to")))
        call_layout.addWidget(self.dx_call)
        call_layout.addWidget(QLabel(Translator.tr("lbl_msg")))
        call_layout.addWidget(self.msg_input)
        
        self.btn_tx = QPushButton(Translator.tr("btn_tx"))
        self.btn_tx.setFixedHeight(40)
        self.btn_tx.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold;")
        
        self.btn_halt = QPushButton(Translator.tr("btn_halt"))
        self.btn_halt.setFixedHeight(40)

        tx_group.addLayout(call_layout)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_tx)
        btn_layout.addWidget(self.btn_halt)
        tx_group.addLayout(btn_layout)

        bottom_layout.addLayout(tx_group, stretch=4)
        main_layout.addWidget(bottom_frame, stretch=1)

        # Apply Theme at the end of UI build
        ThemeManager.apply_theme(QApplication.instance(), self, self.settings.get('theme', 'light'))

    def open_settings(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec():
            new_settings = dlg.get_settings()
            
            # Check if language changed to reload strings
            lang_changed = (new_settings.get('lang') != self.settings.get('lang'))
            
            self.settings.update(new_settings)
            save_settings(self.settings)
            
            if lang_changed:
                Translator.load(self.settings.get('lang', 'en'))
                self.init_ui() # Rebuild UI for language change
            else:
                # Just apply theme
                ThemeManager.apply_theme(QApplication.instance(), self, self.settings.get('theme', 'light'))
