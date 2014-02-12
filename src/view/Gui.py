'''
Created on 04.02.2014

@author: RKlinger
'''

import os
import logging
import urlparse
from werkzeug.debug import DebuggedApplication
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, MethodNotAllowed
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

log = logging.getLogger('Gui')
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


def new_line_to_br(value):
    '''
    Custom jinja2 filter for replacing carriage return and new line with <br />.
    '''
    return value.replace("\n", "<br />")


class Gui(object):
    '''
    Class for web gui following REST style:
    HTTP 
    Method URI                               Action
    GET    http://[hostname]/item/           Retrieve list of items
    GET    http://[hostname]/item/[item_id]  Retrieve a item
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
        
        # initialize jinja template engine
        template_path = os.path.join(os.path.dirname(__file__), '../../web/templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)
        
        # registers the custom filter with Jinja2
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
        constructor.
        '''
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException, e:
            return e


    def get_items(self, item_type):
        get_items = getattr(self.get_sodocu(), 'get_' + item_type + 's')
        items = get_items()
        return items


    def on_item_list(self, request, item_type):
        '''
        On request type GET retrieves all items of specified type.
        On request type POST creates a new item of specified type.
        '''
        if item_type not in ['item', 'idea', 'bla']:
            raise NotFound()
        
        if request.method == 'GET':
            return self.render_template('ideas_table.html', 
                                        items=self.get_items(item_type), 
                                        item_type=item_type)
        elif request.method == 'POST':
#             short_id = self.insert_url(url)
#             return redirect('/%s+' % short_id)
            pass


    def on_single_item(self, request, item_type, item_id):
        '''
        On request type GET retrieves details of specified item.
        On request type PUT updates data of specified item.
        On request type DELETE deletes the of specified item.
        '''
        log.debug('item_type: ' + item_type)
        log.debug('item_id: ' + item_id)
        if item_type not in ['item', 'idea', 'bla']:
            raise NotFound()
        
        log.debug('request.method: ' + request.method)
        if request.method == 'GET':
#             return self.render_template('ideas_table.html', 
#                                         sodocu=self.get_sodocu(), 
#                                         short_id=item_type)
            pass
        elif self.is_put_request(request):
            log.debug('request.method: PUT')
            log.debug("request.form['id']: " + request.form['id'])
            
            if item_id != request.form['id']:
                raise MethodNotAllowed(description='URL and form data do not match!')
            
            attribute = request.form['attribute']
            log.debug("attribute: " + attribute)
            
            idea = self.get_sodocu().get_item_by_id(item_id)
            log.debug("idea: " + str(idea))
            
            self.get_sodocu().set_attribut(idea, attribute, request.form['value'])
            # jEditable requires submited data as return value for updating table
            # @see: https://www.datatables.net/forums/discussion/8365/jeditable-datatables-how-can-i-refresh-table-after-edit 
            return Response(request.form['value'])
        elif request.method == 'DELETE':
            pass

    
    def is_put_request(self, request):
        return (request.method == 'PUT') or (request.method == 'POST' and request.form['_method'].upper() == 'PUT')
                                             
    
    def on_new_url(self, request):
        '''
        This method is called when requesting the base URL, 
        i.e. http://localhost/.
        '''
        error = None
        url = ''
        if request.method == 'POST':
            url = request.form['url']
            if not self.is_valid_url(url):
                error = 'Please enter a valid URL'
            else:
                short_id = self.insert_url(url)
                return redirect('/%s+' % short_id)
        return self.render_template('new_url.html', error=error, url=url)


    def is_valid_url(self, url):
        parts = urlparse.urlparse(url)
        return parts.scheme in ('http', 'https')


    def on_follow_short_link(self, request, short_id):
        '''
        This method is called when requesting the extended URL, 
        i.e. http://localhost/foo.
        '''
        know_urls = {'bla':'http://google.de'}
        link_target = know_urls[short_id]
        if link_target is None:
            raise NotFound()
        return redirect(link_target)


    def on_short_link_details(self, request, short_id):
        '''
        This method is called when requesting the extended URL including 
        details, i.e. http://localhost/foo+.
        '''
        know_urls = {'bla':'http://google.de'}
        link_target = know_urls[short_id]
        if link_target is None:
            raise NotFound()
        click_count = 42
        return self.render_template('short_link_details.html',
            link_target=link_target,
            short_id=short_id,
            click_count=click_count
        )


    def on_short_link_table(self, request, short_id):
        '''
        This method is called when requesting the extended URL including 
        table view, i.e. http://localhost/foo*.
        '''
        if short_id != 'ideas':
            raise NotFound()
        return self.render_template('ideas_table.html',
            sodocu=self.get_sodocu(),
            short_id=short_id
        )


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

    sodocu = property(get_sodocu, None, None, None)


def create_gui(sodocu, with_static=True):
    '''
    Factory method for creating a new instance of Gui. Configuration of static
    content locations is situated here too.
    '''
    gui = Gui(sodocu)
    if with_static:
        gui.wsgi_app = SharedDataMiddleware(gui.wsgi_app, {
            '/js':   os.path.join(os.path.dirname(__file__), '../../web/js'),
            '/css':  os.path.join(os.path.dirname(__file__), '../../web/css'),
            '/img':  os.path.join(os.path.dirname(__file__), '../../web/img')
        })
#    return gui
    return DebuggedApplication(gui, evalex=True)
