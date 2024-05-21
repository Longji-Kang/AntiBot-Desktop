import sys
from datetime import datetime
import requests

sys.path.append('../AntiBot-Desktop')

from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface
from BusinessLogic.LoggingComponent import LoggingComponentClass
from BusinessLogic.ScanUpdateInfo import ScanUpdateInfo

class UpdateChecker():
    SUBSYSTEM = 'Updates'

    def __init__(self, logging: LoggingComponentClass, definitons: DefinitionsFileInterface):
        self.definition_interface = definitons
        self.logging = logging

    def checkForUpdates(self):
        url = 'https://dqz7x5u9sf.execute-api.eu-west-1.amazonaws.com/longji-deployment-stage/updates'

        response = requests.get(url)

        response_url = response.json()['url']
        self.logging.log("Checking for updates...", self.SUBSYSTEM)

        current_file = self.definition_interface.getCurrentFile()
        current_version = self.definition_interface.getCurrentVersion(current_file)

        self.definition_interface.checkHashUpdate()

        if current_version == None:
            self.logging.log("No definitions found, downloading...", self.SUBSYSTEM)
            self.definition_interface.downloadFile(response_url)
            self.logging.log(f"Definition downloaded!", self.SUBSYSTEM)
            self.updateInfo()
        else:
            self.logging.log("Checking for new definition...", self.SUBSYSTEM)
            updated = self.definition_interface.updateFile(response_url, current_version, current_file)

            print(updated)

            if updated == True:
                self.logging.log("New definition found and was downloaded! New version - " + self.definition_interface.getCurrentVersion(self.definition_interface.getCurrentFile()), self.SUBSYSTEM)
            else:
                self.logging.log("Definiton file up to date - nothing was downloaded!", self.SUBSYSTEM)
                self.updateInfo()

    def updateInfo(self):
        date = datetime.today().strftime('%d/%m/%Y %H:%M:%S')
        ScanUpdateInfo.setLastUpdate(date)
        self.definition_interface.writeLastUpdate(date)