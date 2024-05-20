import time
from PyQt6.QtCore import QObject

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.UpdateChecker import UpdateChecker
from BusinessLogic.LoggingComponent import LoggingComponentClass

class UpdatesSchedulerClass(QObject):
    def __init__(self, logger: LoggingComponentClass):
        super().__init__()
        self.logger = logger
        self.updater = UpdateChecker(self.logger)

    def run(self):
        while True:
            self.updater.checkForUpdates()
            time.sleep(7200)