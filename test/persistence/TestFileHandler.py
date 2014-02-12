'''
Created on 31.01.2014

@author: RKlinger
'''
import os
import unittest

from src.model.Idea import Idea, create_idea
from src.persistence.FileHandler import FileHandler


class TestFileHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.project_root_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))
        self.fileHandler = FileHandler(self.project_root_path)
 
 
    @classmethod 
    def tearDownClass(self):
        self.fileHandler = None


    def test_read_file(self):
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/idea/useVCSforRequirements.txt')
        assert 'meta' in config.sections()


    def test_create_file(self):
        idea1 = Idea('idea-99', 'this is a file writer test')
#        print "hasattr(idea1, 'description'): " + str(hasattr(idea1, 'description'))
#        print "hasattr(idea1, 'inventedBy'): " + str(hasattr(idea1, 'inventedBy'))

#        print 'idea1.get_description(): ' + str(idea1.get_description())
#        print 'idea1.get_invented_by(): ' + str(idea1.get_invented_by())

        self.fileHandler.create_file(idea1)
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/idea/ThisIsAFileWriterTest.txt')
        idea2 = create_idea(config)
        assert idea1.get_id() == idea2.get_id()


    def test_update_file(self):
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/idea/ThisIsAFileWriterTest.txt')
        idea1 = create_idea(config)
        idea1.set_filename(self.project_root_path + '/sodocu/idea/ThisIsAFileWriterTest.txt')
        assert idea1.get_filename is not None
        idea1.set_name('this is a file update test')
        self.fileHandler.update_file(idea1)
        config = self.fileHandler.read_file(self.project_root_path + '/sodocu/idea/ThisIsAFileUpdateTest.txt')
        idea1.set_filename(self.project_root_path + '/sodocu/0_ideas/ThisIsAFileUpdateTest.txt')
        idea2 = create_idea(config)
        assert idea1.get_id() == idea2.get_id()
        assert idea1.get_name() == idea2.get_name()
        assert idea1.get_filename() != idea2.get_filename()
        
        
    def test_create_directory(self):
        idea = Idea('idea-99', 'this is a file writer test')
        self.fileHandler.create_directory(idea)
        assert os.path.exists(self.project_root_path + '/sodocu/idea')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
