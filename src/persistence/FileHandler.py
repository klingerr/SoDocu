'''
Created on 31.01.2014

@author: RKlinger
'''

import os
import logging
import ConfigParser
from src.utils.Utils import get_file_basename

log = logging.getLogger('FileHandler')
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)

class FileHandler(object):
    '''
    Provides methods for reading and writing config files.
    '''
    
    file_extension = '.txt'

    
    def __init__(self, path):
        self.__path = path
        

    def read_file(self, filename):
        '''
        Reads a textfile as a config file from filesystem and returns its 
        content as a config.
        '''
        config = ConfigParser.ConfigParser()
        dataset = config.read(filename)
        if len(dataset) == 0:
            raise ValueError, "File not found!"
        return config


    def create_directory(self, item):
        directory = self.get_path() + '/sodocu/' + item.__class__.__name__.lower()
        log.debug('directory: ' + directory)
        if not os.path.exists(directory):
            log.debug(directory + ' does not exists. Creating a new one.')
            os.makedirs(directory)
        return directory


    def create_file(self, item):
        filename = item.get_basename() + self.file_extension
        directory = self.create_directory(item)
        item.set_filename(directory + '/' + filename)
        self.write_file(item)


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


    def update_file(self, item):
        log.debug('item.get_basename(): ' + item.get_basename())
        log.debug('get_file_basename(item.get_filename()): ' + get_file_basename(item.get_filename()))
        if item.get_basename() != get_file_basename(item.get_filename()):
            self.delete_file(item)
            self.create_file(item)
        else:
            self.write_file(item)


    def delete_file(self, item):
        os.remove(item.get_filename())
        

    def get_path(self):
        return self.__path

    path = property(get_path, None, None, None)
