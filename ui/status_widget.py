from datetime import datetime

from PySide6.QtWidgets import (QHBoxLayout, QWidget, QTextEdit)


class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)

        layout = QHBoxLayout()
        layout.addWidget(self.status_output)
        self.setLayout(layout)

    def append_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_output.append(f"[{timestamp}] {message}")

    def update_last_message(self, message):
        """Remove the last line and add the updated message."""
        self.status_output.undo()
        self.append_message(message)
