'''
Created on 31.01.2014

@author: RKlinger
'''
import os
import unittest

from src.model.Idea import Idea, create_idea
from src.persistence.FileHandler import FileHandler, make_camel_case


class TestFileHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.fileHandler = FileHandler(os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir)))
 
 
    @classmethod 
    def tearDownClass(self):
        self.fileHandler = None


    def test_read_file(self):
        config = self.fileHandler.read_file('../../sodocu/0_ideas/useVCSforRequirements.txt')
        assert 'meta' in config.sections()


    def test_write_file(self):
        idea1 = Idea('idea-99', 'this is a file writer test')
        self.fileHandler.write_file(idea1)
        config = self.fileHandler.read_file('../../sodocu/0_ideas/ThisIsAFileWriterTest.txt')
        idea2 = create_idea(config)
        assert idea1.get_id() == idea2.get_id()


    def test_make_camel_case(self):
        text = 'This should be a camel case'
        print make_camel_case(text)
        assert make_camel_case(text) == 'ThisShouldBeACamelCase'
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
