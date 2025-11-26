from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class ThemeManager:
    @staticmethod
    def apply_theme(app, main_window, theme_name='light'):
        palette = QPalette()
        is_dark = (theme_name == 'dark')

        if is_dark:
            # Dark Theme (Tactical)
            bg_color = QColor(30, 30, 30)
            text_color = QColor(220, 220, 220)
            base_color = QColor(25, 25, 25)
            btn_color = QColor(45, 45, 45)
            highlight = QColor(42, 130, 218)
            
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, bg_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, base_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, btn_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, highlight)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        else:
            # Light Theme (Standard)
            bg_color = QColor(240, 240, 240)
            text_color = QColor(0, 0, 0)
            base_color = QColor(255, 255, 255)
            btn_color = QColor(225, 225, 225)
            highlight = QColor(0, 120, 215)

            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Window, bg_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.WindowText, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Base, base_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Text, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Button, btn_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.ButtonText, text_color)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.Highlight, highlight)
            palette.setColor(QPalette.ColorGroup.All, QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
        
        app.setPalette(palette)

        # --- Apply styles to specific widgets ---
        if is_dark:
            # Waterfall Area
            main_window.scope_container.setStyleSheet("background-color: black; border: 1px solid #555;")
            main_window.spectrum_label.setStyleSheet("color: yellow; border-bottom: 1px dashed #333;")
            main_window.waterfall_label.setStyleSheet("color: cyan;")
            
            # Text Areas
            sheet_text = "background-color: #222; color: #0f0; font-family: Consolas; font-size: 11pt; border: 1px solid #444;"
            main_window.band_activity.setStyleSheet(sheet_text)
            sheet_rx = "background-color: #1e1e1e; color: #0ff; font-family: Consolas; font-size: 12pt; border: 1px solid #444;"
            main_window.rx_window.setStyleSheet(sheet_rx)
            
        else:
            # Waterfall Area (Light Mode)
            main_window.scope_container.setStyleSheet("background-color: #e0e0e0; border: 1px solid #aaa;")
            main_window.spectrum_label.setStyleSheet("color: blue; border-bottom: 1px dashed #ccc;")
            main_window.waterfall_label.setStyleSheet("color: black;")
            
            # Text Areas
            sheet_text = "background-color: #fff; color: #000; font-family: Consolas; font-size: 11pt; border: 1px solid #ccc;"
            main_window.band_activity.setStyleSheet(sheet_text)
            sheet_rx = "background-color: #f9f9f9; color: #000; font-family: Consolas; font-size: 12pt; border: 1px solid #ccc;"
            main_window.rx_window.setStyleSheet(sheet_rx)
