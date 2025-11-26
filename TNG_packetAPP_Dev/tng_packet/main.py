import sys
from PyQt6.QtWidgets import QApplication
from tng_packet.ui.main_window import MainWindow
from tng_packet.core.settings import load_settings

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Load Settings
    settings = load_settings()

    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
