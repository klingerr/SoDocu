'''
Created on 12.02.2014

@author: RKlinger
'''
from ConfigParser import ConfigParser
import unittest

from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder
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
        ideas = {Idea('idea-42', 'idea-1'), Idea('idea-100', 'idea-1')}
#         print get_max_id(ideas)
        assert get_max_id(ideas) == 100
 
 
    def test_get_max_id_empty_set(self):
        ideas = set()
#         print get_max_id(ideas)
        assert get_max_id(ideas) == 0
 
 
    def test_create_base_item(self):
        idea = create_base_item('idea', 'idea-1', 'idea name')
        print str('idea: ' + str(idea))
        assert isinstance(idea, Idea)
        stakeholder = create_base_item('stakeholder', 'stakeholder-1', 'stakeholder_name')
        print str('stakeholder: ' + str(stakeholder))
        assert isinstance(stakeholder, Stakeholder)
             

    def test_create_item(self):
        config = ConfigParser()
        section_name = 'idea'
        config.add_section(section_name)
        config.set(section_name, 'id', 'idea-1')
        config.set(section_name, 'name', 'my_name')
        config.set(section_name, 'description', 'my_description')
        config.add_section('meta')
        config.set('meta', 'created_by', 'rklinger')
        config.set('meta', 'created_at', '17.2.2014 18:35:22')
        
        item = create_item(config, '/dir/file.txt')
        assert isinstance(item, Idea)
        assert item.get_id() == 'idea-1'
        assert item.createdBy == 'rklinger'
            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()