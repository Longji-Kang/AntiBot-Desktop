from threading import Lock

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
    def getLastScan() -> str:
        last_scan = ''

        try:
            ScanUpdateInfo.lock.acquire()
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
    def getLastUpdate() -> str:
        last_update = ''
        try:
            ScanUpdateInfo.lock.acquire()
            last_update = ScanUpdateInfo.last_update
        finally:
            ScanUpdateInfo.lock.release()
        return last_update