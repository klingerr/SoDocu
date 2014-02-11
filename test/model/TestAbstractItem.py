'''
Created on 31.01.2014

@author: RKlinger
'''
import unittest
from src.model.AbstractItem import AbstractItem

class TestAbstractItem(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.abstractItem = AbstractItem(0, 'bla')
 
 
    @classmethod 
    def tearDownClass(self):
        self.abstractItem = None


    def test_get_id(self):
        assert self.abstractItem.get_id() == 0


    def test_get_name(self):
        assert self.abstractItem.get_name() == 'bla'


    def test_to_string(self):
        print self.abstractItem
        assert self.abstractItem.__str__() == '[id=0, name=bla]' 


    def test_to_config(self):
        config = self.abstractItem.__config__()
        section = "AbstractItem".lower()
        assert config.has_section(section)
        assert config.has_option(section, 'id')
        assert config.has_option(section, 'name')
        assert config.has_option(section, 'description')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()