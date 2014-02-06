'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.model.Idea import Idea
from src.model.Stakeholder import Stakeholder


class TestIdea(unittest.TestCase):
    
    def test_create_idea(self):
        idea = Idea(1, 'use Python language')
        idea.set_created_by('rklinger')
#         idea.set_created_at('2014-02-03 13:33')
        idea.set_created_now()
        print idea
        assert idea.get_id() == 1
        assert idea.get_name() == 'use Python language'
        assert idea.get_created_by() == 'rklinger'
#         assert idea.get_created_at() == '2014-02-03 13:33'

    def test_assert_none_stakeholder(self):
        idea = Idea(1, 'use Python language')
        with self.assertRaises(Exception):
            idea.set_invented_by('rklinger')
        
    def test_assert_stakeholder(self):
        idea = Idea(1, 'use Python language')
        tester = Stakeholder(2, 'Tester')
        idea.set_invented_by(tester)
        assert idea.get_invented_by() == tester
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()