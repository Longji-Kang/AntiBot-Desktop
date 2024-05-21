import hashlib

class HashScanner:
    def __init__(self, hash_set: set):
        self.hash_set = hash_set

    def checkFile(self, file):
        with open(file, 'rb', buffering=0) as f:
            fhash = hashlib.sha256(f).hexdigest()

            if fhash in self.hash_set:
                return True
            else:
                return False