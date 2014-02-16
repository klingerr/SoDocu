'''
Created on 03.02.2014

@author: RKlinger
'''
from mock import patch
import unittest

from src.SoDocu import SoDocu
from src.model.Idea import Idea
from src.persistence.FileHandler import FileHandler
from src.utils.Config import Config


class TestSoDocu(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        config = Config()
        self.sodocu = SoDocu(config)
 
 
    @classmethod 
    def tearDownClass(self):
        self.sodocu = None


    def test_get_config(self):
        assert isinstance(self.sodocu.get_config(), Config)
        

    def test_get_fileHandler(self):
        assert isinstance(self.sodocu.get_file_handler(), FileHandler)
        

    def test_read_ideas(self):
        for idea in self.sodocu.get_ideas(): 
            print idea.get_filename()
        print len(self.sodocu.get_ideas())
        assert len(self.sodocu.get_ideas()) > 0


    def test_get_item_by_id(self):
        item = self.sodocu.get_item_by_id('idea', 'idea-1')
        print item.get_id()
        assert item.get_id() == 'idea-1'


    @patch.object(FileHandler, 'update_file')
    def test_save_item_success(self, mocked_method):
        mocked_method.return_value = True
        item = self.sodocu.get_item_by_id('idea', 'idea-1')
        assert self.sodocu.save_item(item)
        

    @patch.object(FileHandler, 'update_file')
    def test_save_item_failure(self, mocked_method):
        mocked_method.return_value = False
        item = self.sodocu.get_item_by_id('idea', 'idea-1')
        assert not self.sodocu.save_item(item)
        

    @patch.object(FileHandler, 'delete_file')
    def test_delete_item_success(self, mocked_method):
        mocked_method.return_value = True
        assert self.sodocu.delete_item('idea', 'idea-2')

         
    @patch.object(FileHandler, 'delete_file')
    def test_delete_item_failure(self, mocked_method):
        mocked_method.return_value = False
        assert not self.sodocu.delete_item('idea', 'idea-2')

         
    def test_remove_item_failure(self):
        idea = Idea('idea-2222', 'idea-2222')
        assert not self.sodocu.remove_item(idea)

         
    def test_set_attribut(self):
        item = self.sodocu.get_item_by_id('idea', 'idea-1')
        self.sodocu.set_attribut(item, 'id', 'idea-5')
#         print item.get_id()
        assert item.get_id() == 'idea-5'


    def test_get_get_items_method_get_ideas(self):
        get_items_method = self.sodocu.get_get_items_method('idea')
#         print get_items_method
        assert get_items_method == self.sodocu.get_ideas
        

    def test_get_get_items_method_exception(self):
        assert self.sodocu.get_get_items_method('unknown') is None


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()