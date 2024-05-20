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
        self.tryLock()

        try:
            file_name = datetime.today().strftime('%d-%m-%Y')
            file_dir = f'{self.path}/{file_name}'

            if not os.path.exists(self.path):
                os.mkdir(self.path)

            with open(file_dir, 'a') as file:
                file.write(f'{log_data}\n')

        finally:
            self.unlock()

    def getLogData(self):
        self.tryLock()
        data = {}
        try:
            for log_file in os.listdir(self.path):
                content = []
                with open(f'{self.path}{log_file}') as curr_file:
                    for line in curr_file:
                        content.append(line)
                
                data.update({log_file : content})

        finally:
            self.unlock()

        return data