'''
Created on 14.02.2014

@author: RKlinger
'''
import unittest
from src.utils.Config import Config


class Test(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.config = Config()
 
 
    @classmethod 
    def tearDownClass(self):
        self.config = None


    def test_get_sodocu_path(self):
        assert 'sodocu' in self.config.get_sodocu_path()
        

    def test_is_valid_item_type_valid(self):
        assert self.config.is_valid_item_type('idea')
         
 
    def test_is_valid_item_type_invalid(self):
        assert self.config.is_valid_item_type('invalid') == False
         
 
    def test_get_item_type_valid(self):
        assert self.config.get_item_type('idea').get_name() == 'idea'
         
 
    def test_get_item_type_exception(self):
        with self.assertRaises(Exception):
            self.config.get_item_type('invalid')
         
 
    def test_read_config(self):
        self.config.read_config()
        assert self.config.is_valid_item_type('document')
         
 
#     def test_read_config(self):
#         self.config.read_config()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()