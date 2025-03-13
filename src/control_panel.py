import csv
import os
import re

from PySide6.QtWidgets import (
    QHBoxLayout, QMainWindow, QWidget
)

from src.threads import ImpedanceRecordingThread, ServiceRestartThread
from ui.controls_widget import ControlsWidget
from ui.status_widget import StatusWidget


class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("g.tec Device Impedance Recorder")

        self.restart_thread = ServiceRestartThread()
        self.restart_thread.restart_finished.connect(self._on_restart_finished)

        self.impedance_thread = ImpedanceRecordingThread()
        self.impedance_thread.impedance_finished.connect(self._on_impedance_finished)
        self.impedance_thread.impedance_readings.connect(self._save_impedance_values)

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
        self.control_widget.toggle_restart_button_enabled(False)
        self.restart_thread.start()

    def _on_restart_finished(self, message: str) -> None:
        """Handle completion of service restart."""
        self.status_widget.append_message(message)
        self.control_widget.toggle_restart_button_enabled(True)
    
    def _record_impedance(self) -> None:
        self.status_widget.append_message("Recording impedance...")
        self.control_widget.toggle_impedance_button_enabled(False)
        self.impedance_thread.start()

    def _on_impedance_finished(self, message: str) -> None:
        self.status_widget.append_message(message)
        self.control_widget.toggle_impedance_button_enabled(True)

    def _save_impedance_values(self, impedances: list) -> None:
        save_dir = self.control_widget.get_save_dir().strip()
        subject_id = self.control_widget.get_subject_id().strip()

        self._pretty_print_impedances(impedances)
              
        if not save_dir:
            self.status_widget.append_message("WARNING: Cannot save values - no save directory selected")
            return

        if subject_id == "":
            self.status_widget.append_message("WARNING: Cannot save values - no subject ID specified")
            return
        
        filepath = self._create_file(save_dir, subject_id)

        with open(filepath, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Channel", "Impedance"])
            for index, value in enumerate(impedances):
                writer.writerow([f"{index + 1}", value])
        
    
            self.status_widget.append_message(f"Impedances saved to {filepath}")
    
    def _pretty_print_impedances(self, impedances) -> None:
        """Display impedances with accompanying channel in status widget"""
        for index, impedance in enumerate(impedances):
            self.status_widget.append_message(f"Channel {index + 1}: {impedance}")

    def _create_file(self, save_dir: str, subject_id: str) -> str:
        """Return the path of the file in which to record impedances."""
        subdirectory = self._create_subdirectory(save_dir, subject_id)

        base_filename = f"{subject_id}_impedance"
        file_suffix = self._get_file_number_suffix(subdirectory, base_filename)
        filepath = os.path.join(subdirectory, f"{base_filename}{file_suffix}.csv")
        print(type(filepath))
        return filepath
    
    def _get_file_number_suffix(self,
                                subdirectory: str,
                                base_filename: str) -> str:
        """Return the next file number (ex. _1, _2) based on existing files in the specified directory.
        """
        existing_files = [file for file in os.listdir(subdirectory) if re.match(f"{base_filename}(_\\d+)?\\.csv", file)]

        if existing_files:
            numbers = [int(re.search(r"_(\d+)\.csv", file).group(1)) for file in existing_files if re.search(r"_(\d+)\.csv", file)]
            next_number = max(numbers, default=0) + 1
            return f"_{next_number}"
        else:
            return ""

    def _create_subdirectory(self, save_dir: str, subject_id: str) -> str:
        """Create the necessary directories for saving impedance values."""
        base_filename = f"{subject_id}_impedance"
        subdirectory = os.path.join(save_dir, base_filename)

        if not os.path.exists(subdirectory):
            os.makedirs(subdirectory)

        return subdirectory
