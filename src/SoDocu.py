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


class SoDocu(object):
    '''
    This is the start point of SoDocu.
    '''

    def __init__(self, config):
        '''
        Reads all items into memory.
        '''
        self.__path = config.get_sodocu_path()
        self.__fileHandler = FileHandler(self.__path)
        self.__ideas = set()
        self.read_all_items()


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

        
    def read_all_items(self):
        directoryWalker = DirectoryWalker(self.get_path())
        for filename in directoryWalker.get_filenames():
            config = read_file(filename)
            item = self.create_item(config)
            if isinstance(item, Idea):
                item.set_filename(filename)
                self.add_idea(item)


    def set_attribut(self, item, attribute, value):
        log.debug('item: ' + str(item))
        log.debug('attribute: ' + attribute)
        log.debug('value: ' + value)
        setter_method = getattr(item, 'set_' + attribute)
        log.debug('setter_method: ' + str(setter_method))
        setter_method(value)


    def get_item_by_id(self, identifier):
        log.debug('identifier: ' + identifier) 
        for idea in self.get_ideas():
            log.debug('idea.get_id: ' + idea.get_id()) 
            if idea.get_id() == identifier:
                return idea


    def create_item(self, config):
        if 'idea' in config.sections():
            return create_idea(config)


    def save_item(self, item):
        self.get_file_handler().update_file(item)
        
        
if __name__ == '__main__':
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    log.info('starting ...')
    config = Config()
    sodoku = SoDocu(config)
    gui = create_gui(sodoku)
    
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, gui, use_debugger=True, use_reloader=True)
