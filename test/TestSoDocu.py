'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest

from mock import patch

from src.SoDocu import SoDocu
from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder
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
          
  
    def test_get_item_by_id(self):
        item = self.sodocu.get_item_by_id('idea', 'idea-1')
#         print item.get_id()
        assert item.get_id() == 'idea-1'
        assert self.sodocu.get_item_by_id('idea', 'idea-1000') == None
        assert self.sodocu.get_item_by_id('document', 'document-1000') == None

  
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
 
 
    def test_add_item(self):
        self.sodocu.get_items('idea').clear()
        idea1 = Idea('idea-22', 'idea-22')
        self.sodocu.add_item(idea1)
#         print self.sodocu.get_items('idea')
        assert len(self.sodocu.get_items('idea')) == 1
        idea2 = Idea('idea-33', 'idea-33')
        self.sodocu.add_item(idea2)
#         print self.sodocu.get_items('idea')
        assert len(self.sodocu.get_items('idea')) == 2
        idea3 = Idea('idea-33', 'idea-33')
        self.sodocu.add_item(idea3)
#         print self.sodocu.get_items('idea')
#         print idea2 == idea3
        assert len(self.sodocu.get_items('idea')) == 2
        self.sodocu.read_all_items()
        
         
    def test_remove_item(self):
        self.sodocu.get_items('idea').clear()
        idea = Idea('idea-66', 'idea-66')
        assert not self.sodocu.remove_item(idea)
        stakeholder = Stakeholder('stakeholder-66', 'stakeholder-66')
        assert not self.sodocu.remove_item(stakeholder)
        self.sodocu.add_item(idea)
        assert self.sodocu.remove_item(idea)
        self.sodocu.read_all_items()
 
          
    def test_set_attribut(self):
        idea = Idea('idea-44', 'idea-44')
        self.sodocu.set_attribut(idea, 'id', 'idea-55')
#         print item.get_id()
        assert idea.get_id() == 'idea-55'
  
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()