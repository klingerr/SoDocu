'''
Created on 19.02.2014

@author: RKlinger
'''
import unittest

from src.model.Relations import Relations


class TestRelations(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.relations = Relations()
        self.relations.add_invented_by('stakeholder-1')
 
 
    @classmethod 
    def tearDownClass(self):
        self.relations = None


    def test_get_existing_relations(self):
        self.relations.set_invented_by('stakeholder-1, stakeholder-2')
        self.relations.add_invented_by('stakeholder-3')
        self.relations.add_invented_from('idea-1')
#         print self.relations.get_invented_by()
#         print self.relations.get_existing_relations()
        assert 'stakeholder-1' in str(self.relations.get_existing_relations())


    def test_to_string(self):
#         print self.relations
        assert 'stakeholder-1' in self.relations.__str__() 


    def test_to_config(self):
        config = self.relations.__config__()
        section = Relations.SECTION_NAME
        assert config.has_section(section)
        assert config.has_option(section, 'invented_by')
        print "config.get(section, 'invented_by'): " + str(config.get(section, 'invented_by'))
        assert 'stakeholder-1' in config.get(section, 'invented_by')
        assert not config.has_option(section, 'verified_by')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()