import unittest
import os
import requests

class ApiIntegration(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.url = 'https://dqz7x5u9sf.execute-api.eu-west-1.amazonaws.com/longji-deployment-stage/updates'

    def removeDefFiles(self):
        for file in os.listdir('Definitions'):
            os.remove(f'Definitions/{file}')

    def testGetRequest200(self):
        print('[ApiIntegrationTest] Testing API endpoint returns 200')
        response = requests.get(self.url)
        
        self.assertEqual(response.status_code, 200)

    def testGetRequestGetsS3(self):
        print('[ApiIntegrationTest] Testing API endpoint returns S3 URL')
        response = requests.get(self.url)
        
        contains = 'https://longji-definitions-storage-bucket.s3.eu-west-1.amazonaws.com/definitions/' in response.json()['url']

        self.assertTrue(contains)

if __name__ == '__main__':
    unittest.main()