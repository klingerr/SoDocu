'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.model.MetaData import MetaData

class TestMetaData(unittest.TestCase):


    def testCreatedBy(self):
        metaData = MetaData()
        metaData.set_created_by('rklinger')
        assert metaData.get_created_by() == 'rklinger'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()