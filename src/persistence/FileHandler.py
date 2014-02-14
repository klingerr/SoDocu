'''
Created on 31.01.2014

@author: RKlinger
'''

import os
import logging
import ConfigParser
from src.utils.Utils import get_file_basename

log = logging.getLogger(__name__)


class FileHandler(object):
    '''
    Provides methods for CRUD operations on config files.
    '''
    
    file_extension = '.txt'

    
    def __init__(self, path):
        self.__path = path
        

    def create_file(self, item):
        filename = item.get_camel_case_name() + self.file_extension
        directory = self.create_directory(item)
        item.set_filename(directory + '/' + filename)
        log.info('writing file: ' + item.get_filename())
        self.write_file(item)


    def read_file(self, filename):
        '''
        Reads a textfile as a config file from filesystem and returns its 
        content as a config.
        '''
        config = ConfigParser.ConfigParser()
        log.info('reading file: ' + filename)
        dataset = config.read(filename)
        if len(dataset) == 0:
            raise ValueError, "File not found!"
        return config


    def update_file(self, item):
        log.debug('item.get_camel_case_name(): ' + item.get_camel_case_name())
        log.debug('get_file_basename(item.get_filename()): ' + get_file_basename(item.get_filename()))
        if item.get_camel_case_name() != get_file_basename(item.get_filename()):
            self.delete_file(item)
            self.create_file(item)
        else:
            self.write_file(item)


    def delete_file(self, item):
        log.info('deleting file: ' + item.get_filename())
        os.remove(item.get_filename())
        

    def create_directory(self, item):
        directory = self.get_path() + "/" + item.__class__.__name__.lower()
        log.debug('directory: ' + directory)
        if not os.path.exists(directory):
            log.info(directory + ' does not exists. Creating a new one.')
            os.makedirs(directory)
        return directory


    def write_file(self, item):
        config = item.__config__()
        try:
            cfgfile = open(item.get_filename(), 'w')
            try:
                config.write(cfgfile)
            finally:
                cfgfile.close()
        
        except IOError:
            log.warn("Error: can\'t find file or read data")


    def get_path(self):
        return self.__path

    path = property(get_path, None, None, None)
