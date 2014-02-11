'''
Created on 03.02.2014

@author: RKlinger
'''

import os
import logging
from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileHandler import FileHandler
from src.model.Idea import Idea, create_idea
from src.view.Gui import create_gui

log = logging.getLogger('sodocu')
# console logger
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class SoDocu(object):
    '''
    This is the start point of SoDocu.
    '''

    def __init__(self, path):
        '''
        Reads all items into memory.
        '''
        self.__path = os.path.abspath(path)
        self.__fileHandler = FileHandler(self.__path)
        # TODO: change to a set with unique entries
        self.__ideas = []
        self.read_all_items()

    def get_path(self):
        return self.__path


    def get_file_handler(self):
        return self.__fileHandler


    def get_ideas(self):
        return self.__ideas


    def add_idea(self, value):
        self.__ideas.append(value)

    path = property(get_path, None, None, None)
    fileHandler = property(get_file_handler, None, None, None)
    ideas = property(get_ideas, None, None, None)

        
    def read_all_items(self):
        directoryWalker = DirectoryWalker(self.get_path())
        for filename in directoryWalker.getFilenames():
            config = self.get_file_handler().read_file(filename)
            item = self.create_item(config)
            if isinstance(item, Idea):
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

        
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    sodoku = SoDocu("../sodocu")
    gui = create_gui(sodoku)
    run_simple('127.0.0.1', 8080, gui, use_debugger=True, use_reloader=True)
