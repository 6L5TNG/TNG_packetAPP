from PyQt6.QtWidgets import (QDialog, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QGroupBox, QPushButton, QSpinBox, QDoubleSpinBox, QCheckBox, QSlider)
from PyQt6.QtCore import Qt
from tng_packet.core.i18n import Translator
import sounddevice as sd

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.setWindowTitle(Translator.tr("menu_settings"))
        self.resize(750, 650)
        
        # Pure Native Style (Dark)
        self.setStyleSheet("""
           QDialog { background-color: #2b2b2b; color: #eee; }
           QLabel, QCheckBox { color: #eee; }
           QGroupBox { color: #eee; border: 1px solid #555; margin-top: 6px; font-weight: bold; }
           QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }
           QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox { background-color: #333; color: #eee; border: 1px solid #555; padding: 3px; }
           QTabWidget::pane { border: 1px solid #555; background: #2b2b2b; }
           QTabBar::tab { background: #333; color: #aaa; padding: 6px 12px; }
           QTabBar::tab:selected { background: #444; color: white; border-bottom: 2px solid #0078d7; }
           QPushButton { background-color: #444; color: white; border: 1px solid #555; padding: 5px; border-radius: 3px; }
           QPushButton:hover { background-color: #555; }
        """)

        layout = QVBoxLayout(self)
        self.main_tabs = QTabWidget(); layout.addWidget(self.main_tabs)
        
        self.tab_gen = QWidget(); self.main_tabs.addTab(self.tab_gen, Translator.tr("tab_gen"))
        self.tab_audio = QWidget(); self.main_tabs.addTab(self.tab_audio, Translator.tr("tab_audio"))
        self.tab_trans = QWidget(); self.main_tabs.addTab(self.tab_trans, Translator.tr("tab_trans"))
        self.tab_recv = QWidget(); self.main_tabs.addTab(self.tab_recv, Translator.tr("tab_recv"))
        self.tab_log = QWidget(); self.main_tabs.addTab(self.tab_log, Translator.tr("tab_log"))
        self.tab_macro = QWidget(); self.main_tabs.addTab(self.tab_macro, Translator.tr("tab_macro"))

        self._build_general_tab()
        self._build_audio_tab()
        self._build_transmit_tab()
        self._build_receive_tab()
        self._build_log_tab()
        self._build_macro_tab()
        
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
        self.combo_lang = QComboBox(); self.combo_lang.addItems(['English', 'Korean', 'Japanese'])
        lang_map = {'en': 'English', 'ko': 'Korean', 'jp': 'Japanese'}
        self.combo_lang.setCurrentText(lang_map.get(self.settings.get('lang', 'en'), 'English'))
        r3 = QHBoxLayout(); r3.addWidget(QLabel(Translator.tr("lbl_lang"))); r3.addWidget(self.combo_lang)
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
        layout = QVBoxLayout(self.tab_trans)
        self.sub_tabs_tx = QTabWidget(); layout.addWidget(self.sub_tabs_tx)
        sub_mpda = QWidget(); self.sub_tabs_tx.addTab(sub_mpda, Translator.tr("sub_mpda"))
        l_mpda = QVBoxLayout(sub_mpda)
        self.chk_beeps = QCheckBox(Translator.tr("lbl_beeps")); self.chk_beeps.setChecked(self.settings.get('enable_beeps', True)); l_mpda.addWidget(self.chk_beeps)
        self.txt_start_beep = QLineEdit(self.settings.get('start_beep', '250:400:250')); self.txt_end_beep = QLineEdit(self.settings.get('end_beep', '250:400:250'))
        l_mpda.addWidget(QLabel(Translator.tr("lbl_start_beep"))); l_mpda.addWidget(self.txt_start_beep)
        l_mpda.addWidget(QLabel(Translator.tr("lbl_end_beep"))); l_mpda.addWidget(self.txt_end_beep); l_mpda.addStretch()
        sub_chirp = QWidget(); self.sub_tabs_tx.addTab(sub_chirp, Translator.tr("sub_chirp"))
        QVBoxLayout(sub_chirp).addWidget(QLabel("Chirp Settings"))

    def _build_receive_tab(self):
        layout = QVBoxLayout(self.tab_recv)
        self.sub_tabs_rx = QTabWidget(); layout.addWidget(self.sub_tabs_rx)
        
        # MPDA/Chirp Placeholders
        sub_mpda = QWidget(); self.sub_tabs_rx.addTab(sub_mpda, Translator.tr("sub_mpda")); QVBoxLayout(sub_mpda).addWidget(QLabel("RX Settings"))
        sub_chirp = QWidget(); self.sub_tabs_rx.addTab(sub_chirp, Translator.tr("sub_chirp")); QVBoxLayout(sub_chirp).addWidget(QLabel("Chirp RX Settings"))
        
        # Waterfall - Detailed Settings
        sub_wf = QWidget(); self.sub_tabs_rx.addTab(sub_wf, Translator.tr("sub_wf"))
        l_wf = QVBoxLayout(sub_wf)
        
        self.spin_wf_speed = QSpinBox(); self.spin_wf_speed.setRange(1, 200); self.spin_wf_speed.setValue(int(self.settings.get('wf_speed', 50)))
        l_wf.addWidget(QLabel(Translator.tr("lbl_wf_speed"))); l_wf.addWidget(self.spin_wf_speed)
        
        self.combo_cmap = QComboBox(); self.combo_cmap.addItems(['magma', 'inferno', 'plasma', 'viridis', 'turbo', 'grey', 'thermal', 'bipolar'])
        self.combo_cmap.setCurrentText(self.settings.get('colormap', 'magma'))
        l_wf.addWidget(QLabel(Translator.tr("lbl_cmap"))); l_wf.addWidget(self.combo_cmap)
        
        self.spin_maxf = QSpinBox(); self.spin_maxf.setRange(1000,20000); self.spin_maxf.setValue(int(self.settings.get('max_freq', 3000)))
        l_wf.addWidget(QLabel(Translator.tr("lbl_maxf"))); l_wf.addWidget(self.spin_maxf)
        
        self.spin_drange = QDoubleSpinBox(); self.spin_drange.setRange(10.0, 120.0); self.spin_drange.setValue(float(self.settings.get('drange', 60.0)))
        l_wf.addWidget(QLabel(Translator.tr("lbl_drange"))); l_wf.addWidget(self.spin_drange)

        self.chk_smooth = QCheckBox(Translator.tr("lbl_smooth")); self.chk_smooth.setChecked(self.settings.get('wf_smooth', True))
        l_wf.addWidget(self.chk_smooth)
        l_wf.addStretch()
        
        # Spectrum - Detailed Settings
        sub_spec = QWidget(); self.sub_tabs_rx.addTab(sub_spec, Translator.tr("sub_spec"))
        l_spec = QVBoxLayout(sub_spec)
        
        self.spin_spec_gain = QDoubleSpinBox(); self.spin_spec_gain.setRange(0.1, 10.0); self.spin_spec_gain.setSingleStep(0.1)
        self.spin_spec_gain.setValue(float(self.settings.get('spec_gain', 1.0)))
        l_spec.addWidget(QLabel(Translator.tr("lbl_spec_gain"))); l_spec.addWidget(self.spin_spec_gain)
        
        self.spin_ref_lvl = QDoubleSpinBox(); self.spin_ref_lvl.setRange(-100, 100); self.spin_ref_lvl.setValue(float(self.settings.get('ref_level', 0.0)))
        l_spec.addWidget(QLabel(Translator.tr("lbl_ref_lvl"))); l_spec.addWidget(self.spin_ref_lvl)
        
        self.spin_line_width = QSpinBox(); self.spin_line_width.setRange(1, 5); self.spin_line_width.setValue(int(self.settings.get('spec_line_width', 1)))
        l_spec.addWidget(QLabel(Translator.tr("lbl_line_width"))); l_spec.addWidget(self.spin_line_width)
        
        self.chk_fill = QCheckBox(Translator.tr("lbl_fill")); self.chk_fill.setChecked(self.settings.get('spec_fill', False))
        l_spec.addWidget(self.chk_fill)
        l_spec.addStretch()

    def _build_log_tab(self):
        layout = QVBoxLayout(self.tab_log)
        self.chk_ts = QCheckBox(Translator.tr("lbl_log_ts")); self.chk_ts.setChecked(self.settings.get('log_timestamp', True)); layout.addWidget(self.chk_ts)
        self.spin_font = QSpinBox(); self.spin_font.setRange(8, 24); self.spin_font.setValue(int(self.settings.get('log_font_size', 11))); layout.addWidget(self.spin_font)
        layout.addWidget(QPushButton(Translator.tr("btn_clear_log"))); layout.addStretch()
    
    def _build_macro_tab(self):
        layout = QVBoxLayout(self.tab_macro)
        self.sub_tabs_macro = QTabWidget(); layout.addWidget(self.sub_tabs_macro)
        sub_tx = QWidget(); self.sub_tabs_macro.addTab(sub_tx, Translator.tr("sub_tx_macro")); l_tx = QVBoxLayout(sub_tx)
        for i in range(6): l_tx.addWidget(QLineEdit(f"Macro {i+1}"))
        l_tx.addStretch()
        sub_mail = QWidget(); self.sub_tabs_macro.addTab(sub_mail, Translator.tr("sub_email"))

    def _populate_audio_devices(self):
        try:
            devices = sd.query_devices()
            unique_in = set(); unique_out = set(); self.combo_in.clear(); self.combo_out.clear()
            for d in devices:
                name = d['name']
                if d['max_input_channels']>0 and name not in unique_in: self.combo_in.addItem(name); unique_in.add(name)
                if d['max_output_channels']>0 and name not in unique_out: self.combo_out.addItem(name); unique_out.add(name)
            if self.settings.get('audio_in'): self.combo_in.setCurrentText(self.settings.get('audio_in'))
            if self.settings.get('audio_out'): self.combo_out.setCurrentText(self.settings.get('audio_out'))
        except: pass

    def get_settings(self):
        lang_rev = {'English':'en','Korean':'ko','Japanese':'jp'}
        in_n = self.combo_in.currentText(); out_n = self.combo_out.currentText(); in_i = None; out_i = None
        try: devs = sd.query_devices(); in_i = next((i for i,d in enumerate(devs) if d['name']==in_n),None); out_i = next((i for i,d in enumerate(devs) if d['name']==out_n),None)
        except: pass
        return {
            'callsign': self.txt_call.text().upper(), 'grid': self.txt_grid.text().upper(),
            'theme': 'dark', 'lang': lang_rev.get(self.combo_lang.currentText(),'en'),
            'audio_in': in_n, 'audio_in_idx': in_i, 'audio_out': out_n, 'audio_out_idx': out_i,
            'wf_speed': self.spin_wf_speed.value(), 'colormap': self.combo_cmap.currentText(),
            'max_freq': self.spin_maxf.value(), 'drange': self.spin_drange.value(), 'wf_smooth': self.chk_smooth.isChecked(),
            'spec_gain': self.spin_spec_gain.value(), 'ref_level': self.spin_ref_lvl.value(),
            'spec_line_width': self.spin_line_width.value(), 'spec_fill': self.chk_fill.isChecked(),
            'enable_beeps': self.chk_beeps.isChecked(), 'start_beep': self.txt_start_beep.text(), 'end_beep': self.txt_end_beep.text(),
            'log_timestamp': self.chk_ts.isChecked(), 'log_font_size': self.spin_font.value()
        }
