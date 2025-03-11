from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QWidget
)

from src.threads import ServiceRestartThread
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
        self.status_widget = StatusWidget()

        layout.addWidget(self.control_widget)
        layout.addWidget(self.status_widget)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.control_widget.signal_restart_requested.connect(self._restart_service)
        self.control_widget.signal_impedance_requested.connect(self._record_impedance)

    def _restart_service(self) -> None:
        """Stop, then restart, the g.tec Device Service in a separate thread."""
        self.status_widget.append_message("Restarting GDS service...")
    
        self.control_widget.setEnabled(False)
    
        self.restart_thread = ServiceRestartThread()
        self.restart_thread.restart_finished.connect(self._on_restart_finished)
        self.restart_thread.start()

    def _on_restart_finished(self, success: bool, message: str) -> None:
        """Handle completion of service restart."""
        self.status_widget.append_message(message)
        self.control_widget.setEnabled(True)

    def _record_impedance(self) -> None:
        pass
