'''
Created on 14.02.2014

@author: RKlinger
'''
import os
import logging

from src.persistence.FileHandler import read_file
from src.utils.ItemType import ItemType

log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class Config(object):
    '''
    Reads and holds the current configuration of SoDocu.
    '''
    FIX_OPTIONS = ['path', 'menu_position', 'form_template', 'table_template']


    def __init__(self):
        '''
        Reads the current configuration from sodocu.conf. 
        '''
        self.__sodocu_path = None
        # set of unique item types
        self.__item_types = set()
        self.__project_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))
        self.read_config()

    def get_sodocu_path(self):
        return self.__sodocu_path


    def set_sodocu_path(self, path):
        self.__sodocu_path = path


    def get_item_types(self):
        # @see: https://wiki.python.org/moin/HowTo/Sorting
        return sorted(list(self.__item_types), key=lambda item_type: int(item_type.menu_position))


    def add_item_type(self, item_type):
        return self.__item_types.add(item_type)


    def clear_item_types(self):
        return self.__item_types.clear()
    

    def get_project_path(self):
        return self.__project_path


    def get_item_types_as_string(self):
        item_type_strings = set()
        for item_type in self.get_item_types():
            item_type_strings.add(item_type.get_name())
        log.debug('item_type_strings: ' + str(item_type_strings))
        return item_type_strings
        

    def is_valid_item_type(self, type_name):
        for item_type in self.get_item_types():
            if item_type.get_name() == type_name:
                return True
        return False
    
    
    def get_item_type_by_name(self, item_type_name):
        log.debug('get_item_type_by_name(' + item_type_name + ')')
        for item_type in self.get_item_types():
            log.debug('item_type: ' + str(item_type))
            if item_type.get_name() == item_type_name:
                return item_type
        log.warn('Item type <' + item_type_name + '> is not valid!')
#         raise Exception('Item type <' + item_type_name + '> is not valid!')
    
 
    def read_config(self):
        conf_file = os.path.join(self.get_project_path(), 'sodocu.conf')
        log.debug('conf_file: ' + conf_file)
        config = read_file(conf_file)
        self.set_sodocu_path(os.path.join(self.get_project_path(), config.get('main', 'path')))

        # fill all item options        
        self.clear_item_types()
        for section in config.sections():
            if section != 'main':
                # fix options
                item_type = ItemType(section, config.get(section, 'path'))
                item_type.set_menu_position(config.get(section, 'menu_position'))
                item_type.set_img_url(config.get(section, 'img_url'))
                item_type.set_form_template(config.get(section, 'form_template'))
                item_type.set_table_template(config.get(section, 'table_template'))
                
                # variable relations options
                for option in config.options(section):
                    if option not in Config.FIX_OPTIONS and (option.endswith('_by') or option.endswith('_from')):
                        item_type.add_valid_relation(option, config.get(section, option))
                        
                self.add_item_type(item_type)
                
                
    sodocu_path = property(get_sodocu_path, set_sodocu_path, None, None)
    item_types = property(get_item_types, None, None, None)
    project_path = property(get_project_path, None, None, None)
                
