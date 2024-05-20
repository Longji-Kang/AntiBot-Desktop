import os
import urllib.request

class DefinitionsFileInterface:
    path = 'Definitions/'

    def getCurrentFile(self):
        current = None

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        for file_name in os.listdir('Definitions'):
            if file_name.endswith('.pkl'):
                current = file_name
                break

        return current

    def getCurrentVersion(self, current_file: str):
        if current_file == None:
            return None
        else: 
            current_version = current_file.split('-')[0]
            return current_version
    
    def downloadFile(self, url: str):
        url_split        = url.split('/')
        update_file_name = url_split[len(url_split) - 1]
        urllib.request.urlretrieve(url, f'Definitions/{update_file_name}')

    def updateFile(self, url: str, current_version: str, current_file: str = None):
        url_split        = url.split('/')
        update_file_name = url_split[len(url_split) - 1]

        if current_version < update_file_name.split('-')[0]:
            os.remove(f'Definitions/{current_file}')
            urllib.request.urlretrieve(url, f'Definitions/{update_file_name}')
            return True
        else:
            return False