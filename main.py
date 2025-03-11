import sys

from PySide6.QtWidgets import QApplication, QStyleFactory

from src.control_panel import ControlPanel

def main():
    app = QApplication()
    app.setStyle(QStyleFactory.create("Fusion"))
    window = ControlPanel()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
