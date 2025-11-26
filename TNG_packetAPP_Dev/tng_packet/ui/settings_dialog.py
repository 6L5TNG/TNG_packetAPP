from PyQt6.QtWidgets import (QDialog, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QGroupBox, QPushButton, QSpinBox, QDoubleSpinBox, QCheckBox)
from tng_packet.core.i18n import Translator
import sounddevice as sd

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.setWindowTitle(Translator.tr("menu_settings"))
        self.resize(700, 550)
        layout = QVBoxLayout(self)
        self.main_tabs = QTabWidget()
        layout.addWidget(self.main_tabs)
        
        self.tab_gen = QWidget(); self.main_tabs.addTab(self.tab_gen, Translator.tr("tab_gen")); self._build_general_tab()
        self.tab_audio = QWidget(); self.main_tabs.addTab(self.tab_audio, Translator.tr("tab_audio")); self._build_audio_tab()
        self.tab_trans = QWidget(); self.main_tabs.addTab(self.tab_trans, Translator.tr("tab_trans")); self._build_transmit_tab()
        self.tab_recv = QWidget(); self.main_tabs.addTab(self.tab_recv, Translator.tr("tab_recv")); self._build_receive_tab()
        self.tab_log = QWidget(); self.main_tabs.addTab(self.tab_log, Translator.tr("tab_log")); self._build_log_tab()
        self.tab_macro = QWidget(); self.main_tabs.addTab(self.tab_macro, Translator.tr("tab_macro")); self._build_macro_tab()
        
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK"); btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancel"); btn_cancel.clicked.connect(self.reject)
        btn_layout.addStretch(); btn_layout.addWidget(btn_ok); btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def _build_general_tab(self):
        layout = QVBoxLayout(self.tab_gen)
        grp_st = QGroupBox(Translator.tr("grp_station"))
        l_st = QVBoxLayout(grp_st)
        r1 = QHBoxLayout(); self.txt_call = QLineEdit(self.settings.get('callsign', '')); r1.addWidget(QLabel(Translator.tr("lbl_call"))); r1.addWidget(self.txt_call)
        r2 = QHBoxLayout(); self.txt_grid = QLineEdit(self.settings.get('grid', '')); r2.addWidget(QLabel(Translator.tr("lbl_grid"))); r2.addWidget(self.txt_grid)
        l_st.addLayout(r1); l_st.addLayout(r2); layout.addWidget(grp_st)

        grp_ui = QGroupBox(Translator.tr("grp_ui"))
        l_ui = QVBoxLayout(grp_ui)
        self.combo_theme = QComboBox(); self.combo_theme.addItems(['Light', 'Dark']); self.combo_theme.setCurrentText(self.settings.get('theme', 'light').capitalize())
        self.combo_lang = QComboBox(); self.combo_lang.addItems(['English', 'Korean', 'Japanese'])
        lang_map = {'en': 'English', 'ko': 'Korean', 'jp': 'Japanese'}
        self.combo_lang.setCurrentText(lang_map.get(self.settings.get('lang', 'en'), 'English'))
        r3 = QHBoxLayout(); r3.addWidget(QLabel(Translator.tr("lbl_theme"))); r3.addWidget(self.combo_theme)
        r3.addWidget(QLabel(Translator.tr("lbl_lang"))); r3.addWidget(self.combo_lang)
        l_ui.addLayout(r3); layout.addWidget(grp_ui); layout.addStretch()

    def _build_audio_tab(self):
        layout = QVBoxLayout(self.tab_audio)
        grp_aud = QGroupBox(Translator.tr("grp_audio_dev"))
        l_aud = QVBoxLayout(grp_aud)
        self.combo_in = QComboBox(); self.combo_out = QComboBox()
        self._populate_audio_devices()
        l_aud.addWidget(QLabel(Translator.tr("lbl_in"))); l_aud.addWidget(self.combo_in)
        l_aud.addWidget(QLabel(Translator.tr("lbl_out"))); l_aud.addWidget(self.combo_out)
        layout.addWidget(grp_aud); layout.addStretch()

    def _build_transmit_tab(self):
        layout = QVBoxLayout(self.tab_trans); self.sub_tabs_tx = QTabWidget(); layout.addWidget(self.sub_tabs_tx)
        # MPDA
        sub_mpda = QWidget(); self.sub_tabs_tx.addTab(sub_mpda, Translator.tr("sub_mpda"))
        l_mpda = QVBoxLayout(sub_mpda); self.chk_beeps = QCheckBox(Translator.tr("lbl_beeps")); self.chk_beeps.setChecked(self.settings.get('enable_beeps', True)); l_mpda.addWidget(self.chk_beeps)
        l_mpda.addWidget(QLabel("MPDA TX Params (Pilot, Gap, etc.)")); l_mpda.addStretch()
        # Chirp
        sub_chirp = QWidget(); self.sub_tabs_tx.addTab(sub_chirp, Translator.tr("sub_chirp"))
        l_chirp = QVBoxLayout(sub_chirp); l_chirp.addWidget(QLabel("TNG_Chirp Settings")); l_chirp.addStretch()

    def _build_receive_tab(self):
        layout = QVBoxLayout(self.tab_recv); self.sub_tabs_rx = QTabWidget(); layout.addWidget(self.sub_tabs_rx)
        # MPDA
        sub_mpda = QWidget(); self.sub_tabs_rx.addTab(sub_mpda, Translator.tr("sub_mpda"))
        l_mpda = QVBoxLayout(sub_mpda); l_mpda.addWidget(QLabel("MPDA RX Thresholds")); l_mpda.addStretch()
        # Chirp (Added)
        sub_chirp = QWidget(); self.sub_tabs_rx.addTab(sub_chirp, Translator.tr("sub_chirp"))
        l_chirp = QVBoxLayout(sub_chirp); l_chirp.addWidget(QLabel("TNG_Chirp RX Settings")); l_chirp.addStretch()
        # Waterfall
        sub_wf = QWidget(); self.sub_tabs_rx.addTab(sub_wf, Translator.tr("sub_wf"))
        l_wf = QVBoxLayout(sub_wf)
        r1 = QHBoxLayout(); self.spin_maxf = QSpinBox(); self.spin_maxf.setRange(1000, 20000); self.spin_maxf.setValue(int(self.settings.get('max_freq', 3000))); r1.addWidget(QLabel(Translator.tr("lbl_maxf"))); r1.addWidget(self.spin_maxf); l_wf.addLayout(r1)
        r2 = QHBoxLayout(); self.combo_cmap = QComboBox(); self.combo_cmap.addItems(['magma', 'inferno', 'plasma', 'viridis', 'turbo', 'gray']); self.combo_cmap.setCurrentText(self.settings.get('colormap', 'magma')); r2.addWidget(QLabel(Translator.tr("lbl_cmap"))); r2.addWidget(self.combo_cmap); l_wf.addLayout(r2)
        r3 = QHBoxLayout(); self.spin_drange = QDoubleSpinBox(); self.spin_drange.setRange(10.0, 120.0); self.spin_drange.setValue(float(self.settings.get('drange', 60.0))); r3.addWidget(QLabel(Translator.tr("lbl_drange"))); r3.addWidget(self.spin_drange); l_wf.addLayout(r3); l_wf.addStretch()
        # Spectrum
        sub_spec = QWidget(); self.sub_tabs_rx.addTab(sub_spec, Translator.tr("sub_spec"))
        l_spec = QVBoxLayout(sub_spec); l_spec.addWidget(QLabel("Spectrum Settings")); l_spec.addStretch()

    def _build_log_tab(self): 
        layout = QVBoxLayout(self.tab_log); self.chk_ts = QCheckBox(Translator.tr("lbl_log_ts")); self.chk_ts.setChecked(self.settings.get('log_timestamp', True)); layout.addWidget(self.chk_ts)
        r1 = QHBoxLayout(); self.spin_font = QSpinBox(); self.spin_font.setRange(8, 24); self.spin_font.setValue(int(self.settings.get('log_font_size', 11))); r1.addWidget(QLabel(Translator.tr("lbl_log_font"))); r1.addWidget(self.spin_font); layout.addLayout(r1)
        layout.addWidget(QPushButton(Translator.tr("btn_clear_log"))); layout.addStretch()
    def _build_macro_tab(self): 
        layout = QVBoxLayout(self.tab_macro); self.sub_tabs_macro = QTabWidget(); layout.addWidget(self.sub_tabs_macro)
        sub_tx = QWidget(); self.sub_tabs_macro.addTab(sub_tx, Translator.tr("sub_tx_macro")); l_tx = QVBoxLayout(sub_tx)
        for i in range(1, 7): l_tx.addWidget(QLineEdit(f"Macro {i}...")); 
        l_tx.addStretch()
        sub_mail = QWidget(); self.sub_tabs_macro.addTab(sub_mail, Translator.tr("sub_email")); l_mail = QVBoxLayout(sub_mail); l_mail.addWidget(QLabel("Email Settings")); l_mail.addStretch()

    def _populate_audio_devices(self):
        try:
            devices = sd.query_devices()
            hostapis = sd.query_hostapis()
            seen_in = set(); input_devs = []
            seen_out = set(); output_devs = []
            
            # Intelligent Filtering
            for i, d in enumerate(devices):
                name = d['name']
                api_idx = d['hostapi']
                api_name = hostapis[api_idx]['name']
                
                # Skip unnecessary APIs (keep MME/DirectSound on Windows usually, or WASAPI)
                # But for now, just remove duplicates by name to clean up list
                if d['max_input_channels'] > 0:
                    if name not in seen_in:
                        input_devs.append(f"{i}: {name} ({api_name})")
                        seen_in.add(name)
                if d['max_output_channels'] > 0:
                    if name not in seen_out:
                        output_devs.append(f"{i}: {name} ({api_name})")
                        seen_out.add(name)
            
            self.combo_in.addItems(input_devs if input_devs else ["No Input Devices"])
            self.combo_out.addItems(output_devs if output_devs else ["No Output Devices"])
            
            saved_in = self.settings.get('audio_in')
            saved_out = self.settings.get('audio_out')
            
            # Try to match saved device partially if index changed
            if saved_in:
                 idx = self.combo_in.findText(saved_in, Qt.MatchFlag.MatchContains)
                 if idx >= 0: self.combo_in.setCurrentIndex(idx)
            if saved_out:
                 idx = self.combo_out.findText(saved_out, Qt.MatchFlag.MatchContains)
                 if idx >= 0: self.combo_out.setCurrentIndex(idx)
            
        except Exception:
            self.combo_in.addItem("Audio Error"); self.combo_out.addItem("Audio Error")

    def get_settings(self):
        lang_rev_map = {'English': 'en', 'Korean': 'ko', 'Japanese': 'jp'}
        return {
            'callsign': self.txt_call.text().upper(), 'grid': self.txt_grid.text().upper(),
            'theme': self.combo_theme.currentText().lower(), 'lang': lang_rev_map.get(self.combo_lang.currentText(), 'en'),
            'audio_in': self.combo_in.currentText(), 'audio_out': self.combo_out.currentText(),
            'max_freq': self.spin_maxf.value(), 'colormap': self.combo_cmap.currentText(),
            'drange': self.spin_drange.value(), 'enable_beeps': self.chk_beeps.isChecked(),
            'start_beep': self.txt_start_beep.text(), 'end_beep': self.txt_end_beep.text(),
            'log_timestamp': self.chk_ts.isChecked(), 'log_font_size': self.spin_font.value()
        }
