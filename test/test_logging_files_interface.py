import unittest
import os
from datetime import datetime

import sys
sys.path.append('../AntiBot-Desktop')

from FileSystems.LoggingFilesInterface import LoggingFilesInterface

class LoggingTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        try:
            os.mkdir('Logs')
        except:
            print('Dir already exists')

        self.removeLogs()

    def removeLogs(self):
        for file in os.listdir('Logs'):
            os.remove(f'Logs/{file}')

    def test_log_data(self):
        print('[LoggingFilesInterface] Testing logging data')
        log_inter = LoggingFilesInterface()

        data = 'log test'
        date = datetime.today().strftime('%d-%m-%Y')

        log_inter.logData(data)

        read = ''
        with open(f'Logs/{date}', 'r') as f:
            read = f.readline().replace('\n', '')

        self.assertEqual(data, read)

        self.removeLogs()

    def test_get_log_data(self):
        print('[LoggingFilesInterface] Testing getting log data')

        log_inter = LoggingFilesInterface()

        data = 'log test'
        date = datetime.today().strftime('%d-%m-%Y')

        with open(f'Logs/{date}', 'w') as f:
            f.write(data)

        read = log_inter.getLogData()

        data_dict = {date: [data]}

        self.assertDictEqual(read, data_dict)

        self.removeLogs()


if __name__ == '__main__':
    unittest.main()