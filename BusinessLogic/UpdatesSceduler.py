import sys
sys.path.append('../AntiBot-Desktop')

import time
from PyQt6.QtCore import QObject
from BusinessLogic.UpdateChecker import UpdateChecker

class UpdatesSchedulerClass(QObject):
    def __init__(self):
        super().__init__()
        self.updater = UpdateChecker()

    def run(self):
        while True:
            self.updater.checkForUpdates()
            time.sleep(7200)