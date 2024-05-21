import os
import urllib.request
from threading import Lock

class DefinitionsFileInterface:
    path = 'Definitions/'

    def __init__(self):
        self.lock = Lock()

    def getLock(self):
        self.lock.acquire()

    def unlock(self):
        self.lock.release()

    def getCurrentFile(self):
        current = None

        try:
            self.getLock()

            if not os.path.exists(self.path):
                os.mkdir(self.path)

            for file_name in os.listdir('Definitions'):
                if file_name.endswith('definition.pkl'):
                    current = file_name
                    break
        finally:
            self.unlock()

        return current

    def getCurrentVersion(self, current_file: str):
        try:
            self.getLock()
            if current_file == None:
                return None
            else: 
                current_version = current_file.split('-')[0]
                return current_version
        finally:
            self.unlock()
    
    def downloadFile(self, url: str):
        try:
            self.getLock()

            url_split        = url.split('/')
            update_file_name = url_split[len(url_split) - 1]
            urllib.request.urlretrieve(url, f'{self.path}{update_file_name}')
        finally:
            self.unlock()

    def updateFile(self, url: str, current_version: str, current_file: str = None):
        status = False
        try:
            self.getLock()

            url_split        = url.split('/')
            update_file_name = url_split[len(url_split) - 1]

            if current_version < update_file_name.split('-')[0]:
                os.remove(f'{self.path}{current_file}')
                urllib.request.urlretrieve(url, f'{self.path}{update_file_name}')
                status = True
        finally:
            self.unlock()

        return status
        
        
    def writeLastUpdate(self, date_time: str):
        try:
            self.getLock()
            with open(f'{self.path}update_info.txt', 'w') as file:
                file.write(date_time)
        finally:
            self.unlock()

    def writeLastScan(self, date_time: str):
        try:
            self.getLock()
            with open(f'{self.path}scan_info.txt', 'w') as file:
                file.write(date_time)
        finally:
            self.unlock()

    def getLastScan(self):
        scan = ''

        try:
            self.getLock()

            if os.path.exists(f'{self.path}scan_info.txt'):
                with open(f'{self.path}scan_info.txt', 'r') as file:
                    scan = file.readline()
            else:
                scan = 'None'
        finally:
            self.unlock()

        return scan
    
    def getLastUpdate(self):
        update = ''
        try:
            self.getLock()

            if os.path.exists(f'{self.path}update_info.txt'):
                with open(f'{self.path}update_info.txt', 'r') as file:
                    update = file.readline()
            else:
                update = 'None'
        finally:
            self.unlock()
            
        return update
    
    def checkHashUpdate(self):
        try:
            self.getLock()

            url = 'https://longji-definitions-storage-bucket.s3.eu-west-1.amazonaws.com/definitions/clean.csv'

            if not os.path.exists(f'{self.path}clean.csv'):
                urllib.request.urlretrieve(url, f'{self.path}clean.csv')
        finally:
            self.unlock()

    def getHashSet(self):
        hSet = set()

        try:
            self.getLock()

            with open(f'{self.path}clean.csv', 'r') as file:
                for line in file:
                    hSet.add(line.strip())
        finally:
            self.unlock()
        return hSet