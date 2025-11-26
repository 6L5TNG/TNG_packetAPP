from PyQt6.QtWidgets import (QDialog, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QComboBox, QGroupBox, QPushButton)
from tng_packet.core.i18n import Translator

class SettingsDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings or {}
        self.setWindowTitle(Translator.tr("menu_settings"))
        self.resize(600, 450)
        
        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # --- Tab 1: General ---
        self.tab_gen = QWidget()
        self.tabs.addTab(self.tab_gen, Translator.tr("tab_gen"))
        gen_layout = QVBoxLayout(self.tab_gen)
        
        # Station
        grp_station = QGroupBox("Station Details") # Key can be mapped if needed
        form_st = QVBoxLayout()
        self.txt_call = QLineEdit(self.settings.get('callsign', ''))
        self.txt_grid = QLineEdit(self.settings.get('grid', ''))
        
        row_call = QHBoxLayout()
        row_call.addWidget(QLabel(Translator.tr("lbl_call")))
        row_call.addWidget(self.txt_call)
        
        row_grid = QHBoxLayout()
        row_grid.addWidget(QLabel(Translator.tr("lbl_grid")))
        row_grid.addWidget(self.txt_grid)
        
        form_st.addLayout(row_call)
        form_st.addLayout(row_grid)
        grp_station.setLayout(form_st)
        gen_layout.addWidget(grp_station)
        
        # UI
        grp_ui = QGroupBox("User Interface")
        form_ui = QVBoxLayout()
        
        # Theme
        row_theme = QHBoxLayout()
        row_theme.addWidget(QLabel(Translator.tr("lbl_theme")))
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(['Light', 'Dark'])
        current_theme = self.settings.get('theme', 'light')
        self.combo_theme.setCurrentText(current_theme.capitalize())
        row_theme.addWidget(self.combo_theme)
        
        # Language
        row_lang = QHBoxLayout()
        row_lang.addWidget(QLabel(Translator.tr("lbl_lang")))
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(['English', 'Korean', 'Japanese'])
        
        lang_map = {'en': 'English', 'ko': 'Korean', 'jp': 'Japanese'}
        curr_lang_code = self.settings.get('lang', 'en')
        self.combo_lang.setCurrentText(lang_map.get(curr_lang_code, 'English'))
        row_lang.addWidget(self.combo_lang)
        
        form_ui.addLayout(row_theme)
        form_ui.addLayout(row_lang)
        grp_ui.setLayout(form_ui)
        gen_layout.addWidget(grp_ui)
        
        gen_layout.addStretch()
        
        # --- Tab 2: Audio ---
        self.tab_audio = QWidget()
        self.tabs.addTab(self.tab_audio, Translator.tr("tab_audio"))
        aud_layout = QVBoxLayout(self.tab_audio)
        aud_layout.addWidget(QLabel(Translator.tr("lbl_in")))
        self.combo_in = QComboBox()
        self.combo_in.addItems(["Default Input", "Microphone (Realtek Audio)"])
        aud_layout.addWidget(self.combo_in)
        
        aud_layout.addWidget(QLabel(Translator.tr("lbl_out")))
        self.combo_out = QComboBox()
        self.combo_out.addItems(["Default Output", "Speakers (Realtek Audio)"])
        aud_layout.addWidget(self.combo_out)
        aud_layout.addStretch()

        # --- Tab 3: Tx Macros ---
        self.tab_macro = QWidget()
        self.tabs.addTab(self.tab_macro, Translator.tr("tab_macro"))
        mac_layout = QVBoxLayout(self.tab_macro)
        mac_layout.addWidget(QLabel("Standard Messages:"))
        for i in range(1, 7):
            mac_layout.addWidget(QLineEdit(f"Macro {i} Message..."))
        mac_layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)

    def get_settings(self):
        lang_rev_map = {'English': 'en', 'Korean': 'ko', 'Japanese': 'jp'}
        return {
            'callsign': self.txt_call.text().upper(),
            'grid': self.txt_grid.text().upper(),
            'theme': self.combo_theme.currentText().lower(),
            'lang': lang_rev_map.get(self.combo_lang.currentText(), 'en')
        }
