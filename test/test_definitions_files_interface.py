import unittest
import os


import sys
sys.path.append('../AntiBot-Desktop')

from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class DefinitionsTest(unittest.TestCase):
    def __init__(self, methodName: str = "DefinitionTests") -> None:
        super().__init__(methodName)

        self.url = 'https://longji-definitions-storage-bucket.s3.eu-west-1.amazonaws.com/definitions/1716298960-definition.pkl'

        try:
            os.mkdir('Definitions')
        except:
            print('Dir already exists')

    def removeDefFiles(self):
        for file in os.listdir('Definitions'):
            os.remove(f'Definitions/{file}')


    def test_update_no_definitions(self):
        print('[DefinitionFilesInterface] Testing no definition file update')

        self.removeDefFiles()

        def_inter = DefinitionsFileInterface()

        def_inter.downloadFile(self.url)

        self.assertTrue('1716298960-definition.pkl' in os.listdir('Definitions'))

    def test_update_exising_definitions(self):
        print('[DefinitionFilesInterface] Testing existing definition file update')

        self.removeDefFiles()

        file = 'Definitions/1_definition.pkl'

        with open(file, 'w'):
            print('Create temp file')

        def_inter = DefinitionsFileInterface()

        def_inter.updateFile(self.url, '1', '1_definition.pkl')

        self.assertTrue('1716298960-definition.pkl' in os.listdir('Definitions'))

    def test_get_current(self):
        print('[DefinitionFilesInterface] Testing get current file name')
        def_inter = DefinitionsFileInterface()

        self.removeDefFiles()

        file = 'Definitions/1_definition.pkl'

        with open(file, 'w'):
            print('Create temp file')

        curr = def_inter.getCurrentFile()

        self.assertEqual(curr, '1_definition.pkl')

    def test_current_version(self):
        print('[DefinitionFilesInterface] Testing get current version from string')
        def_inter = DefinitionsFileInterface()

        file = '1-definition.pkl'

        curr = def_inter.getCurrentVersion(file)

        self.assertEqual(curr, '1')

    def test_write_update(self):
        print('[DefinitionFilesInterface] Testing write update info')
        def_inter = DefinitionsFileInterface()
        date = '01/01/2024'
        def_inter.writeLastUpdate(date)
        curr = ''
        
        with open('Definitions/update_info.txt', 'r') as f:
            curr = f.readline()

        self.assertEqual(curr, date)

        self.removeDefFiles()

    def test_read_update(self):
        print('[DefinitionFilesInterface] Testing get update info')
        def_inter = DefinitionsFileInterface()
        date = '01/01/2024'
        
        with open('Definitions/update_info.txt', 'w') as f:
            f.write(date)

        curr = def_inter.getLastUpdate()

        self.assertEqual(curr, date)
        self.removeDefFiles()

    def test_write_scan(self):
        print('[DefinitionFilesInterface] Testing write scan info')
        def_inter = DefinitionsFileInterface()
        date = '01/01/2024'

        def_inter.writeLastScan(date)

        with open('Definitions/scan_info.txt', 'r') as f:
            curr = f.readline()

        self.assertEqual(curr, date)

        self.removeDefFiles()

    def test_read_scan(self):
        print('[DefinitionFilesInterface] Testing read scan info')
        def_inter = DefinitionsFileInterface()
        date = '01/01/2024'
        
        with open('Definitions/scan_info.txt', 'w') as f:
            f.write(date)

        curr = def_inter.getLastScan()

        self.assertEqual(curr, date)
        self.removeDefFiles()

    def test_hash_update(self):
        print('[DefinitionFilesInterface] Testing hash update')
        def_inter = DefinitionsFileInterface()

        def_inter.checkHashUpdate()

        features = 'features.pkl' in os.listdir('Definitions/')
        hashf    = 'clean.csv' in os.listdir('Definitions/')

        self.assertTrue(features and hashf)

        self.removeDefFiles()

    def test_hash_value_with_white_space(self):
        print('[DefinitionFilesInterface] Testing hash value')
        def_inter = DefinitionsFileInterface()

        line_1 = 'a b c'
        line_2 = 'd e f'

        with open('Definitions/clean.csv', 'w') as f:
            f.write(f'{line_1}\n')
            f.write(f'{line_2}\n')

        hSet = def_inter.getHashSet()

        l1_in = line_1.strip() in hSet
        l2_in = line_2.strip() in hSet

        self.assertTrue(l1_in and l2_in)

if __name__ == '__main__':
    unittest.main()