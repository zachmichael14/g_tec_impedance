import os

from PySide6.QtCore import (
    QRegularExpression, QRegularExpressionMatch, Signal, Slot
)
from PySide6.QtWidgets import (
    QFileDialog, QFormLayout, QLabel, QLineEdit,
    QPushButton, QWidget
)

class ControlsWidget(QWidget):
    signal_restart_requested = Signal()
    signal_impedance_requested = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.subject_id = QLineEdit()
        # Display a warning message when subject ID is not in proper format
        self.warning_message = QLabel("")
        self.save_dir = ""

        self._init_ui()

    def _init_ui(self):
        layout = QFormLayout()
        self.setLayout(layout)

        self.subject_id.setPlaceholderText("BSI0XXS0XX")
        self.subject_id.textChanged.connect(self._subject_id_changed)
        layout.addRow(QLabel("Subject ID:"), self.subject_id)

        # Hide the message if there are no errors
        self.warning_message.hide() 
        layout.addRow(self.warning_message)
        
        save_dir_button = QPushButton("Select Save Directory")
        save_dir_button.clicked.connect(self._select_save_directory)
        layout.addRow(save_dir_button)

        # Lazy way to create buffer space to separate widgets
        layout.addRow(QLabel(""))

        self.service_restart_button = QPushButton("Restart GDS")
        self.service_restart_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; height: 25px; margin-bottom: 5px;")
        self.service_restart_button.clicked.connect(self._service_restart_requested)
        layout.addRow(self.service_restart_button)

        self.impedance_button = QPushButton("Get Impedance")
        self.impedance_button.setStyleSheet("background-color: green; color: white; font-size: 14px; height: 50px;")
        self.impedance_button.clicked.connect(self._impedance_requested)
        layout.addRow(self.impedance_button)

    def get_subject_id(self) -> str:
        """Return current subject ID."""

        return self.subject_id.text()
    
    def get_save_dir(self) -> str:
        """Return selected save directory."""
        return self.save_dir
    
    def toggle_restart_button_enabled(self, enabled: bool) -> None:
        self.service_restart_button.setEnabled(enabled)
        if enabled:
            self.service_restart_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; height: 25px; margin-bottom: 5px;")
        else:
            self.service_restart_button.setStyleSheet("background-color: grey; color: white; font-size: 14px; height: 25px; margin-bottom: 5px;")
            
    def toggle_impedance_button_enabled(self, enabled: bool) -> None:
        self.impedance_button.setEnabled(enabled)
        if enabled:
            self.impedance_button.setStyleSheet("background-color: green; color: white; font-size: 14px; height: 50px;")
        else:
            self.impedance_button.setStyleSheet("background-color: grey; color: white; font-size: 14px; height: 50px;")

    @Slot(str)
    def _select_save_directory(self) -> None:
        """Display a dialog to select a folder to save impedance values in."""
        directory = QFileDialog.getExistingDirectory(self,
                                                     "Select Save Directory",
                                                     os.path.expanduser("~"))
        if directory:
            self.save_dir = directory

    @Slot()
    def _service_restart_requested(self) -> None:
        """Emit a signal that the restart button has been pressed."""
        self.signal_restart_requested.emit()

    @Slot()
    def _impedance_requested(self) -> None:
        """Emit a signal that the impedance button has been pressed."""
        self.signal_impedance_requested.emit()

    @Slot(str)
    def _subject_id_changed(self, subject_id: str) -> None:
        """
        Validate the subject ID, if there is one.
        
        If the field is empty, hide the warning message.
        """
        if not subject_id:
            self._hide_warning_message()
            return
        
        self._validate_subject_id(subject_id)

    def _validate_subject_id(self, subject_id: str) -> None:
        """Display error message if subject ID doesn't match specific format.
        
        If the format matches, hide any error messages.
        """
        match = self._match_subject_id(subject_id)
        
        if match.hasMatch() or match.hasPartialMatch():
            self._hide_warning_message()
        else:
            self._show_warning_message()

    def _match_subject_id(self, subject_id) -> QRegularExpressionMatch:
        """Match the subject ID to the specified format."""
        regex = QRegularExpression("BSI[0-9]{3}S[0-9]{3}")
        match = regex.match(subject_id,
                            matchType=QRegularExpression.PartialPreferCompleteMatch)
        return match
            
    def _hide_warning_message(self) -> None:
        """Clear and hide the validation message."""
        self.warning_message.setText("")
        self.warning_message.hide()

    def _show_warning_message(self) -> None:
        """Show error message to user (BSIXXXSXXX format for subject ID)"""
        self.warning_message.setText("Invalid format - please use BSI0XXS0XX")
        self.warning_message.setStyleSheet("color: red")
        self.warning_message.show()
