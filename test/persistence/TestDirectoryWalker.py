'''
Created on 31.01.2014

@author: RKlinger
'''
import unittest

from src.persistence.DirectoryWalker import DirectoryWalker

class TestDirectoryWalker(unittest.TestCase):

    directoryWalker = DirectoryWalker("C:\workspace\Head\SoDocu\sodocu")

#     def setUp(self):
#         pass
# 
#     def tearDown(self):
#         pass

    def testName(self):
        filenames = self.directoryWalker.getFilenames()
        assert len(filenames) > 0

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    