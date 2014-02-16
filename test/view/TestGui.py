'''
Created on 14.02.2014

@author: RKlinger
'''
import unittest

from mock import Mock, patch
from werkzeug.test import EnvironBuilder
from werkzeug.wrappers import Request

from src.SoDocu import SoDocu
from src.view.Gui import Gui


# @see: http://werkzeug.pocoo.org/docs/test/
# @see: http://myadventuresincoding.wordpress.com/2011/02/26/python-python-mock-cheat-sheet/
class TestGui(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.sodoku = Mock(SoDocu)
        self.gui = Gui(self.sodoku)


    @classmethod 
    def tearDownClass(self):
        self.gui = None


    @patch('src.view.Gui.Gui.on_new_url')        
    def test_dispatch_home_url(self, mocked_method):
        mocked_method.return_value = None
        builder = EnvironBuilder(path='/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'new_url'


    @patch('src.view.Gui.Gui.on_item_list')        
    def test_dispatch_item_list(self, mocked_method):
        mocked_method.return_value = None
        builder = EnvironBuilder(path='/item/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'item_list'

        

    @patch('src.view.Gui.Gui.on_single_item')        
    def test_dispatch_single_item(self, mocked_method):
        mocked_method.return_value = None
        builder = EnvironBuilder(path='/item/idea-99')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'single_item'

        
    def test_is_put_request_get(self):
        builder = EnvironBuilder(method='GET')
        env = builder.get_environ()
        request = Request(env)
        assert not self.gui.is_put_request(request)
        

    def test_is_put_request_put(self):
        builder = EnvironBuilder(method='PUT')
        env = builder.get_environ()
        request = Request(env)
        assert self.gui.is_put_request(request)
        

    def test_is_put_request_post_method_put(self):
        builder = EnvironBuilder(method='POST', data={'_method': 'put'})
        env = builder.get_environ()
        request = Request(env)
        assert self.gui.is_put_request(request)
        

    def test_is_single_attribute_update_success(self):
        builder = EnvironBuilder(method='POST', data={'attribute': 'bla'})
        env = builder.get_environ()
        request = Request(env)
        assert self.gui.is_single_attribute_update(request)
        

    def test_is_single_attribute_update_failure(self):
        builder = EnvironBuilder(method='POST', data={'bla': 'bla'})
        env = builder.get_environ()
        request = Request(env)
        assert not self.gui.is_single_attribute_update(request)
    
    
    def _test_is_valid_item_type_valid(self):
        assert self.gui.is_valid_item_type('idea')
        

    def _test_is_valid_item_type_invalid(self):
        assert not self.gui.is_valid_item_type('bla')
        

#     def test_fetch_items(self):
#         get_items_method = self.gui.get_get_items_method('idea')
#         print get_items_method
#         assert len(self.gui.fetch_items(get_items_method)) > 0
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()