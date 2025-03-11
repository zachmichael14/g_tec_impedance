import os
import sys

from PySide6.QtCore import QRegularExpression, QRegularExpressionMatch, Signal, Slot
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QStyleFactory, QWidget
)
from win32serviceutil import RestartService


class AppControlWidget(QWidget):
    signal_subject_id_changed = Signal(str)
    signal_session_id_changed = Signal(str)
    signal_save_dir_selected = Signal(str)

    signal_restart_requested = Signal()
    signal_impedance_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QFormLayout()
        self.setLayout(layout)

        subject_id = QLineEdit()
        subject_id.setPlaceholderText("BSI0XXS0XX")
        subject_id.textChanged.connect(self._subject_id_changed)
        layout.addRow(QLabel("Subject ID:"), subject_id)

        # Display a warning message when subject ID is not in proper format
        self.validation_message = QLabel("")
        layout.addRow(self.validation_message)

        # Hide the message if there are no errors
        self.validation_message.hide() 

        save_dir_button = QPushButton("Select Save Directory")
        save_dir_button.clicked.connect(self._select_save_directory)
        layout.addRow(save_dir_button)

        # Lazy way to create buffer space to separate widgets
        layout.addRow(QLabel(""))

        service_restart_button = QPushButton("Restart GDS")
        service_restart_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; height: 25px; margin-bottom: 5px;")
        service_restart_button.clicked.connect(self._service_restart_requested)
        layout.addRow(service_restart_button)

        impedance_button = QPushButton("Get Impedance")
        impedance_button.setStyleSheet("background-color: green; color: white; font-size: 14px; height: 50px;")
        impedance_button.clicked.connect(self._impedance_requested)
        layout.addRow(impedance_button)

    @Slot(str)
    def _subject_id_changed(self, subject_id: str) -> None:
        if not subject_id:
            self._clear_validation_message()

        elif self._validate_subject_id(subject_id):
            self.signal_subject_id_changed.emit(subject_id)

    def _validate_subject_id(self, subject_id: str) -> None:
        """Display error message if subject ID doesn't match specific format."""
        match = self._match_subject_id(subject_id)
        
        if match.hasMatch() or match.hasPartialMatch():
            self._clear_validation_message()
        else:
            self._set_error_validation_message()

    def _match_subject_id(self, subject_id) -> QRegularExpressionMatch:
        """Match the subject ID to the specified format."""
        regex = QRegularExpression("BSI[0-9]{3}S[0-9]{3}")
        match = regex.match(subject_id,
                            matchType=QRegularExpression.PartialPreferCompleteMatch)
        return match
            
    def _clear_validation_message(self):
        """Empty the validation message."""
        self.validation_message.setText("")
        self.validation_message.hide()

    def _set_error_validation_message(self):
        """Show error message to user (BSIXXXSXXX format for subject ID)"""
        self.validation_message.setText("Invalid format - please use BSI0XXS0XX")
        self.validation_message.setStyleSheet("color: red")
        self.validation_message.show()

    @Slot(str)
    def _session_id_changed(self, session_id: str) -> None:
        self.signal_session_id_changed.emit(session_id)

    @Slot(str)
    def _select_save_directory(self) -> None:
        directory = QFileDialog.getExistingDirectory(self,
                                                     "Select Save Directory",
                                                     os.path.expanduser("~"))
        if directory:
            self.signal_save_dir_selected.emit(directory)

    @Slot()
    def _service_restart_requested(self) -> None:
        self.signal_restart_requested.emit()

    @Slot()
    def _impedance_requested(self) -> None:
        self.signal_impedance_requested.emit()


class ImpedanceRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("g.tec Device Impedance Recorder")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.control_widget = AppControlWidget()       
        
        self.layout.addWidget(self.control_widget)

        self._connect_signals()

    def _connect_signals(self) -> None:
        self.control_widget.signal_subject_id_changed.connect(self._set_subject_id)
        self.control_widget.signal_session_id_changed.connect(self._set_session_id)
        self.control_widget.signal_save_dir_selected.connect(self._set_save_dir)
        self.control_widget.signal_restart_requested.connect(self._restart_service)
        self.control_widget.signal_impedance_requested.connect(self._record_impedance)

    def _set_subject_id(self, subject_id: str) -> None:
        self.subject_id = subject_id

    def _set_session_id(self, session_id: str) -> None:
        self.subject_id = session_id

    def _set_save_dir(self, save_dir: str) -> None:
        self.save_dir = save_dir

    def _restart_service(self) -> None:
        """Stop, then restart, the g.tec Device Service."""
        try:
            RestartService("GDS")
        except:
            # pywintypes.error: (5, 'OpenSCManager', 'Access is denied.')
            print("Unable to restart service.")

    def _record_impedance(self) -> None:
        pass

def main():
    app = QApplication()
    app.setStyle(QStyleFactory.create("Fusion"))
    window = ImpedanceRecorder()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
