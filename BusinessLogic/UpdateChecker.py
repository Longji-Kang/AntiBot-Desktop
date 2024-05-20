import requests
import os
import urllib.request
import sys

sys.path.append('../AntiBot-Desktop')

from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class UpdateChecker():
    def __init__(self):
        self.definition_interface = DefinitionsFileInterface()

    def checkForUpdates(self):
        url = 'https://dqz7x5u9sf.execute-api.eu-west-1.amazonaws.com/longji-deployment-stage/updates'

        # response = requests.get(url)

        # response_url = response.json()['url']
        response_url     = 'https://longji-definitions-storage-bucket.s3.eu-west-1.amazonaws.com/definitions/1716140905-definition.pkl'

        current_file = self.definition_interface.getCurrentFile()
        current_version = self.definition_interface.getCurrentVersion(current_file)

        if current_version == None:
            self.definition_interface.downloadFile(response_url)
        else:
            updated = self.definition_interface.updateFile(response_url, current_version, current_file)
            print(updated)