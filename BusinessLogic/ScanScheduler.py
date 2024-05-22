import time
from PyQt6.QtCore import QObject

import sys
sys.path.append('../AntiBot-DeskTop')

from BusinessLogic.LoggingComponent import LoggingComponentClass
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface
from BusinessLogic.Scanner import Scanner

class ScanScheduler(QObject):
    def __init__(self, logger: LoggingComponentClass, definitions: DefinitionsFileInterface):
        super().__init__()
        self.logger = logger
        self.definitions = definitions
        self.scanner = Scanner(self.definitions, self.logger)

    def run(self):
        while True:
            time.sleep(10)
            self.scanner.scan()
            time.sleep(600)
