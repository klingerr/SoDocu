'''
Created on 03.02.2014

@author: RKlinger
'''

import logging.config

from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileHandler import FileHandler, read_file
from src.utils.Config import Config
from src.utils.Glossary import Glossary
from src.utils.Utils import create_item, get_setter_method
from src.view.Gui import create_gui


log = logging.getLogger('SoDocu')
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class SoDocu(object):
    '''
    This is the start point of SoDocu.
    '''

    def __init__(self, sodocu_config):
        '''
        Reads all items into memory.
        '''
        self.__glossary = Glossary()
        self.__config = sodocu_config
        self.__path = self.__config.get_sodocu_path()
        self.__fileHandler = FileHandler(self.__config)
        # dictionary/map with item_type_name as key and set of items as value
        self.__items = self.initialize_items_dictionary()
        self.read_all_items(self.__config)


    def initialize_items_dictionary(self):
        '''
        Creates a dictionary with one key for each item type and an empty set as value.
        '''
        items = dict()
        for item_type_name in self.get_config().get_item_types_as_string():
            items[item_type_name] = set()
        return items 


    def get_glossary(self):
        return self.__glossary


    def get_config(self):
        return self.__config


    def get_path(self):
        return self.__path


    def get_file_handler(self):
        return self.__fileHandler


    def get_items(self):
        return self.__items


    def get_items_by_type(self, item_type):
        try:
            return self.__items[item_type.get_name()]
        except KeyError:
            log.info('There are no items of type <' + item_type + '>')
        return None


    def add_item(self, item):
        log.debug('add_item(' + str(item) + ')')
        item_type = item.get_item_type()
        items = self.get_items_by_type(item_type)
#         if items is None:
#             self.__items[item_type.get_name()] = set()
#             items = self.get_items_by_type(item_type)
        items.add(item)

        
    glossary = property(get_glossary, None, None, None)
    path = property(get_path, None, None, None)
    fileHandler = property(get_file_handler, None, None, None)
    items = property(get_items_by_type, None, None, None)
    config = property(get_config, None, None, None)

        
    def read_all_items(self, sodocu_config):
        directoryWalker = DirectoryWalker(self.get_path())
        log.debug('directoryWalker.get_filenames(): ' + str(directoryWalker.get_filenames()))
        for filename in directoryWalker.get_filenames():
            item_config = read_file(filename)
            item = create_item(sodocu_config, item_config, filename)
            self.add_item(item)


    def set_attribut(self, item, attribute, value):
        log.debug('set_attribut: ' + str(item) + ', ' + attribute + ', ' + value + ')')
        setter_method = get_setter_method(item, attribute)
        log.debug('setter_method: ' + str(setter_method))
        setter_method(value)


    def get_item_by_id(self, item_type, identifier):
        log.debug('get_item_by_id(' + str(item_type) + ', ' + str(identifier) + ')') 
        items = self.get_items_by_type(item_type)
        if items is None:
            log.debug('item: ' + str(None)) 
            return None
        
        for item in items:
            if item.get_id() == identifier:
                log.debug('item: ' + str(item)) 
                return item


    def save_item(self, item):
        return self.get_file_handler().update_file(item)
        
        
    def delete_item(self, item):
        if self.get_file_handler().delete_file(item):
            return self.remove_item(item)
        return False
        

    def remove_item(self, item):
        '''
        Removes the given item from set of item_types
        '''
        items = self.get_items_by_type(item.get_item_type())
        if items is None:
            return False
        
        try:
            items.remove(item)
            return True
        except KeyError:
            log.info('There is no item <' + item.get_id() + '> to remove!')
        return False


    def search(self, search_string):
        results = set()
        for key in self.get_items().keys():
            item_type = self.get_config().get_item_type(key)
            for value in self.get_items_by_type(item_type):
                if value.contains_text(search_string):
                    results.add(value)
        return results


    def read_glossary_as_json(self):
        self.get_glossary().read_glossary(self.get_config().get_sodocu_path())
        return self.get_glossary().get_entries_as_json()
        

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    log.info('starting ...')
    config = Config()
    sodoku = SoDocu(config)
    gui = create_gui(sodoku)
    
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, gui, use_debugger=True, use_reloader=True)
