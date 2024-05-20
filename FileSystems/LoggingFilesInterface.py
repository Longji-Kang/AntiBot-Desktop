import sys
import os
import threading
from datetime import datetime

class LoggingFilesInterface:
    path = 'Logs/'

    def __init__(self):
        self.lock = threading.Lock()

    def tryLock(self):
        self.lock.acquire()

    def unlock(self):
        self.lock.release()

    def logData(self, log_data):
        print('try lock')
        self.tryLock()

        try:
            file_name = datetime.today().strftime('%d-%m-%Y')
            file_dir = f'{self.path}/{file_name}'

            with open(file_dir, 'a') as file:
                file.write(f'{log_data}\n')

        finally:
            self.unlock()