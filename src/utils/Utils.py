'''
Created on 12.02.2014

@author: RKlinger
'''

from ConfigParser import ConfigParser
import importlib
import logging
import ntpath
import os

from src.model.MetaData import MetaData
from src.model.Relations import Relations


log = logging.getLogger(__name__)
# console logger
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


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
    log.debug('create_base_item(' + str(item_type) + ', ' + item_id + ', ' + item_name + ')')
    log.debug('item_type.title(): ' + item_type.get_name().title())
    module = importlib.import_module('src.model.' + item_type.get_name().title())
    log.debug('module: ' + str(module))
    item_class = getattr(module, item_type.get_name().title())   
    log.debug('item_class: ' + str(item_class))
    item = item_class(item_type, item_id, item_name)
    log.debug('item: ' + str(item))
    return item


def create_item(sodocu_config, item_config, filename):
    '''
    Creates an item from item_config file.
    '''
    item_type_name = item_config.sections()[0]
    log.debug('item_type_name: ' + item_type_name)
    log.debug("item_config.get(item_type_name, 'id'): " + item_config.get(item_type_name, 'id'))
    log.debug("item_config.get(item_type_name, 'name'): " + item_config.get(item_type_name, 'name'))
    
    item = create_base_item(sodocu_config.get_item_type(item_type_name), item_config.get(item_type_name, 'id'), item_config.get(item_type_name, 'name'))
    item.set_filename(filename) 
    
    for section in item_config.sections():
        log.debug('section: ' + section)
        if section in sodocu_config.get_item_types_as_string():
            fill_item(item, item_config, section)
        elif section == MetaData.SECTION_NAME:
            fill_item(item.get_meta_data(), item_config, section)
        elif section == Relations.SECTION_NAME:
            fill_item(item.get_relations(), item_config, section)
    return item


def fill_item(obj, item_config, section):
    log.debug('fill_item(' + str(obj) + ', ' + str(item_config) + ', ' + section + ')')
    for option in item_config.options(section):
        # direct class methods
        try:
            setter_method = get_setter_method(obj, option)
            setter_method(item_config.get(section, option))
        except AttributeError:
            log.info('Item file has no setter method for option <' + option + '>!')
    

def get_setter_method(obj, option):
    setter_method = getattr(obj, 'set_' + option)
    log.debug('setter_method: ' + str(setter_method))
    return setter_method
    

def merge_item_configs(first_config, second_config):
    '''
    Copies options from MetaData into given config.
    '''
    config = ConfigParser()
    copy_config(first_config, config)
    copy_config(second_config, config)
    return config


def copy_config(source, dest):
    for section in source.sections():
        dest.add_section(section)
        for option in source.options(section):
            dest.set(section, option, source.get(section, option))
    