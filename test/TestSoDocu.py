'''
Created on 03.02.2014

@author: RKlinger
'''
import json
import unittest

from mock import patch

from src.SoDocu import SoDocu
from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder
from src.persistence.FileHandler import FileHandler
from src.utils.Config import Config
from src.utils.ItemType import ItemType


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
        item = self.sodocu.get_item_by_id(ItemType('idea', ''), 'idea-1')
#         print item.get_id()
        assert item.get_id() == 'idea-1'
        assert self.sodocu.get_item_by_id(ItemType('idea', ''), 'idea-1000') == None
        assert self.sodocu.get_item_by_id(ItemType('document', ''), 'document-1000') == None
  
    
    @patch.object(FileHandler, 'update_file')
    def test_save_item_success(self, mocked_method):
        mocked_method.return_value = True
        item = self.sodocu.get_item_by_id(ItemType('idea', ''), 'idea-1')
        assert self.sodocu.save_item(item)
            
    
    @patch.object(FileHandler, 'update_file')
    def test_save_item_failure(self, mocked_method):
        mocked_method.return_value = False
        item = self.sodocu.get_item_by_id(ItemType('idea', ''), 'idea-1')
        assert not self.sodocu.save_item(item)
             
     
    @patch.object(FileHandler, 'delete_file')
    def test_delete_item_success(self, mocked_method):
        mocked_method.return_value = True
        assert self.sodocu.delete_item(Idea(ItemType('idea', ''), 'idea-2', 'idea-2'))
     
              
    @patch.object(FileHandler, 'delete_file')
    def test_delete_item_failure(self, mocked_method):
        mocked_method.return_value = False
        assert not self.sodocu.delete_item(Idea(ItemType('idea', ''), 'idea-2', 'idea-2'))
    
    
    def test_add_item(self):
        self.sodocu.get_items_by_type(ItemType('idea', '')).clear()
        idea1 = Idea(ItemType('idea', ''), 'idea-22', 'idea-22')
        self.sodocu.add_item(idea1)
#         print self.sodocu.get_items_by_type('idea')
        assert len(self.sodocu.get_items_by_type(ItemType('idea', ''))) == 1
        idea2 = Idea(ItemType('idea', ''), 'idea-33', 'idea-33')
        self.sodocu.add_item(idea2)
#         print self.sodocu.get_items_by_type('idea')
        assert len(self.sodocu.get_items_by_type(ItemType('idea', ''))) == 2
        idea3 = Idea(ItemType('idea', ''), 'idea-33', 'idea-33')
        self.sodocu.add_item(idea3)
#         print self.sodocu.get_items_by_type('idea')
#         print idea2 == idea3
        assert len(self.sodocu.get_items_by_type(ItemType('idea', ''))) == 2
        self.sodocu.read_all_items(self.sodocu.get_config())
           
            
    def test_remove_item(self):
        self.sodocu.get_items_by_type(ItemType('idea', '')).clear()
        idea = Idea(ItemType('idea', ''), 'idea-66', 'idea-66')
        assert not self.sodocu.remove_item(idea)
        stakeholder = Stakeholder(ItemType('stakeholder', ''), 'stakeholder-66', 'stakeholder-66')
        assert not self.sodocu.remove_item(stakeholder)
        self.sodocu.add_item(idea)
        assert self.sodocu.remove_item(idea)
        self.sodocu.read_all_items(self.sodocu.get_config())
    
             
    def test_set_attribut(self):
        idea = Idea(None, 'idea-44', 'idea-44')
        self.sodocu.set_attribut(idea, 'id', 'idea-55')
#         print item.get_id()
        assert idea.get_id() == 'idea-55'
     
     
    def test_read_glossary_as_json(self):
        assert 'stakeholder' in str(self.sodocu.get_glossary_entries_as_json())
          
      
    def test_get_items_by_type(self):
        item_list = self.sodocu.get_items_by_type(ItemType('idea', ''))
#         print 'item_list: ' + str(item_list)
        assert len(item_list) > 0
      
      
    def test_get_items_by_type_as_json(self):
        item_list_json = self.sodocu.get_items_by_type_name_as_json('idea')
#         print 'item_list_json: ' + str(item_list_json)
        assert len(item_list_json) > 0
      
      
    def test_search(self):
        items = self.sodocu.search('tester')
        assert len(items) > 0
        
    
    def test_get_all_items_as_json(self):
        json_graph = self.sodocu.get_all_items_as_json() 
#         print json_graph
        graph = json.loads(json_graph)
#         print graph
        assert 'idea-1' in str(graph)
        
        
    def test_set_item_counts(self):
        item = self.sodocu.get_item_by_id(ItemType('idea', ''), 'idea-1')
        assert item.get_item_type().get_item_count() > 0
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
