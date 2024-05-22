import os
import time
import psutil
from datetime import datetime

import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.ScannerComponents.HashScanner import HashScanner
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface
from BusinessLogic.ConfigState import ConfigurationState
from BusinessLogic.StateEnums import Modes, DeleteNoDelete, OnOff
from BusinessLogic.LoggingComponent import LoggingComponentClass
from BusinessLogic.ScanUpdateInfo import ScanUpdateInfo
from BusinessLogic.ScannerComponents.AiScanner import AiScanner
from BusinessLogic.ScannerComponents.ProcessScanner import ProcessScanner

class Scanner:
    subsystem = 'Scanner'
    def __init__(self, definitions: DefinitionsFileInterface, logger: LoggingComponentClass):
        self.definitions = definitions
        self.logger = logger
        self.count = 0

    def scan(self, dir: str = 'D:\\University\\COS 730\\COS730-Assignment2\\MockDrive'):
        if ConfigurationState.getOnOff() == OnOff.ON:
            date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
            ScanUpdateInfo.setLastScan(date)
            self.definitions.writeLastScan(date)
            
            h_set = self.definitions.getHashSet()
            h_scanner = HashScanner(h_set)
            ai_scanner = AiScanner(self.definitions.getCurrentFile())
            p_scan = ProcessScanner()

            self.walkProcesses(p_scan)

            start_epoch = int(time.time())
            
            self.logger.log('Starting scan...', Scanner.subsystem)

            self.walk(dir, h_scanner, ai_scanner)
            end_epoch = int(time.time())

            self.logger.log(f'Scanned {self.count} files in {end_epoch - start_epoch} seconds', Scanner.subsystem)

            self.count = 0
        else:
            self.logger.log('Scan turned off - skipping scan', Scanner.subsystem)

    def action(self, file):
        if ConfigurationState.getMode() == Modes.BASIC:
            os.remove(file)
            self.logger.log(f'Found malicious file: {file} - Deleted', Scanner.subsystem)
        else:
            if ConfigurationState.getDelete == DeleteNoDelete.DELETE:
                self.logger.log(f'Found malicious file: {file} - Deleted', Scanner.subsystem)
                os.remove(file)
            else:
                self.logger.log(f'Found malicious file: {file} - Not deleted due to user choice', Scanner.subsystem)
            

    def walk(self, dir, h_scan: HashScanner, ai_scanner: AiScanner):
        sub_folders = []

        for curr in os.scandir(dir):
            if curr.is_dir():
                if not 'System Volume Information' in curr.path:
                    sub_folders.append(curr.path)
            elif curr.is_file():
                self.count = self.count + 1

                malicious = h_scan.checkFile(curr.path)

                if malicious == True:
                    self.action(f'{curr.path}')
                elif curr.name.endswith('.exe'):
                    res = ai_scanner.aiScan(curr.path) 
                    if res == 0:
                        self.action(curr.path)

        for curr in sub_folders:
            sub_fold = self.walk(curr, h_scan, ai_scanner)
            sub_folders.extend(sub_fold)

        return sub_folders
        
    def walkProcesses(self, p_scan = ProcessScanner):
        processes = psutil.process_iter()

        for proc in processes:
            self.count = self.count + 1
            if p_scan.checkProcess(proc) == True:
                if ConfigurationState.getMode() == Modes.BASIC:
                    self.logger.log(f'Found malicious process: {proc.name()} - Terminated', Scanner.subsystem)
                else:
                    if ConfigurationState.getDelete == DeleteNoDelete.DELETE:
                        self.logger.log(f'Found malicious process: {proc.name()} - Terminated', Scanner.subsystem)
                    else:
                        self.logger.log(f'Found malicious process: {proc.name()} - Not terminated due to user choice', Scanner.subsystem)

        self.logger.log(f'Scanned {self.count} processes', Scanner.subsystem)
        self.count = 0