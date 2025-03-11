from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QWidget
)
from win32serviceutil import RestartService

from ui.controls_widget import ControlsWidget
from ui.status_widget import StatusWidget

class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("g.tec Device Impedance Recorder")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        self.control_widget = ControlsWidget()       
        
        layout.addWidget(self.control_widget)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.control_widget.signal_restart_requested.connect(self._restart_service)
        self.control_widget.signal_impedance_requested.connect(self._record_impedance)

    def _restart_service(self) -> None:
        """Stop, then restart, the g.tec Device Service."""
        try:
            RestartService("GDS")
        except:
            # pywintypes.error: (5, 'OpenSCManager', 'Access is denied.')
            print("Unable to restart service.")

    def _record_impedance(self) -> None:
        pass
