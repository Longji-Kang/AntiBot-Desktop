class ProcessScanner():
    def __init__(self):
        self.malicious_processes = [
            'AppMarket.exe',
            'PcyybAssistant.exe'
        ]

    def checkProcess(self, proc) -> bool:
        if proc.name() in self.malicious_processes:
            return True
        else:
            return False