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
        self.project_root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))
        self.fileHandler = FileHandler(self.project_root_path)
 
 
    @classmethod 
    def tearDownClass(self):
        self.fileHandler = None


    def test_read_file(self):
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/0_ideas/useVCSforRequirements.txt')
        assert 'meta' in config.sections()


    def test_write_file(self):
        idea1 = Idea('idea-99', 'this is a file writer test')
#        print "hasattr(idea1, 'description'): " + str(hasattr(idea1, 'description'))
#        print "hasattr(idea1, 'inventedBy'): " + str(hasattr(idea1, 'inventedBy'))

#        print 'idea1.get_description(): ' + str(idea1.get_description())
#        print 'idea1.get_invented_by(): ' + str(idea1.get_invented_by())

        self.fileHandler.write_file(idea1)
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/0_ideas/ThisIsAFileWriterTest.txt')
        idea2 = create_idea(config)
        assert idea1.get_id() == idea2.get_id()


    def test_make_camel_case(self):
        text = 'This should be a camel case'
        print make_camel_case(text)
        assert make_camel_case(text) == 'ThisShouldBeACamelCase'
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
