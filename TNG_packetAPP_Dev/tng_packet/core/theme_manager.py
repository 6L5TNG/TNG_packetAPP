from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt

class ThemeManager:
    @staticmethod
    def apply_theme(app, main_window=None, theme_name='light'):
        # Set global palette first
        palette = QPalette()
        is_dark = (str(theme_name).lower() == 'dark')

        if is_dark:
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

        if app is not None:
            app.setPalette(palette)

        # Safely style widgets only if they exist on main_window
        if main_window is None:
            return

        # Define per-widget styles for dark/light
        def style_of(name):
            mapping = {
                'band_activity': (
                    "background-color: #222; color: #0f0; font-family: Consolas; font-size: 11pt; border: 1px solid #444;",
                    "background-color: #fff; color: #000; font-family: Consolas; font-size: 11pt; border: 1px solid #ccc;",
                ),
                'rx_window': (
                    "background-color: #1e1e1e; color: #0ff; font-family: Consolas; font-size: 12pt; border: 1px solid #444;",
                    "background-color: #f9f9f9; color: #000; font-family: Consolas; font-size: 12pt; border: 1px solid #ccc;",
                ),
                # 아래 항목들은 현재 메인창에는 없지만(분리된 창으로 이동) 혹시 남아있을 수 있어 안전 적용
                'scope_container': (
                    "background-color: black; border: 1px solid #555;",
                    "background-color: #e0e0e0; border: 1px solid #aaa;",
                ),
                'spectrum_label': (
                    "color: yellow; border-bottom: 1px dashed #333;",
                    "color: blue; border-bottom: 1px dashed #ccc;",
                ),
                'waterfall_label': (
                    "color: cyan;",
                    "color: black;",
                ),
            }
            return mapping.get(name, (None, None))

        for attr in ['band_activity', 'rx_window', 'scope_container', 'spectrum_label', 'waterfall_label']:
            if hasattr(main_window, attr):
                dark_sheet, light_sheet = style_of(attr)
                sheet = dark_sheet if is_dark else light_sheet
                if sheet:
                    try:
                        getattr(main_window, attr).setStyleSheet(sheet)
                    except Exception:
                        pass
