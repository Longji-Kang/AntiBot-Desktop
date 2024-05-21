from threading import Lock

import sys
sys.path.append('../AntiBot-Desktop')

from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class ScanUpdateInfo:
    last_update = "-"
    last_scan = "-"

    lock = Lock()

    @staticmethod
    def setLastScan(scan: str):
        try:
            ScanUpdateInfo.lock.acquire()
            ScanUpdateInfo.last_scan = scan
        finally:
            ScanUpdateInfo.lock.release()

    @staticmethod
    def getLastScan(file_inter: DefinitionsFileInterface) -> str:
        last_scan = ''

        try:
            ScanUpdateInfo.lock.acquire()
    
            if ScanUpdateInfo.last_scan == '-':
                last_scan = file_inter.getLastScan()
            else:
                last_scan = ScanUpdateInfo.last_scan
        finally:
            ScanUpdateInfo.lock.release()

        return last_scan
    
    @staticmethod
    def setLastUpdate(update: str):
        try:
            ScanUpdateInfo.lock.acquire()
            ScanUpdateInfo.last_update = update
        finally:
            ScanUpdateInfo.lock.release()

    @staticmethod
    def getLastUpdate(file_inter: DefinitionsFileInterface) -> str:
        last_update = ''
        try:
            ScanUpdateInfo.lock.acquire()
            
            if ScanUpdateInfo.last_scan == '-':
                last_update = file_inter.getLastUpdate()
            else:
                last_update = ScanUpdateInfo.last_update
        finally:
            ScanUpdateInfo.lock.release()
        return last_update