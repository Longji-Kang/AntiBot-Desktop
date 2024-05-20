import sys 
import time
from PyQt6.QtCore import QObject

sys.path.append('../AntiBot-Desktop')

from BusinessLogic.LoggingComponents.LogWriter import LogWriter
from BusinessLogic.LoggingComponents.LogReader import LogReader
from FileSystems.LoggingFilesInterface import LoggingFilesInterface

class LoggingComponentClass():
    def __init__(self):
        self.files_interface = LoggingFilesInterface()
        self.writer = LogWriter(self.files_interface)
        self.reader = LogReader()

    def log(self, log_data: str, subsystem: str):
        self.writer.writeToLog(log_data, subsystem)

    def get_logs(self):
        data = self.reader.getData()
        return data