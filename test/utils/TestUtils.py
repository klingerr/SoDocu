'''
Created on 12.02.2014

@author: RKlinger
'''
import unittest
from src.utils.Utils import make_camel_case, get_file_basename

class Test(unittest.TestCase):


    def test_make_camel_case(self):
        text = 'This should be a camel case'
#         print make_camel_case(text)
        assert make_camel_case(text) == 'ThisShouldBeACamelCase'


    def test_get_filename(self):
        path = '../../sodocu/0_ideas/ThisIsAFileWriterTest.txt'
#         print get_file_basename(path)
        assert get_file_basename(path) == 'ThisIsAFileWriterTest'
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()