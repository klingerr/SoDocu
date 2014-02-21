'''
Created on 12.02.2014

@author: RKlinger
'''
from ConfigParser import ConfigParser
import unittest

from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder
from src.utils.Config import Config
from src.utils.ItemType import ItemType
from src.utils.Utils import make_camel_case, get_file_basename, get_max_id, create_base_item,\
    create_item


class Test(unittest.TestCase):


    def test_make_camel_case(self):
        text = 'This should be a camel case'
#         print make_camel_case(text)
        assert make_camel_case(text) == 'ThisShouldBeACamelCase'
  
  
    def test_get_filename(self):
        path = '../../sodocu/0_ideas/ThisIsAFileWriterTest.txt'
#         print get_file_basename(path)
        assert get_file_basename(path) == 'ThisIsAFileWriterTest'
          
      
    def test_get_max_id_filled_set(self):
        ideas = {Idea(ItemType('idea', ''), 'idea-42', 'idea-1'), Idea(ItemType('idea', ''), 'idea-100', 'idea-1')}
#         print get_max_id(ideas)
        assert get_max_id(ideas) == 100
  
  
    def test_get_max_id_empty_set(self):
        ideas = set()
#         print get_max_id(ideas)
        assert get_max_id(ideas) == 0
  
  
    def test_create_base_item(self):
        idea = create_base_item(ItemType('idea', ''), 'idea-1', 'idea name')
#         print str('idea: ' + str(idea))
        assert isinstance(idea, Idea)
        stakeholder = create_base_item(ItemType('stakeholder', ''), 'stakeholder-1', 'stakeholder_name')
#         print str('stakeholder: ' + str(stakeholder))
        assert isinstance(stakeholder, Stakeholder)
             

    def test_create_item(self):
        item_config = ConfigParser()
        section_name = 'idea'
        item_config.add_section(section_name)
        item_config.set(section_name, 'id', 'idea-1')
        item_config.set(section_name, 'name', 'my_name')
        item_config.set(section_name, 'description', 'my_description')
        item_config.add_section('meta')
        item_config.set('meta', 'created_by', 'rklinger')
        item_config.set('meta', 'created_at', '17.2.2014 18:35:22')
        item_config.add_section('relations')
        item_config.set('relations', 'invented_by', 'stakeholder-1')
        
        item = create_item(Config(), item_config, '/dir/file.txt')
        assert isinstance(item, Idea)
        assert item.get_id() == 'idea-1'
        assert item.get_meta_data().get_created_by() == 'rklinger'
        print 'item.get_relations().get_invented_by(): ' + str(item.get_relations().get_invented_by())
        assert 'stakeholder-1' in str(item.get_relations().get_invented_by())
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()