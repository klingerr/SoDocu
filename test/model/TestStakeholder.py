'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
from src.model.Stakeholder import Stakeholder


class TestStakeholder(unittest.TestCase):

    def test_create_stakeholder(self):
        stakeholder = Stakeholder(1, 'Developer')
        stakeholder.set_created_by('rklinger')
#         stakeholder.set_created_now()
#         print stakeholder
        assert stakeholder.get_id() == 1
        assert stakeholder.get_name() == 'Developer'
        assert stakeholder.get_created_by() == 'rklinger'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()