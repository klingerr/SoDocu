'''
Created on 03.02.2014

@author: RKlinger
'''

import logging.config

from src.model.Idea import Idea, create_idea
from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileHandler import FileHandler, read_file
from src.view.Gui import create_gui
from src.utils.Config import Config

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
        self.__ideas = set()
        self.read_all_items()

    def get_config(self):
        return self.__config


    def get_path(self):
        return self.__path


    def get_file_handler(self):
        return self.__fileHandler


    def get_ideas(self):
        return self.__ideas


    def add_idea(self, value):
        self.__ideas.add(value)
        
    path = property(get_path, None, None, None)
    fileHandler = property(get_file_handler, None, None, None)
    ideas = property(get_ideas, None, None, None)
    config = property(get_config, None, None, None)

        
    # TODO dynamic item type
    def read_all_items(self):
        directoryWalker = DirectoryWalker(self.get_path())
        log.debug('directoryWalker.get_filenames(): ' + str(directoryWalker.get_filenames()))
        for filename in directoryWalker.get_filenames():
            item_config = read_file(filename)
            item = self.create_item(item_config, filename)
            if isinstance(item, Idea):
                self.add_idea(item)


    def set_attribut(self, item, attribute, value):
        log.debug('item: ' + str(item))
        log.debug('attribute: ' + attribute)
        log.debug('value: ' + value)
        setter_method = getattr(item, 'set_' + attribute)
        log.debug('setter_method: ' + str(setter_method))
        setter_method(value)


    def get_item_by_id(self, item_type, identifier):
        log.debug('get_item_by_id(: ' + item_type + ', ' + identifier + ')') 
        for item in self.get_items(item_type):
            log.debug('item.get_id: ' + item.get_id()) 
            if item.get_id() == identifier:
                return item


    def get_items(self, item_type):
        log.debug('get_items(: ' + item_type + ')')
        getter_method = self.get_get_items_method(item_type)
        return getter_method()


    def get_get_items_method(self, item_type):
        '''
        Returns the correct getter method for given item type.
        '''
        if hasattr(self, 'get_' + str(item_type) + 's'):
            log.debug('getter_method: get_' + str(item_type) + 's')
            getter_method = getattr(self, 'get_' + str(item_type) + 's')
            log.debug('getter_method: ' + str(getter_method))
            return getter_method
        else:
            log.warn('Sodocu has no method get_' + str(item_type) + 's!')
            return None


    # TODO dynamic item type
    def create_item(self, item_config, filename):
        if 'idea' in item_config.sections():
            return create_idea(item_config, filename)


    def save_item(self, item):
        return self.get_file_handler().update_file(item)
        
        
    def delete_item(self, item_type, item_id):
        item = self.get_item_by_id(item_type, item_id)
        if self.get_file_handler().delete_file(item):
            return self.remove_item(item)
        return False
        

    # TODO dynamic item type
    def remove_item(self, item):
        for idea in self.get_ideas():
            if idea.get_id() == item.get_id():
                log.debug('remove item: ' + idea.get_id()) 
                self.get_ideas().remove(idea)
                return True
        return False


if __name__ == '__main__':
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    log.info('starting ...')
    config = Config()
    sodoku = SoDocu(config)
    gui = create_gui(sodoku)
    
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, gui, use_debugger=True, use_reloader=True)
