'''
Created on 03.02.2014

@author: RKlinger
'''

import logging
from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileReader import FileReader
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
        self.__fileReader = FileReader()
        self.__path = path
        self.__ideas = []
        self.read_all_items()

    def get_path(self):
        return self.__path

    def get_ideas(self):
        return self.__ideas

    def add_idea(self, value):
        self.__ideas.append(value)

        
    def read_all_items(self):
        directoryWalker = DirectoryWalker(self.get_path())
        for filename in directoryWalker.getFilenames():
            config = self.__fileReader.readTxtFile(filename)
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
    sodoku = SoDocu("C:\workspace\Head\SoDocu\sodocu")
    gui = create_gui(sodoku)
    run_simple('127.0.0.1', 80, gui, use_debugger=True, use_reloader=True)
