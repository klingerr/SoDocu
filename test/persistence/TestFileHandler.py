'''
Created on 31.01.2014

@author: RKlinger
'''
import os
import unittest

from src.model.Idea import Idea
from src.persistence.FileHandler import FileHandler, read_file
from src.utils.Config import Config
from src.utils.ItemType import ItemType
from src.utils.Utils import create_item


class TestFileHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.config = Config()
        self.project_sodocu_path = self.config.get_sodocu_path()
#         print 'sodocu path: ' + self.project_sodocu_path
        self.fileHandler = FileHandler(self.config)
 
 
    @classmethod 
    def tearDownClass(self):
        self.fileHandler = None


    def test_create_directory(self):
        idea = Idea(ItemType('idea', ''), 'idea-99', 'this is a file writer test')
        self.fileHandler.create_directory(idea)
        assert os.path.exists(self.project_sodocu_path + '/idea')
 
 
    def test_create_file(self):
        idea1 = Idea(ItemType('idea', ''), 'idea-99', 'this is a file writer test')
#         print "hasattr(idea1, 'description'): " + str(hasattr(idea1, 'description'))
#         print "hasattr(idea1, 'inventedBy'): " + str(hasattr(idea1, 'inventedBy'))
#         print 'idea1.get_description(): ' + str(idea1.get_description())
#         print 'idea1.get_invented_by(): ' + str(idea1.get_invented_by())
        self.fileHandler.create_file(idea1)
#         print self.project_sodocu_path + '/sodocu/idea/ThisIsAFileWriterTest.txt'
        item_config = read_file(self.project_sodocu_path + '/idea/ThisIsAFileWriterTest.txt')
        idea2 = create_item(self.config, item_config, self.project_sodocu_path + '/idea/ThisIsAFileWriterTest.txt')
        assert idea1.get_id() == idea2.get_id()
 
 
    def test_read_file(self):
#         print self.project_sodocu_path + '/idea/useVCSforRequirements.txt'
        config = read_file(self.project_sodocu_path + '/idea/ThisIsAFileWriterTest.txt')
        assert 'meta' in config.sections()
 
 
    def test_read_file_failure(self):
        with self.assertRaises(ValueError):
            read_file(self.project_sodocu_path + '/idea/ThisFileDoesNotExists.txt')
 
 
    def test_write_file_failure(self):
        idea = Idea(ItemType('idea', ''), 'idea-66', 'idea-66')
        idea.set_filename('/no/directory/idea/Idea-66.txt')
#         with self.assertRaises(IOError):
        assert not self.fileHandler.write_file(idea)
 
 
    def test_update_file_new_item(self):
        idea = Idea(ItemType('idea', ''), 'idea-88', 'idea-88')
        assert self.fileHandler.update_file(idea)
        config = read_file(self.project_sodocu_path + '/idea/Idea-88.txt')
        assert 'idea' in config.sections()
        
        
    def test_update_file_item_non_existing_file(self):
        idea = Idea(ItemType('idea', ''), 'idea-77', 'idea-77')
        idea.relations.add_invented_by('stakeholder-1')
        idea.relations.add_invented_by('stakeholder-2')
        assert self.fileHandler.update_file(idea)
        idea.set_filename(self.project_sodocu_path + '/idea/Idea-66.txt')
        idea.set_name('idea-55')
        assert not self.fileHandler.update_file(idea)
        
        
    def test_update_file_changed_item_name(self):
        item_config = read_file(self.project_sodocu_path + '/idea/ThisIsAFileWriterTest.txt')
        idea1 = create_item(self.config, item_config, self.project_sodocu_path + '/idea/ThisIsAFileWriterTest.txt')
        assert idea1.get_filename is not None
        idea1.set_name('this is a file update test')
        self.fileHandler.update_file(idea1)
        item_config = read_file(self.project_sodocu_path + '/idea/ThisIsAFileUpdateTest.txt')
        idea2 = create_item(self.config, item_config, self.project_sodocu_path + '/idea/ThisIsAFileUpdateTest.txt')
        assert idea1.get_id() == idea2.get_id()
        assert idea1.get_name() == idea2.get_name()
        assert idea1.get_filename() != idea2.get_filename()
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
