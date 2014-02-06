'''
Created on 31.01.2014

@author: RKlinger
'''
import unittest
from src.persistence.FileReader import FileReader

class TestFileReader(unittest.TestCase):

    def testReadTxtFile(self):
        fileReader = FileReader()
        config = fileReader.readTxtFile('C:\\workspace\\Head\\SoDocu\\sodocu\\0_ideas\\useVCSforRequirements.txt')
        assert 'meta' in config.sections()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()