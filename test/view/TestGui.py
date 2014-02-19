'''
Created on 14.02.2014

@author: RKlinger
'''
import unittest
import json

from mock import Mock, patch
from werkzeug.test import EnvironBuilder
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response

from src.SoDocu import SoDocu
from src.model.Idea import Idea
from src.utils.Config import Config
from src.utils.ItemType import ItemType
from src.view.Gui import Gui


# @see: http://werkzeug.pocoo.org/docs/test/
# @see: http://myadventuresincoding.wordpress.com/2011/02/26/python-python-mock-cheat-sheet/
class TestGui(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.sodocu = Mock(SoDocu)
        self.gui = Gui(self.sodocu)


    @classmethod 
    def tearDownClass(self):
        self.gui = None


    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_new_url')        
    def test_dispatch_home_url(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'new_url'
        
        
    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_item_list')        
    def test_dispatch_item_list(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/item/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'item_list'
                
        
    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_single_item')        
    def test_dispatch_single_item(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/item/idea-99/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'single_item'
        
                
    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_user')        
    def test_dispatch_user(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/user/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'user'
        
                
    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_search')        
    def test_dispatch_search(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/search/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'search'
        
                
    @patch('src.view.Gui.Gui.exists_username')        
    @patch('src.view.Gui.Gui.on_search')        
    def test_dispatch_json_glossary(self, mocked_method, mocked_exists_username):
        mocked_method.return_value = None
        mocked_exists_username.return_value = True
        builder = EnvironBuilder(path='/glossary/json/')
        env = builder.get_environ()
        request = Request(env)
#         print 'request: ' + str(request)
        self.gui.dispatch_request(request)
        assert str(self.gui.get_endpoint()) == 'json_glossary'
        
                
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
            
            
    def test_get_sodocu(self):
        assert isinstance(self.gui.get_sodocu(), SoDocu) 
                
        
    def test_update_single_attribute(self):
        idea = Idea('idea-1', 'idea-1')
        self.sodocu.get_item_by_id.return_value = idea
                
        builder = EnvironBuilder(method='POST', data={'id': 'idea-1', 'attribute':'name', 'value':'updated name'})
        env = builder.get_environ()
        request = Request(env)
                
        self.gui.update_single_attribute(request, 'idea', 'idea-1')
#         print idea.get_name()
        # assertion not possible because of mocking SoDocu
#         assert idea.get_name() == 'updated name'
       
       
    def test_update_single_attribute_exception(self):
        idea = Idea('idea-1', 'idea-1')
        self.sodocu.get_item_by_id.return_value = idea
                
        builder = EnvironBuilder(method='POST', data={'id': 'idea-5', 'attribute':'name', 'value':'updated name'})
        env = builder.get_environ()
        request = Request(env)
                
        with self.assertRaises(Exception):
            self.gui.update_single_attribute(request, 'idea', 'idea-1')
       
       
    def test_create_or_update_item_existing(self):
        self.sodocu.save_item.return_value = True
        idea = Idea('idea-1', 'idea-1')
        self.sodocu.get_item_by_id.return_value = idea
               
        builder = EnvironBuilder(method='POST', data={'id': 'idea-1', 'name':'updated name', 'description':'new description', 'bla':'bli'})
        env = builder.get_environ()
        request = Request(env)
                
        self.gui.create_or_update_item(request, 'idea', 'idea-1')
        assert idea.get_name() == 'updated name'
        assert idea.get_description() == 'new description'
      
      
    @patch('src.utils.Utils.create_item')
    def test_create_or_update_item_new(self, mocked_create_item):
#         print str(mocked_create_item)
        idea = Idea('idea-1', 'idea-1')
        mocked_create_item.return_value = idea
               
        self.sodocu.save_item.return_value = True
        self.sodocu.get_item_by_id.return_value = None
               
        builder = EnvironBuilder(method='POST', data={'id': 'idea-1', 'name':'updated name', 'description':'new description', 'bla':'bli'})
        env = builder.get_environ()
        request = Request(env)
                
        self.gui.create_or_update_item(request, 'idea', 'idea-1')
        # assertion not possible because of mocking SoDocu
#         assert idea.get_name() == 'updated name'
#         assert idea.get_description() == 'new description'
      
      
    def test_update_item(self):
        builder = EnvironBuilder(method='POST', data={'id': 'idea-1', 'name':'updated name', 'description':'new description', 'bla':'bli'})
        env = builder.get_environ()
        request = Request(env)
                
        idea = Idea('idea-1', 'idea-1')
        self.gui.update_item(request, idea)
                
        assert idea.get_name() == 'updated name'
        assert idea.get_description() == 'new description'
      
      
    @patch('src.view.Gui.Gui.check_valid_item_type')
    def test_on_single_item_put_attribute(self, mocked_check_valid_item_type):
        mocked_check_valid_item_type.return_value = True
        idea = Idea('idea-1', 'idea-1')
        self.sodocu.get_item_by_id.return_value = idea

        builder = EnvironBuilder(method='POST', data={'_method': 'put', 'id': 'idea-1', 'attribute':'name', 'value':'updated name'})
        env = builder.get_environ()
        request = Request(env)
                
        response = self.gui.on_single_item(request, 'idea', 'idea-1')
#         print str(response)
#         print str(Response('updated name'))
        assert str(response) == str(Response('updated name'))
             
     
    @patch('src.view.Gui.Gui.check_valid_item_type')
    def test_on_single_item_put_item(self, mocked_check_valid_item_type):
        mocked_check_valid_item_type.return_value = True
        builder = EnvironBuilder(method='POST', data={'_method': 'put', 'id': 'idea-1', 'name':'updated name'})
        env = builder.get_environ()
        request = Request(env)
               
        response = self.gui.on_single_item(request, 'idea', 'idea-1')
#         print str(response)
#         print str(redirect('/idea/'))
        assert str(response) == str(redirect('/idea/'))
     
     
    @patch('src.view.Gui.Gui.check_valid_item_type')
    def test_on_single_item_delete(self, mocked_check_valid_item_type):
        mocked_check_valid_item_type.return_value = True
        builder = EnvironBuilder(method='DELETE', data={'id': 'idea-1', 'name':'updated name'})
        env = builder.get_environ()
        request = Request(env)
        
        response = self.gui.on_single_item(request, 'idea', 'idea-1')
#         print str(response)
#         print str(redirect('/idea/'))
        assert str(response) == str(Response('success', mimetype='text/plain'))
    
    
    def test_check_valid_item_type(self):
        mocked_config = Mock(Config)
        mocked_config.get_item_types_as_string.return_value = {'idea'}
        self.sodocu.get_config.return_value = mocked_config
            
        assert self.gui.check_valid_item_type('idea')
            
        with self.assertRaises(Exception):
            self.gui.check_valid_item_type('bla')
    
    
    @patch('src.view.Gui.Gui.render_template')
    @patch('src.view.Gui.Gui.check_valid_item_type')
    def test_on_item_list_get(self, mocked_check_valid_item_type, mocked_render_template):
        mocked_check_valid_item_type.return_value = True
        mocked_render_template.return_value = True
        mocked_config = Mock(Config)
        mocked_config.get_item_types.return_value = {ItemType('idea', './idea')}
        builder = EnvironBuilder(method='GET', path='/idea/')
        env = builder.get_environ()
        request = Request(env)
            
        assert self.gui.on_item_list(request, 'idea')
  

    @patch('src.view.Gui.Gui.check_valid_item_type')
    @patch('src.view.Gui.Gui.render_new_item_as_form')
    def test_on_item_list_post(self, mocked_render_new_item_as_form, mocked_check_valid_item_type):
        mocked_check_valid_item_type.return_value = True
        mocked_render_new_item_as_form.return_value = True
        builder = EnvironBuilder(method='POST', path='/idea/')
        env = builder.get_environ()
        request = Request(env)
         
        assert self.gui.on_item_list(request, 'idea')
 
 
    @patch('src.view.Gui.Gui.render_template')
    def test_on_user_get(self, mocked_render_template):
        mocked_render_template.return_value = True
        builder = EnvironBuilder(method='GET', path='/user/')
        env = builder.get_environ()
        request = Request(env)
              
        assert self.gui.on_user(request)
   
  
    def test_on_user_post(self):
        builder = EnvironBuilder(method='POST', data={'user': 'rklinger'})
        env = builder.get_environ()
        request = Request(env)
              
        response = self.gui.on_user(request)
#         print str(response)
        assert '302' in str(response)
 
 
    def test_exists_username(self):
        builder = EnvironBuilder(method='GET', path='/user/')
        env = builder.get_environ()
        request = Request(env)
#         print self.gui.exists_username(request)
        assert not self.gui.exists_username(request)


    @patch('src.view.Gui.Gui.check_valid_item_type')
    def test_on_json_glossary(self, mocked_check_valid_item_type):
        mocked_check_valid_item_type.return_value = True
        self.sodocu.read_glossary_as_json.return_value = {"stakeholder":"person"}
        
        builder = EnvironBuilder(method='GET', path='/glossary/json/')
        env = builder.get_environ()
        request = Request(env)
        
        print str(self.gui.on_json_glossary(request).data)
        assert 'stakeholder' in str(self.gui.on_json_glossary(request).data) 
  

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
