from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QComboBox, QTextEdit, QSplitter, QFrame, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from tng_packet.core.theme_manager import ThemeManager
from tng_packet.ui.settings_dialog import SettingsDialog
from tng_packet.core.settings import save_settings
from tng_packet.core.i18n import Translator
from tng_packet.ui.wideband_window import WidebandWindow

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        lang = self.settings.get('lang', 'en')
        Translator.load(lang)
        self.wide_window = None
        self.resize(900, 600)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"TNG_PacketAPP - MPDA v4.1.0 [{self.settings.get('callsign', 'NOCALL')}]")
        if self.centralWidget(): self.centralWidget().deleteLater()
        central_widget = QWidget(); self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget); main_layout.setContentsMargins(2, 2, 2, 2)

        # Menu Bar
        self.menuBar().clear(); menubar = self.menuBar()
        file_menu = menubar.addMenu(Translator.tr("menu_file"))
        settings_action = QAction(Translator.tr("menu_settings"), self); settings_action.triggered.connect(self.open_settings); file_menu.addAction(settings_action)
        exit_action = QAction(Translator.tr("menu_exit"), self); exit_action.triggered.connect(self.close); file_menu.addAction(exit_action)
        
        view_menu = menubar.addMenu(Translator.tr("menu_view"))
        wf_action = QAction(Translator.tr("menu_show_wf"), self); wf_action.triggered.connect(self.toggle_waterfall); view_menu.addAction(wf_action)
        
        help_menu = menubar.addMenu(Translator.tr("menu_help")); help_menu.addAction('About')

        # Main Area: Splitter (Band Activity | RX)
        mid_splitter = QSplitter(Qt.Orientation.Horizontal)
        left_cont = QWidget(); left_l = QVBoxLayout(left_cont); left_l.setContentsMargins(0,0,0,0)
        left_l.addWidget(QLabel(Translator.tr("grp_activity"))); self.band_activity = QTextEdit(); self.band_activity.setReadOnly(True); left_l.addWidget(self.band_activity)
        
        right_cont = QWidget(); right_l = QVBoxLayout(right_cont); right_l.setContentsMargins(0,0,0,0)
        right_l.addWidget(QLabel(Translator.tr("grp_rx"))); self.rx_window = QTextEdit(); self.rx_window.setReadOnly(True); right_l.addWidget(self.rx_window)
        
        mid_splitter.addWidget(left_cont); mid_splitter.addWidget(right_cont); mid_splitter.setStretchFactor(0, 1); mid_splitter.setStretchFactor(1, 2)
        main_layout.addWidget(mid_splitter, stretch=4)

        # Bottom Controls
        bottom_frame = QFrame(); bottom_layout = QHBoxLayout(bottom_frame)
        settings_group = QFrame(); settings_layout = QVBoxLayout(settings_group)
        self.track_combo = QComboBox(); self.track_combo.addItems(["4 Tracks", "8 Tracks", "1 Track"])
        self.speed_combo = QComboBox(); self.speed_combo.addItems(["10 Hz", "5 Hz", "15 Hz"])
        settings_layout.addWidget(QLabel(Translator.tr("lbl_config"))); settings_layout.addWidget(self.track_combo); settings_layout.addWidget(self.speed_combo); settings_layout.addStretch()
        bottom_layout.addWidget(settings_group, stretch=1)

        tx_group = QVBoxLayout()
        call_layout = QHBoxLayout()
        self.dx_call = QTextEdit(); self.dx_call.setFixedHeight(30); self.msg_input = QTextEdit(); self.msg_input.setFixedHeight(30)
        call_layout.addWidget(QLabel(Translator.tr("lbl_to"))); call_layout.addWidget(self.dx_call); call_layout.addWidget(QLabel(Translator.tr("lbl_msg"))); call_layout.addWidget(self.msg_input)
        self.btn_tx = QPushButton(Translator.tr("btn_tx")); self.btn_tx.setFixedHeight(40); self.btn_tx.setStyleSheet("background-color: #d32f2f; color: white; font-weight: bold;")
        self.btn_halt = QPushButton(Translator.tr("btn_halt")); self.btn_halt.setFixedHeight(40)
        tx_group.addLayout(call_layout)
        btn_layout = QHBoxLayout(); btn_layout.addWidget(self.btn_tx); btn_layout.addWidget(self.btn_halt); tx_group.addLayout(btn_layout)
        bottom_layout.addLayout(tx_group, stretch=4)
        main_layout.addWidget(bottom_frame, stretch=1)

        ThemeManager.apply_theme(QApplication.instance(), self, self.settings.get('theme', 'light'))

    def open_settings(self):
        dlg = SettingsDialog(self, self.settings)
        if dlg.exec():
            new_settings = dlg.get_settings()
            lang_changed = (new_settings.get('lang') != self.settings.get('lang'))
            self.settings.update(new_settings)
            save_settings(self.settings)
            if lang_changed: Translator.load(self.settings.get('lang', 'en')); self.init_ui()
            else: ThemeManager.apply_theme(QApplication.instance(), self, self.settings.get('theme', 'light'))
            if self.wide_window: self.wide_window.update_style()

    def toggle_waterfall(self):
        if self.wide_window is None:
            self.wide_window = WidebandWindow(self.settings)
        
        if self.wide_window.isVisible():
            self.wide_window.hide()
        else:
            self.wide_window.show()

    def closeEvent(self, event):
        if self.wide_window: self.wide_window.close()
        super().closeEvent(event)
