'''
Created on 04.02.2014

@author: RKlinger
'''

import logging
import os

from jinja2 import Environment, FileSystemLoader
from werkzeug.debug import DebuggedApplication
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.routing import Map, Rule
from werkzeug.utils import redirect
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware

from src.utils.ItemType import ItemType
from src.utils.Utils import new_line_to_br, get_max_id, create_base_item, \
                            get_getter_method, get_setter_method, get_adder_method


log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class Gui(object):
    COOKIE_NAME = 'sudocu_user'
    COOKIE_MAX_AGE = 365 * 24 * 60 * 60 # 1 year
    
    '''
    Class for web gui following REST style:
    HTTP 
    Method URI                                         Action
    GET    http://[hostname]/item_type_name/           Retrieve list of items
    GET    http://[hostname]/item_type_name/[item_id]  Retrieve a single item
    POST   http://[hostname]/item_type_name/           Create a new item
    PUT    http://[hostname]/item_type_name/[item_id]  Update an existing item
    DELETE http://[hostname]/item_type_name/[item_id]  Delete a item
    
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
        self.__user = None
        
        # initialize jinja template engine
        template_path = os.path.join(os.path.dirname(__file__), '../../web/templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        
        # registers the custom filter with Jinja2
        # @see: http://jinja.pocoo.org/docs/api/#custom-filters
        self.jinja_env.filters['new_line_to_br'] = new_line_to_br
        
        # define routing table
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/<item_type_name>/', endpoint='item_list'),
            Rule('/<item_type_name>/<item_id>/', endpoint='single_item'),
            # special URL for getting item types as JSON data for jquery autocomplete
            Rule('/<item_type_name>/json/', endpoint='item_list_json'),
            # special URL for getting all items as JSON data for D3js data vizualization
            Rule('/d3js/json/', endpoint='d3js_json'),
            # special URL for entering or changing current username
            Rule('/user/', endpoint='user'),
            # special URL for searching over all items
            Rule('/search/', endpoint='search'),
            # special URL for getting glossary entries as json data
            Rule('/glossary/json/', endpoint='glossary_json'),
            # special URL for getting glossary entries for editing in frontend
            Rule('/glossary/', endpoint='glossary'),
            Rule('/glossary/<term>/', endpoint='glossary_term')
        ])


    def dispatch_request(self, request):
        '''
        Dispatcher for incoming URLs which uses the routing table defined in 
        constructor, sets prefix 'on_' to the specified endpoint as called method name.
        '''
        log.debug('dispatch_request(' + str(request) + ')')
        if not self.exists_username(request) and request.path != '/user/':
            return redirect('/user/')
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
        return self.render_template('new_url.html', 
                                    error=error, 
                                    url='http://localhost',
                                    user=self.get_user(),
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def on_item_list(self, request, item_type_name):
        '''
        On request type GET retrieves all items of specified type.
        On request type POST creates a new item of specified type.
        '''
        log.debug('on_item_list(' + str(request) + ', ' + item_type_name + ')')
        self.check_valid_item_type(item_type_name)
        if request.method == 'GET':
            log.debug('request.method: GET')
            item_type = self.get_sodocu().get_config().get_item_type_by_name(item_type_name)
            template = item_type.get_table_template()
            items = self.sodocu.get_items_by_type(item_type)
            return self.render_all_item_as_table(template, item_type_name, items)
        elif request.method == 'POST':
            log.debug('request.method: POST')
            return self.render_new_item_as_form(item_type_name)


    def on_single_item(self, request, item_type_name, item_id):
        '''
        On request type GET retrieves details of specified item.
        On request type PUT updates data of specified item.
        On request type DELETE deletes the of specified item.
        '''
        log.debug('on_single_item(' + str(request) + ', ' + item_type_name + ', ' + item_id + ')')
        self.check_valid_item_type(item_type_name)
        item_type = self.get_sodocu().get_config().get_item_type_by_name(item_type_name)
        
        if request.method == 'GET':
            log.debug('request.method: GET')
            item = self.sodocu.get_item_by_id(item_type, item_id)
            return self.render_one_item_as_form(item)
        elif self.is_put_request(request):
            log.debug('request.method: PUT')
            if self.is_single_attribute_update(request):
                return self.update_single_attribute(request, item_type_name, item_id)
            else:
                return self.create_or_update_item(request, item_type_name, item_id)
        elif request.method == 'DELETE':
            log.debug('request.method: DELETE')
            self.get_sodocu().delete_item(item_type_name, item_id)
            # JavaScript delete method requires text response "success" for removing table row
            return Response('success', mimetype='text/plain')
        else:
            log.warn('request.method: UNKNOWN')
            raise NotFound('request.method: UNKNOWN')
    
    
    def on_user(self, request):
        '''
        On request type GET retrieves current username from cookie.
        On request type POST saves given username as cookie.
        '''
        log.debug('on_user(' + str(request) + ')')
        if request.method == 'GET':
            log.debug('request.method: GET')
            return self.render_template('user_form.html', 
                                        user=self.get_user(),
                                        valid_item_types=self.get_sodocu().get_config().get_item_types())
        elif request.method == 'POST':
            log.debug('request.method: POST')
            self.set_user(request.form['user'])
            response = redirect('/')  
            response.set_cookie(Gui.COOKIE_NAME, self.get_user(), Gui.COOKIE_MAX_AGE)
            return response  
    
    
    def on_search(self, request):
        log.debug('on_search(' + str(request) + ')')
        if request.method == 'POST':
            log.debug('request.method: POST')
            search_results = self.sodocu.search(request.form['search_string'])
            return self.render_all_item_as_table('generic_table.html', 'search result', search_results)
      
    
    def on_glossary_json(self, request):
        log.debug('on_glossary_json(' + str(request) + ')')
        if request.method == 'GET':
            return Response(self.sodocu.get_glossary_entries_as_json(), mimetype='application/json')
    
    
    def on_item_list_json(self, request, item_type_name):
        log.debug('on_item_list_json(' + str(request) + ', ' + item_type_name + ')')
        if request.method == 'GET':
            return Response(self.sodocu.get_items_by_type_name_as_json(item_type_name), mimetype='application/json')
    
    
    def on_d3js_json(self, request):
        log.debug('on_d3js_json(' + str(request) + ')')
        if request.method == 'GET':
            return Response(self.sodocu.get_all_items_as_json(), mimetype='application/json')
    
    
    def on_glossary(self, request):
        '''
        On request type GET retrieves all terms of glossary.
        On request type POST creates a new term for glossary.
        '''
        log.debug('on_glossary(' + str(request) + ')')
        if request.method == 'GET':
            return self.render_template('glossary_table.html', 
                                glossary=self.get_sodocu().get_glossary_entries(),
                                item_type='glossary',
                                user=self.get_user(),
                                valid_item_types=self.get_sodocu().get_config().get_item_types())
        elif request.method == 'POST':
            log.debug('request.method: POST')
            return self.render_template('glossary_form.html', 
                                        item_type='glossary',
                                        user=self.get_user(),
                                        valid_item_types=self.get_sodocu().get_config().get_item_types())


    def on_glossary_term(self, request, term):
        '''
        On request type PUT updates data of specified term.
        On request type DELETE deletes the specified term.
        '''
        log.debug('on_glossary_term(' + str(request) + ', ' + term +')')
        glossary = self.sodocu.get_glossary_entries()
        if self.is_put_request(request):
            log.debug('request.method: PUT')
            if self.is_single_attribute_update(request):
                self.update_single_glossary_term(request, glossary)
                return Response(request.form['value'])
            else:
                glossary[request.form['term']] = request.form['description'] 
                # write and re-read changed config file
                self.sodocu.glossary.update_glossary()
                return redirect('/glossary/')    
        elif request.method == 'DELETE':
            log.debug('request.method: DELETE')
            glossary.pop(term, None)
            # write and re-read changed config file
            self.sodocu.glossary.update_glossary()
            # JavaScript delete method requires text response "success" for removing table row
            return Response('success', mimetype='text/plain')
        else:
            log.warn('request.method: UNKNOWN')
            raise NotFound('request.method: UNKNOWN')


    def update_single_glossary_term(self, request, glossary):
        # update term or description
        if request.form['attribute'] == 'term':
            glossary[request.form['value']] = glossary.pop(request.form['id'])
        elif request.form['attribute'] == 'description':
            glossary[request.form['id']] = request.form['value']
        # write and re-read changed config file
        self.sodocu.glossary.update_glossary()


    def exists_username(self, request):
        '''
        Reads browser coockie for saved username.
        '''
        log.debug('exists_username(' + str(request) + ')')
        # @see: http://runnable.com/UqbOjvh9mtpcAACn/using-session-in-werkzeug-for-python
        username = request.cookies.get(Gui.COOKIE_NAME)
        log.debug('username: ' + str(username))
        if username is None:
            return False
        self.set_user(username)
        return True
    
    
    def check_valid_item_type(self, item_type_name):
        if not self.is_valid_item_type(item_type_name):
            log.warn('Unknown item type: ' + item_type_name)
            raise NotFound('Unknown item type: ' + item_type_name)
        return True


    def render_all_item_as_table(self, template, item_type_name, items):
        return self.render_template(template, 
                                    item_type=item_type_name,
                                    items=items, 
                                    user=self.get_user(),
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def render_new_item_as_form(self, item_type_name):
        item_type = self.get_sodocu().get_config().get_item_type_by_name(item_type_name)
        new_id = item_type_name + '-' + str(get_max_id(self.sodocu.get_items_by_type(item_type)) + 1)
        temp_item = create_base_item(item_type, new_id, '')
        return self.render_one_item_as_form(temp_item)


    def render_one_item_as_form(self, item):
        log.debug('render_one_item_as_form(' + str(item) + ')')
        item_type = item.get_item_type()
        relations = self.sodocu.get_relations_by_item(item)
        return self.render_template(item_type.get_form_template(), 
                                    item=item,
                                    relations=relations,
                                    item_type=item_type.get_name(),
                                    user=self.get_user(),
                                    valid_item_types=self.get_sodocu().get_config().get_item_types())


    def update_single_attribute(self, request, item_type_name, item_id):
        log.debug('update_single_attribute(' + str(request) + ', ' + item_type_name + ', ' + item_id + ')')
        
        if item_id != request.form['id']:
            raise MethodNotAllowed(description='URL and form data do not match!')
        
        item = self.get_item_by_name(item_type_name, item_id)
        
        if item is None:
            raise NotFound()
            
        attribute = request.form['attribute']
        value = request.form['value']
        log.debug("item: " + str(item))
        log.debug("attribute: " + attribute)
        log.debug("value: " + value)
        
        self.get_sodocu().set_attribut(item, attribute, value)
        item.get_meta_data().set_changed_by(self.get_user())
        item.get_meta_data().set_changed_now()
        self.get_sodocu().save_item(item)
        
        # jEditable requires submited data as return value for updating table
        # @see: https://www.datatables.net/forums/discussion/8365/jeditable-datatables-how-can-i-refresh-table-after-edit 
        return Response(request.form['value'])
    
    
    def create_or_update_item(self, request, item_type_name, item_id):
        '''
        Decides to create a new item or update an existing item.
        '''
        log.debug('create_or_update_item(' + str(request) + ', ' + item_type_name + ', ' + item_id+ ')')
        item_type = self.get_sodocu().get_config().get_item_type_by_name(item_type_name)
        item = self.sodocu.get_item_by_id(item_type, item_id)
        log.debug('item: ' + str(item))
        
        if item is None:
            item = create_base_item(item_type, item_id, request.form['name'])
            item.get_meta_data().set_created_by(self.get_user())
            item.get_meta_data().set_created_now()
            self.get_sodocu().add_item(item)
        
        self.update_item(request, item)
        item.get_meta_data().set_changed_by(self.get_user())
        item.get_meta_data().set_changed_now()
        self.get_sodocu().save_item(item)
        
        return redirect('/%s/' % item_type_name)


    def update_item(self, request, item):
        '''
        Updates all item attributes by given form args. 
        '''
        log.debug('update_item(' + str(request) + ', ' + str(item) + ')')
        for key in request.form:
            request_values = ''.join(request.form.getlist(key))
            log.debug('request_values(' + key + '): ' + str(request_values))
            
#             if request_values and request_values != '':
#             if request_values:
            if key.endswith('_by'):
                # order of the two following statements are important because of removing deleted from-relations
                self.update_from_relations(item, key, request_values)
                self.update_value(item.get_relations(), key, request_values)
            elif not key.startswith('_'):
                self.update_value(item, key, request_values)


    def update_from_relations(self, unchanged_item, key, request_values):
        '''
        Deletes from-relations of given by-relation and sets the new from-relations of given by-relation items.
        '''
        log.debug('update_from_relations(' + str(unchanged_item) + ', ' + key + ', ' + str(request_values) + ')')
        if self.remove_from_relations(unchanged_item, key):
            self.add_from_relation(unchanged_item, key, request_values)
                    
            
    def remove_from_relations(self, unchanged_item, key):
        '''
        Removes all from-relations of given by-relation.
        '''
        log.debug('remove_from_relations(' + str(unchanged_item) + ', ' + key + ')')
        
        try:
            getter_by_method = get_getter_method(unchanged_item.get_relations(), key)
            existing_by_relation_item_ids = getter_by_method()
            log.debug('existing_by_relation_item_ids: ' + str(existing_by_relation_item_ids))
        except AttributeError:
            log.info('Item <' + unchanged_item.get_id() + '> has not getter method for key <' + key + '>!')
            return False
        
        for existing_by_relation_item_id in filter(None, existing_by_relation_item_ids):
            try:
                existing_by_relation_item = self.sodocu.get_item_by_id(ItemType(existing_by_relation_item_id.split('-')[0], ''), existing_by_relation_item_id)
                getter_from_method = get_getter_method(existing_by_relation_item.get_relations(), key.replace('_by', '_from'))
                existing_from_relation_items = getter_from_method()
                log.debug('existing_from_relation_items: ' + existing_by_relation_item.get_id() + ' - ' + str(existing_from_relation_items))
                existing_from_relation_items.remove(unchanged_item.get_id())
                log.debug('removed_item_name: ' + unchanged_item.get_id())
                self.get_sodocu().save_item(existing_by_relation_item)
            except KeyError:
                log.info('Item <' + existing_by_relation_item.get_id() + '> has no from relation to item <' + unchanged_item.get_id() + '>!')
        return True


    def add_from_relation(self, unchanged_item, key, request_values):
        log.debug('add_from_relation(' + str(unchanged_item) + ', ' + key + ', ' + str(request_values) + ')')
        
        for request_item_id in filter(None, list(request_values.split(','))):
            log.debug("request_item_id.split('-')[0]: " + request_item_id.split('-')[0])
            request_item = self.sodocu.get_item_by_id(ItemType(request_item_id.split('-')[0], ''), request_item_id)
            log.debug('request_item: ' + str(request_item))
        
            try:
                adder_method = get_adder_method(request_item.get_relations(), key.replace('_by', '_from'))
                log.debug('adder_method: ' + str(adder_method))
                adder_method(unchanged_item.get_id())
                request_item.get_meta_data().set_changed_by(self.get_user())
                request_item.get_meta_data().set_changed_now()
                self.get_sodocu().save_item(request_item)
            except AttributeError:
                log.info('Item <' + request_item.get_id() + '> has not adder method for key <' + key.replace('_by', '_from') + '>!')
                return False
        return True


    def update_value(self, item, key, request_values):
        '''
        Identifies the setter method for given key an sets the given value.
        '''
        log.debug('update_value(' + str(item) + ', ' + key + ', ' + request_values + ')')
        try:
            setter_method = get_setter_method(item, key)
            log.debug('setter_method: ' + str(setter_method))
            setter_method(request_values)
        except AttributeError:
            log.info('Item <' + item.get_id() + '> has not setter method for key <' + key + '>!')


    def get_item_by_name(self, item_type_name, item_id):
        item_type = self.get_sodocu().get_config().get_item_type_by_name(item_type_name)
        return self.get_sodocu().get_item_by_id(item_type, item_id)

    
    def is_valid_item_type(self, item_type_name):
        log.debug('valid item types: ' + str(self.get_sodocu().get_config().get_item_types_as_string()))
        return item_type_name in self.get_sodocu().get_config().get_item_types_as_string()
    
    
    def is_put_request(self, request):
        return (request.method == 'PUT') or (request.method == 'POST' and request.form['_method'].upper() == 'PUT')
                      
                      
    def is_single_attribute_update(self, request):
        log.debug('is_single_attribute_update(' + str(request) + ')')
        return 'attribute' in request.form
                            
    
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

    def get_user(self):
        return self.__user


    def set_user(self, value):
        self.__user = value

    sodocu = property(get_sodocu, None, None, None)
    endpoint = property(get_endpoint, None, None, None)
    user = property(get_user, set_user, None, None)


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
