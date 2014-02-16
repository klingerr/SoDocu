'''
Created on 04.02.2014

@author: RKlinger
'''

import logging
import os
import urlparse

from jinja2 import Environment, FileSystemLoader
from werkzeug.debug import DebuggedApplication
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
from src.utils.Utils import new_line_to_br, get_max_id
from src.model.Idea import Idea

log = logging.getLogger(__name__)


class Gui(object):
    '''
    Class for web gui following REST style:
    HTTP 
    Method URI                               Action
    GET    http://[hostname]/item/           Retrieve list of items
    GET    http://[hostname]/item/[item_id]  Retrieve a single item
    POST   http://[hostname]/item/           Create a new item
    PUT    http://[hostname]/item/[item_id]  Update an existing item
    DELETE http://[hostname]/item/[item_id]  Delete a item
    
    jEditable for inline editing doesn't support PUT requests directly. It sends
    a POST request with additional attribute "_method=PUT".
    @see: http://www.appelsiini.net/2008/put-support-for-jeditable
    '''

    def __init__(self, sodocu):
        '''
        Initialize jinja template engine and defines URL routings.
        '''
        self.__sodocu = sodocu
        # needed for testing
        self.__endpoint = None
        
        # initialize jinja template engine
        template_path = os.path.join(os.path.dirname(__file__), '../../web/templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        
        # registers the custom filter with Jinja2
        # @see: http://jinja.pocoo.org/docs/api/#custom-filters
        self.jinja_env.filters['new_line_to_br'] = new_line_to_br
        
        # define routing table
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/<item_type>/', endpoint='item_list'),
            Rule('/<item_type>/<item_id>', endpoint='single_item')
        ])


    def dispatch_request(self, request):
        '''
        Dispatcher for incoming URLs which uses the routing table defined in 
        constructor, sets prefix 'on_' to the specified endpoint as called method name.
        '''
        log.debug('dispatch_request(' + str(request) + ')')
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            self.__endpoint = endpoint
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e


    def on_new_url(self, request):
        '''
        This method is called when requesting the base URL, 
        i.e. http://localhost/.
        '''
        log.debug('on_new_url(' + str(request) + ')')
        error = None
        url = ''
        if request.method == 'POST':
            url = request.form['url']
            if not self.is_valid_url(url):
                error = 'Please enter a valid URL'
            else:
                return redirect('/%s+' % 'short_id')
        return self.render_template('new_url.html', error=error, url=url,
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def on_item_list(self, request, item_type):
        '''
        On request type GET retrieves all items of specified type.
        On request type POST creates a new item of specified type.
        '''
        log.debug('on_item_list(request, ' + item_type + ')')
        self.check_valid_item_type(item_type)
        if request.method == 'GET':
            log.debug('request.method: GET')
            return self.render_all_item_as_table(item_type)
        elif request.method == 'POST':
            log.debug('request.method: POST')
            return self.render_new_item_as_form(item_type)


    def on_single_item(self, request, item_type, item_id):
        '''
        On request type GET retrieves details of specified item.
        On request type PUT updates data of specified item.
        On request type DELETE deletes the of specified item.
        '''
        log.debug('on_single_item(request, ' + item_type + ', ' + item_id + ')')
        self.check_valid_item_type(item_type)
        if request.method == 'GET':
            log.debug('request.method: GET')
            # TODO
        elif self.is_put_request(request):
            log.debug('request.method: PUT')
            if self.is_single_attribute_update(request):
                return self.update_single_attribute(request, item_id)
            else:
                return self.update_item(request, item_type, item_id)
        elif request.method == 'DELETE':
            log.debug('request.method: DELETE')
            self.get_sodocu().delete_item(item_type, item_id)
            # JavaScript delete method requires text response "success" for removing table row
            return Response('success', mimetype='text/plain')
        else:
            log.debug('request.method: UNKNOWN')
    
    
    def check_valid_item_type(self, item_type):
        if self.is_valid_item_type(item_type):
            log.warn('Unknown item type: ' + item_type)
            raise NotFound()


    def render_all_item_as_table(self, item_type):
        return self.render_template(item_type + '_table.html', 
                                    items=self.sodocu.get_items(item_type), 
                                    item_type=item_type,
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def render_new_item_as_form(self, item_type):
        new_id = get_max_id(self.sodocu.get_items(item_type)) + 1
        return self.render_template(item_type + '_new.html', 
                                    identifier=item_type + '-' + str(new_id),
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def render_one_item_as_form(self, item_type, item_id):
        return self.render_template(item_type + '_new.html', 
                                    item=self.sodocu.get_item_by_id(item_type, item_id),
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def update_single_attribute(self, request, item_id):
        log.debug('update_single_attribute(' + str(request) + ', ' + item_id + ')')
        log.debug("request.form['id']: " + request.form['id'])
        
        if item_id != request.form['id']:
            raise MethodNotAllowed(description='URL and form data do not match!')
        
        attribute = request.form['attribute']
        log.debug("attribute: " + attribute)
        
        item = self.get_sodocu().get_item_by_id(item_id)
        log.debug("item: " + str(item))
        
        self.get_sodocu().set_attribut(item, attribute, request.form['value'])
        self.get_sodocu().save_item(item)
        
        # jEditable requires submited data as return value for updating table
        # @see: https://www.datatables.net/forums/discussion/8365/jeditable-datatables-how-can-i-refresh-table-after-edit 
        return Response(request.form['value'])
    
    # TODO dynamic item type
    def update_item(self, request, item_type, item_id):
        log.debug('update_item(' + str(request) + ', ' + item_id + ')')
        idea = Idea(item_id, request.form['name'])
        idea.set_description(request.form['description'])
        self.get_sodocu().save_item(idea)
        self.get_sodocu().add_idea(idea)
        return redirect('/%s/' % item_type)


    def is_valid_item_type(self, item_type):
        log.debug('valid item types: ' + str(self.get_sodocu().get_config().get_item_types_as_string()))
        return item_type not in self.get_sodocu().get_config().get_item_types_as_string()
    
    
    def is_put_request(self, request):
        return (request.method == 'PUT') or (request.method == 'POST' and request.form['_method'].upper() == 'PUT')
                      
                      
    def is_single_attribute_update(self, request):
        return 'attribute' in request.form
                            
    
    def is_valid_url(self, url):
        parts = urlparse.urlparse(url)
        return parts.scheme in ('http', 'https')


    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

        
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)


    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

        
    def get_sodocu(self):
        return self.__sodocu


    def get_endpoint(self):
        return self.__endpoint

    sodocu = property(get_sodocu, None, None, None)
    endpoint = property(get_endpoint, None, None, None)


def create_gui(sodocu, with_static=True):
    '''
    Factory method for creating a new instance of Gui. Configuration of static
    content locations is situated here too.
    '''
    gui = Gui(sodocu)
    if with_static:
        gui.wsgi_app = SharedDataMiddleware(gui.wsgi_app, {
            '/js':    os.path.join(os.path.dirname(__file__), '../../web/js'),
            '/css':   os.path.join(os.path.dirname(__file__), '../../web/css'),
            '/img':   os.path.join(os.path.dirname(__file__), '../../web/img'),
            '/fonts': os.path.join(os.path.dirname(__file__), '../../web/fonts')
        })
#     return gui
    # @see: http://werkzeug.pocoo.org/docs/debug/
    return DebuggedApplication(gui, evalex=True)
