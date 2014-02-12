'''
Created on 31.01.2014

@author: RKlinger
'''

import os
import unittest

from src.persistence.DirectoryWalker import DirectoryWalker

class TestDirectoryWalker(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.project_root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))
        self.directoryWalker = DirectoryWalker(self.project_root_path + '/sodocu')
 
 
    @classmethod 
    def tearDownClass(self):
        self.fileHandler = None


    def test_get_filenames(self):
        filenames = self.directoryWalker.get_filenames()
#         print filenames
        assert len(filenames) > 0


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    