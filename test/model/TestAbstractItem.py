'''
Created on 31.01.2014

@author: RKlinger
'''
import unittest
from src.model.AbstractItem import AbstractItem

class TestAbstractItem(unittest.TestCase):


    def testGetContent(self):
        abstractItem = AbstractItem(0, 'bla')
        print abstractItem
        assert abstractItem.get_id() == 0


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()