'''
Created on 03.02.2014

@author: RKlinger
'''
import unittest
import ConfigParser
from src.model.MetaData import MetaData, merge_meta_config

class TestMetaData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.metaData = MetaData()
        self.metaData.set_created_by('rklinger')
 
 
    @classmethod 
    def tearDownClass(self):
        self.metaData = None


    def test_created_by(self):
        assert self.metaData.get_created_by() == 'rklinger'


    def test_to_string(self):
        assert self.metaData.__str__() == '[createdBy=rklinger, createdAt=None]' 


    def test_to_config(self):
        config = self.metaData.__config__()
        section = 'meta'
        assert config.has_section(section)
        assert config.has_option(section, 'created_by')
        assert config.get(section, 'created_by') == 'rklinger'
        assert config.has_option(section, 'created_at')
        assert config.has_option(section, 'changed_by')
        assert config.has_option(section, 'changed_at')


    def test_merge_meta_config(self):
        meta_config = self.metaData.__config__()
        test_config = ConfigParser.ConfigParser()
        test_config.add_section('test')
        test_config.set('test', 'option', 'value')
        merged_config = merge_meta_config(meta_config, test_config)
        assert merged_config.has_section('meta')
        assert merged_config.has_option('meta', 'created_by')
        assert merged_config.get('meta', 'created_by') == 'rklinger'
        assert merged_config.has_section('test')
        assert merged_config.has_option('test', 'option')
        assert merged_config.get('test', 'option') == 'value'
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()