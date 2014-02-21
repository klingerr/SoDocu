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
 
 
    @classmethod 
    def tearDownClass(self):
        self.relations = None


    def test_get_existing_relations(self):
        self.relations.set_invented_by('stakeholder-1, stakeholder-2')
        self.relations.add_invented_by('stakeholder-3')
        self.relations.add_invented_from('idea-1')
        print self.relations.get_invented_by()
        print self.relations.get_existing_relations()
        assert 'stakeholder-1' in str(self.relations.get_existing_relations())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()