import sys
sys.path.append('../AntiBot-Desktop')

from BusinessLogic.ScannerComponents.HashScanner import HashScanner
from FileSystems.DefinitionFilesInterface import DefinitionsFileInterface

class Scanner:
    def __init__(self, definitions: DefinitionsFileInterface):
        self.definitions = definitions

    def scan(self):
        hSet = self.definitions.getHashSet()
        hScanner = HashScanner(hSet)