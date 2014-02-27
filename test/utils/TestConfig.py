'''
Created on 14.02.2014

@author: RKlinger
'''
import os
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
#         print self.config.get_sodocu_path()
        assert 'SoDocu' + os.sep + './sodocu' in self.config.get_sodocu_path()
        

    def test_is_valid_item_type_valid(self):
        assert self.config.is_valid_item_type('idea')
         
 
    def test_is_valid_item_type_invalid(self):
        assert self.config.is_valid_item_type('invalid') == False
         
 
    def test_get_item_type_valid(self):
        assert self.config.get_item_type_by_name('idea').get_name() == 'idea'
         
 
    def test_get_item_type_exception(self):
#         with self.assertRaises(Exception):
#             self.config.get_item_type_by_name('invalid')
        assert self.config.get_item_type_by_name('invalid') == None
         
 
    def test_read_config(self):
        self.config.read_config()
        assert self.config.is_valid_item_type('document')
    
    
    def test_get_item_types_as_string(self):
#         print self.config.get_item_types_as_string()
        assert 'idea' in self.config.get_item_types_as_string()
        
 
    def test_get_item_types(self):
#         print self.config.get_item_types()
        assert 'idea' == self.config.get_item_types()[0].get_name()
        assert 'stakeholder' == self.config.get_item_types()[1].get_name()
        assert 'document' == self.config.get_item_types()[2].get_name()
        assert 'invented_by' in str(self.config.get_item_types()[0].get_valid_relations())
        
 
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()