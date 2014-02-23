'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest

from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder
from src.utils.ItemType import ItemType


class TestIdea(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.idea = Idea(ItemType('idea', ''), 'idea-1', 'use Python language')
        self.idea.get_meta_data().set_created_by('rklinger')
        self.idea.get_relations().set_invented_by('stakeholder-1')
 
 
    @classmethod 
    def tearDownClass(self):
        self.idea = None


    def test_create_idea(self):
        self.idea.get_meta_data().set_created_at('2014-02-03 13:33')
#         self.idea.set_created_now()
        assert self.idea.get_id() == 'idea-1'
        assert self.idea.get_name() == 'use Python language'
        assert self.idea.get_meta_data().get_created_by() == 'rklinger'
        assert self.idea.get_meta_data().get_created_at() == '2014-02-03 13:33'


#     def test_assert_none_stakeholder(self):
#         with self.assertRaises(Exception):
#             self.idea.relations.set_invented_by('stakeholder-1')

        
#     def test_assert_stakeholder(self):
#         tester = Stakeholder(ItemType('stakeholder', ''), 'stakeholder-2', 'Tester')
#         self.idea.relations.set_invented_by(tester)
#         assert self.idea.relations.get_invented_by() == tester
        

    def test_to_string(self):
#         print 'self.idea.get_description(): ' + str(self.idea.get_description())
#         print 'self.idea.get_invented_by(): ' + str(self.idea.get_invented_by())
#         print 'self.idea.__str__(): ' + self.idea.__str__()
        assert 'id=idea-1' in self.idea.__str__()


    def test_to_config(self):
        config = self.idea.__config__()
        assert config.has_section('idea')
        assert config.has_option('idea', 'id')
        assert config.has_option('idea', 'name')
        assert config.has_option('idea', 'description')
        
        assert config.has_section('meta')
        assert config.has_option('meta', 'created_by')
        assert config.get('meta', 'created_by') == 'rklinger'
        assert config.has_option('meta', 'created_at')
        assert config.has_option('meta', 'changed_by')
        assert config.has_option('meta', 'changed_at')

        assert config.has_section('relations')
        assert config.has_option('relations', 'invented_by')
#         print "config.get('relations', 'invented_by'): " + config.get('relations', 'invented_by')
        assert 'stakeholder-1' in config.get('relations', 'invented_by')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()