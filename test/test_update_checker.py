import unittest
import os
from datetime import datetime

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.UpdateChecker import UpdateChecker
from BusinessLogic.LoggingComponent import LoggingComponentClass
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class UpdateCheckerTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.logger = LoggingComponentClass()
        self.def_inter = DefinitionsFileInterface()

        try:
            os.mkdir('Definitions')
        except:
            print('Dir already exists')

    def removeDefFiles(self):
        for file in os.listdir('Definitions'):
            os.remove(f'Definitions/{file}')

    def test_no_definitions(self):
        print('[UpdatesChecker] Testing no definition file update')
        self.removeDefFiles()

        updater = UpdateChecker(self.logger, self.def_inter)

        updater.checkForUpdates()

        self.assertTrue('1716298960-definition.pkl' in os.listdir('Definitions'))

        self.removeDefFiles()

    def test_older_definitions(self):
        print('[UpdatesChecker] Testing older definition file update')
        updater = UpdateChecker(self.logger, self.def_inter)

        file = 'Definitions/1-definition.pkl'

        with open(file, 'w'):
            print('Create temp file')

        updater.checkForUpdates()

        self.assertTrue('1716298960-definition.pkl' in os.listdir('Definitions'))

        self.removeDefFiles()


if __name__ == '__main__':
    unittest.main()    