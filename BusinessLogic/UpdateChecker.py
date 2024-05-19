import requests
import os
import urllib.request

class UpdateChecker():
    def checkForUpdates(self):
        url = 'https://dqz7x5u9sf.execute-api.eu-west-1.amazonaws.com/longji-deployment-stage/updates'

        # response = requests.get(url)

        # response_url = response.json()['url']
        response_url     = 'https://longji-definitions-storage-bucket.s3.eu-west-1.amazonaws.com/definitions/1716140905-definition.pkl'
        url_split        = response_url.split('/')
        update_file_name = url_split[len(url_split) - 1]

        current_file = None

        for file_name in os.listdir('Definitions'):
            if file_name.endswith('.pkl'):
                current_file = file_name
                break

        if current_file == None:
            urllib.request.urlretrieve(response_url, f'Definitions/{update_file_name}')
        else:
            if current_file.split('-')[0] > update_file_name.split('-')[0]:
                os.remove(f'Definitions/{current_file}')
                urllib.request.urlretrieve(response_url, f'Definitions/{update_file_name}')
            else: 
                # Log same file found