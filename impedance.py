import os
import sys

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QStyleFactory, QWidget
)

class AppControlWidget(QWidget):
    signal_subject_id_changed = Signal(str)
    signal_session_id_changed = Signal(str)
    signal_save_dir_selected = Signal(str)

    signal_restart_requested = Signal()
    signal_impedance_requested = Signal()

    def __init__(self):
        super().__init__()

        layout = QFormLayout()
       
        subject_id_field = QLineEdit()
        subject_id_field.textChanged.connect(self._subject_id_changed)
        layout.addRow(QLabel("Subject ID:"), subject_id_field)
       
        session_id_field = QLineEdit()
        session_id_field.textChanged.connect(self._session_id_changed)
        layout.addRow(QLabel("Session Number:"), session_id_field)
       
        save_dir_button = QPushButton("Select Save Directory")
        save_dir_button.clicked.connect(self._select_save_directory)
        layout.addRow(save_dir_button)

        service_restart_button = QPushButton("Restart GDS")
        service_restart_button.setStyleSheet("background-color: blue; color: white; font-size: 14px; height: 50px;")
        service_restart_button.clicked.connect(self._service_restart_requested)
        layout.addRow(service_restart_button)

        impedance_button = QPushButton("Get Impedance")
        impedance_button.setStyleSheet("background-color: green; color: white; font-size: 14px; height: 50px;")
        impedance_button.clicked.connect(self._impedance_requested)
        layout.addRow(impedance_button)

        self.setLayout(layout)

    @Slot(str)
    def _subject_id_changed(self, subject_id):
        self.signal_subject_id_changed.emit(subject_id)
        # TODO: Add validation for BSI at beginnin of subject id
        # The app prepends "BSI" to subject id, so if it is not included
        # add it. If it is included, do not prepend. 

        #TODO: validat formate "BSIXXXSXXX" where x are numeric chars

        #TODO: Do session id and subject id need to be different?
    
    @Slot(str)
    def _session_id_changed(self, session_id):
        self.signal_session_id_changed.emit(session_id)

    @Slot(str)
    def _select_save_directory(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     "Select Save Directory",
                                                     os.path.expanduser("~"))
        if directory:
            self.signal_save_dir_selected.emit(directory)

    @Slot()
    def _service_restart_requested(self):
        self.signal_restart_requested.emit()

    @Slot()
    def _impedance_requested(self):
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

    def _connect_signals(self):
        self.control_widget.signal_subject_id_changed.connect(self._set_subject_id)
        self.control_widget.signal_session_id_changed.connect(self._set_session_id)
        self.control_widget.signal_save_dir_selected.connect(self._set_save_dir)
        self.control_widget.signal_restart_requested.connect(self._restart_service)
        self.control_widget.signal_impedance_requested.connect(self._record_impedance)

    def _set_subject_id(self, subject_id):
        self.subject_id = subject_id

    def _set_session_id(self, session_id):
        self.subject_id = session_id

    def _set_save_dir(self, save_dir):
        self.save_dir = save_dir

    def _restart_service(self):
        pass

    def _record_impedance(self):
        pass


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = ImpedanceRecorder()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
