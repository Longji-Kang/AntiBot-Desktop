import sys
from datetime import datetime

import sys
sys.path.append('../AntiBot-Desktop')

from FileSystems.LoggingFilesInterface import LoggingFilesInterface

class LogWriter:
    def __init__(self, logging_interface: LoggingFilesInterface):
        self.logging = logging_interface

    def writeToLog(self, log_info: str, subsystem: str):
        log_data = f"({subsystem})[{datetime.today().strftime('%d-%m-%Y/%H:%M:%S')}] - {log_info}"

        self.logging.logData(log_data)
