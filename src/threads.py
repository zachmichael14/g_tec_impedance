from PySide6.QtCore import QThread, Signal

import pygds
from win32serviceutil import RestartService


class ServiceRestartThread(QThread):
    restart_finished = Signal(str)

    def run(self):
        try:
            RestartService("GDS")
            self.restart_finished.emit("GDS service restarted successfully.")
        except Exception as e:
            self.restart_finished.emit(f"Unable to restart service: {str(e)}")


class ImpedanceRecordingThread(QThread):
    impedance_readings = Signal(list)
    impedance_finished = Signal(str)

    def run(self):
        try:
            device = pygds.GDS()
            impedances = device.GetImpedance()[0][:32]
            self.impedance_readings.emit(impedances)
            self.impedance_finished.emit("Impedances read successfully.")
            
        except (pygds.GDSError, AssertionError):
            self.impedance_finished.emit("Device Error: Cannot connect to gNautilus.")
            self.impedance_finished.emit("Please close BCI2000 and g.Recorder, then try again")
        finally:
            device.Close()