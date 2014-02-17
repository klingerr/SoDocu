'''
Created on 03.02.2014

@author: RKlinger
'''

import logging.config

from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileHandler import FileHandler, read_file
from src.utils.Config import Config
from src.utils.Utils import create_item
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
        self.__config = sodocu_config
        self.__path = self.__config.get_sodocu_path()
        self.__fileHandler = FileHandler(self.__config)
        # dictionary/map with item_type as key and set of items as value
        self.__items = dict()
        self.read_all_items()

    def get_config(self):
        return self.__config


    def get_path(self):
        return self.__path


    def get_file_handler(self):
        return self.__fileHandler


    def get_items(self, item_type):
        try:
            return self.__items[item_type]
        except KeyError:
            log.info('There are no items of type <' + item_type + '>')
        return None


    def add_item(self, item):
        log.debug('add_item(' + str(item) + ')')
        item_type = item.__class__.__name__.lower()
        items = self.get_items(item_type)
        if items is None:
            self.__items[item_type] = set()
            items = self.get_items(item_type)
        items.add(item)

        
    path = property(get_path, None, None, None)
    fileHandler = property(get_file_handler, None, None, None)
    items = property(get_items, None, None, None)
    config = property(get_config, None, None, None)

        
    # TODO dynamic item type
    def read_all_items(self):
        directoryWalker = DirectoryWalker(self.get_path())
        log.debug('directoryWalker.get_filenames(): ' + str(directoryWalker.get_filenames()))
        for filename in directoryWalker.get_filenames():
            item_config = read_file(filename)
            item = create_item(item_config, filename)
            self.add_item(item)


    def set_attribut(self, item, attribute, value):
        log.debug('set_attribut: ' + str(item) + ', ' + attribute + ', ' + value + ')')
        setter_method = getattr(item, 'set_' + attribute)
        log.debug('setter_method: ' + str(setter_method))
        setter_method(value)


    def get_item_by_id(self, item_type, identifier):
        log.debug('get_item_by_id(: ' + item_type + ', ' + identifier + ')') 
        items = self.get_items(item_type)
        if items is None:
            return None
        
        for item in items:
            log.debug('item.get_id: ' + item.get_id()) 
            if item.get_id() == identifier:
                return item


    def save_item(self, item):
        return self.get_file_handler().update_file(item)
        
        
    def delete_item(self, item_type, item_id):
        item = self.get_item_by_id(item_type, item_id)
        if self.get_file_handler().delete_file(item):
            return self.remove_item(item)
        return False
        

    def remove_item(self, item):
        '''
        Removes the given item from set of item_types
        '''
        item_type = item.__class__.__name__.lower()
        items = self.get_items(item_type)
        if items is None:
            return False
        
        try:
            items.remove(item)
            return True
        except KeyError:
            log.info('There is no item <' + item.get_id() + '> to remove!')
        return False


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    log.info('starting ...')
    config = Config()
    sodoku = SoDocu(config)
    gui = create_gui(sodoku)
    
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, gui, use_debugger=True, use_reloader=True)
