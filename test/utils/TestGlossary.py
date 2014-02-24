'''
Created on 19.02.2014

@author: RKlinger
'''
import unittest
import json

from src.utils.Config import Config
from src.utils.Glossary import Glossary


class TestGlossary(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        self.sodocu_path = Config().get_sodocu_path()
        self.glossary = Glossary(self.sodocu_path)


    @classmethod 
    def tearDownClass(self):
        self.glossary = None


    def test_read_glossary(self):
        self.glossary.get_entries()
        assert 'person' in self.glossary.get_entries()['stakeholder']


    def test_read_glossary_as_json(self):
        self.glossary.get_entries()
        json_data = self.glossary.get_entries_as_json()
        python_data = json.loads(json_data)
#         print 'json_data: ' + str(json_data) 
#         print 'python_data: ' + str(python_data) 
#         print 'python_data[0][u\'term\']: ' + str(python_data[0][u'term'])
        assert 'acceptence' in str(python_data[0][u'term'])
        assert 'verifies' in str(python_data[0][u'description'])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()