'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.SoDocu import SoDocu

class TestSoDocu(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.sodocu = SoDocu("../sodocu")
 
 
    @classmethod 
    def tearDownClass(self):
        self.sodocu.__ideas = None
        self.sodocu = None


    def test_read_ideas(self):
#         for idea in sodocu.get_ideas(): 
#             print idea 
        print len(self.sodocu.get_ideas())
        assert len(self.sodocu.get_ideas()) == 2


    def test_get_item_by_idea(self):
        item = self.sodocu.get_item_by_id('idea-1')
#         print item.get_id()
        assert item.get_id() == 'idea-1'


    def test_set_attribut(self):
        item = self.sodocu.get_item_by_id('idea-1')
        self.sodocu.set_attribut(item, 'id', 'idea-5')
#         print item.get_id()
        assert item.get_id() == 'idea-5'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()