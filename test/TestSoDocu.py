'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.SoDocu import SoDocu

class TestSoDocu(unittest.TestCase):

    def test_read_ideas(self):
        soDocu = SoDocu("C:\workspace\Head\SoDocu\sodocu")
        soDocu.read_all_items()
        for idea in soDocu.get_ideas(): 
            print idea 
        assert len(soDocu.get_ideas()) == 2

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()