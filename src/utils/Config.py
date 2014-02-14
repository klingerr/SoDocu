'''
Created on 14.02.2014

@author: RKlinger
'''
import os
import logging

from src.persistence.FileHandler import read_file
from src.utils.ItemType import ItemType


# @see: http://pymotw.com/2/json/
log = logging.getLogger(__name__)


class Config(object):
    '''
    Reads and holds the current configuration of SoDocu.
    '''

    def __init__(self):
        '''
        Reads the current configuration from sodocu.json. 
        '''
        self.__sodocu_path = '../sodocu/'
        # set of unique item types
        self.__item_types = set()
        self.read_config()


    def get_sodocu_path(self):
        return self.__sodocu_path


    def set_sodocu_path(self, path):
        self.__sodocu_path = path


    def get_item_types(self):
        return self.__item_types


    def add_item_type(self, item_type):
        return self.__item_types.add(item_type)


    def clear_item_types(self):
        return self.__item_types.clear()

    def get_item_types_as_string(self):
        item_type_strings = set()
        for item_type in self.get_item_types():
            item_type_strings.add(str(item_type))
        return item_type_strings
        

    def is_valid_item_type(self, type_name):
        for item_type in self.get_item_types():
            if item_type.get_name() == type_name:
                return True
        return False
    
    
    def get_item_type(self, type_name):
        for item_type in self.get_item_types():
            if item_type.get_name() == type_name:
                return item_type
        log.warn('Item type <' + type_name + '> is not valid!')
        raise Exception('Item type <' + type_name + '> is not valid!')
    
 
    def read_config(self):
        self.clear_item_types()
        config = read_file(os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir)) + '/sodocu.conf')
        self.set_sodocu_path(config.get('main', 'path'))
        
        for section in config.sections():
            if section != 'main':
                self.add_item_type(ItemType(section, config.get(section, 'path')))
