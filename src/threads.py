from PySide6.QtCore import QThread, Signal

# import pygds
from win32serviceutil import RestartService


class ServiceRestartThread(QThread):
    restart_finished = Signal(bool, str)

    def run(self):
        try:
            RestartService("GDS")
            self.restart_finished.emit(True, "GDS service restarted successfully.")
        except Exception as e:
            self.restart_finished.emit(False, f"Unable to restart service: {str(e)}")


class ImpedanceRecordingThread(QThread):
    impedance_readings = Signal()
    impedance_finished = Signal(bool, str)

    def run(self):
        try:
            device = pygds.GDS()
            
        except (pygds.GDSError, AssertionError):
            self.impedance_finished.emit(False, "Device Error: Cannot connect to gNautilus.")
            self.impedance_finished.emit(False, "Please close BCI2000 and g.Recorder, then try again")
