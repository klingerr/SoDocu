'''
Created on 12.02.2014

@author: RKlinger
'''

import importlib
import logging
import ntpath
import os


log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


def make_camel_case(text):
    '''
    Returns a single camel cased word from given text with whitespaces.
    '''
    return text.title().replace(' ', '')


def get_file_basename(path):
    '''
    Returns the filename without extension.
    '''
    log.debug('path: ' + str(path)) 
    if path is not None:
        head, tail = ntpath.split(path)
        filename = tail or ntpath.basename(head)
        return os.path.splitext(filename)[0]
    return None


def new_line_to_br(value):
    '''
    Custom jinja2 filter for replacing carriage return and new line with <br />.
    '''
    return value.replace("\n", "<br />")


def get_max_id(abstract_items):
    '''
    Returns the highest ID from the given set of items as a number.
    '''
    if len(abstract_items) == 0:
        return 0
    
    identifier = 0
    for abstract_item in abstract_items:
        number = abstract_item.get_id().split('-')[1]
        if int(number) > int(identifier):
            identifier = int(number)
    return identifier


def create_base_item(item_type, item_id, item_name):
    '''
    Creates a new item model class by given item_type with given item_id an name.
    '''
    log.debug('create_base_item(' + item_type + ', ' + item_id + ', ' + item_name + ')')
    log.debug('item_type.title(): ' + item_type.title())
#     module = __import__('src.model.' + item_type.title())
    module = importlib.import_module('src.model.' + item_type.title())
    log.debug('module: ' + str(module))
    item_class = getattr(module, item_type.title())   
    log.debug('item_class: ' + str(item_class))
    item = item_class(item_id, item_name)
    log.debug('item: ' + str(item))
    return item


def create_item(config, filename):
    '''
    Creates an item from config file.
    '''
    item_type = config.sections()[0]
    log.debug('item_type: ' + item_type)
    log.debug("config.get(item_type, 'id'): " + config.get(item_type, 'id'))
    log.debug("config.get(item_type, 'name'): " + config.get(item_type, 'name'))
    
    item = create_base_item(item_type, config.get(item_type, 'id'), config.get(item_type, 'name'))
    item.set_filename(filename) 
    
    for section in config.sections():
        for option in config.options(section):
            try:
                setter_method = getattr(item, 'set_' + option)
                log.debug('setter_method: ' + str(setter_method))
                setter_method(config.get(section, option))
            except AttributeError:
                log.info('Item <' + item.get_id() + '> has not setter method for option <' + option + '>!')
    return item
