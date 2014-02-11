'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder


class TestIdea(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.idea = Idea(1, 'use Python language')
        self.idea.set_created_by('rklinger')
 
 
    @classmethod 
    def tearDownClass(self):
        self.idea = None


    def test_create_idea(self):
        self.idea.set_created_at('2014-02-03 13:33')
#         self.idea.set_created_now()
        assert self.idea.get_id() == 1
        assert self.idea.get_name() == 'use Python language'
        assert self.idea.get_created_by() == 'rklinger'
        assert self.idea.get_created_at() == '2014-02-03 13:33'


    def test_assert_none_stakeholder(self):
        with self.assertRaises(Exception):
            self.idea.set_invented_by('rklinger')

        
    def test_assert_stakeholder(self):
        tester = Stakeholder(2, 'Tester')
        self.idea.set_invented_by(tester)
        assert self.idea.get_invented_by() == tester
        

    def test_to_string(self):
        print 'self.idea.get_description(): ' + str(self.idea.get_description())
        print 'self.idea.get_invented_by(): ' + str(self.idea.get_invented_by())
        assert self.idea.__str__() == 'Idea {[id=1, name=use Python language][createdBy=rklinger, createdAt=2014-02-03 13:33]}' 


    def test_to_config(self):
        config = self.idea.__config__()
        assert config.has_section('idea')
        assert config.has_option('idea', 'id')
        assert config.has_option('idea', 'name')
        assert config.has_option('idea', 'description')
        assert config.has_option('idea', 'inventedBy')
        
        assert config.has_section('meta')
        assert config.has_option('meta', 'created_by')
        assert config.get('meta', 'created_by') == 'rklinger'
        assert config.has_option('meta', 'created_at')
        assert config.has_option('meta', 'changed_by')
        assert config.has_option('meta', 'changed_at')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()