import sys

from PySide6.QtWidgets import (
    QApplication, QHBoxLayout, QWidget, QFormLayout, QLabel, QLineEdit,
    QPushButton, QMainWindow, QStyleFactory
)

class AppControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout()
       
        self.subject_id_field = QLineEdit()
        layout.addRow(QLabel("Subject ID:"), self.subject_id_field)
       
        self.session_field = QLineEdit()
        layout.addRow(QLabel("Session Number:"), self.session_field)
       
        self.save_dir_button = QPushButton("Select Save Directory")
        layout.addRow(self.save_dir_button)

        self.service_restart_button = QPushButton("Restart Service")
        self.service_restart_button.setStyleSheet("background-color: blue; color: white; font-size: 14px;")
        self.service_restart_button.setFixedHeight(75)
        layout.addRow(self.service_restart_button)


        self.submit_button = QPushButton("Get Impedance")
        self.submit_button.setStyleSheet("background-color: green; color: white; font-size: 14px;")
        self.submit_button.setFixedHeight(75)
        layout.addRow(self.submit_button)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("g.tec Device Impedance Recorder")
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QHBoxLayout(self.central_widget)
        
        self.control_widget = AppControlWidget()
        # self.status_widget = AppStatusWidget()
        
        # self.status_widget.setStyleSheet("background-color: #e0e0e0;")
        
        self.layout.addWidget(self.control_widget)
        # self.layout.addWidget(self.status_widget)


def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
