'''
Created on 31.01.2014

@author: RKlinger
'''

import os
import logging
import ConfigParser
from src.utils.Utils import get_file_basename

log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class FileHandler(object):
    '''
    Provides methods for CRUD operations on config files.
    '''
    
    file_extension = '.txt'

    
    def __init__(self, config):
        self.__config = config
        

    def create_file(self, item):
        log.debug('create_file(' + str(item) + ')')
        filename = item.get_camel_case_name() + self.file_extension
        directory = self.create_directory(item)
        if directory is not None:
            item.set_filename(directory + '/' + filename)
            log.info('writing file: ' + item.get_filename())
            return self.write_file(item)
        return False


    def update_file(self, item):
        log.debug('update_file(' + str(item) + ')')
#         log.debug('item.get_camel_case_name(): ' + item.get_camel_case_name())
#         log.debug('get_file_basename(item.get_filename()): ' + str(get_file_basename(item.get_filename())))
        if get_file_basename(item.get_filename()) is None:
            return self.create_file(item)
        elif item.get_camel_case_name() != get_file_basename(item.get_filename()):
            if self.delete_file(item):
                return self.create_file(item)
            return False
        else:
            return self.write_file(item)


    def delete_file(self, item):
        log.debug('delete_file: ' + item.get_filename())
        try:
            os.remove(item.get_filename())
            return True
        except OSError:
            log.warn('Could not delete file ' + item.get_filename())
        return False


    def create_directory(self, item):
        item_type = self.get_config().get_item_type_by_name(item.__class__.__name__.lower())
        directory = os.path.join(self.get_config().get_sodocu_path(), item_type.get_path())
        log.debug('directory: ' + directory)
        if not os.path.exists(directory):
            log.info(directory + ' does not exists. Creating a new one.')
            os.makedirs(directory)
        return directory


    def write_file(self, item):
        log.debug('write_file(' + str(item) + ')')
        item_config = item.__config__()
        return write_file(item_config, item.get_filename())


    def get_config(self):
        return self.__config

    config = property(get_config, None, None, None)


def read_file(filename):
    '''
    Reads a textfile as a config file from filesystem and returns its 
    content as a config.
    '''
    log.info('read_file(' + filename + ')')
    config = ConfigParser.ConfigParser()
    dataset = config.read(filename)
    if len(dataset) == 0:
        raise ValueError("File not found!")
    return config


def write_file(config, filename):
    log.info('write_file(' + str(config) + ', ' + filename + ')')
    try:
        cfgfile = open(filename, 'w')
        try:
            config.write(cfgfile)
            return True
        finally:
            cfgfile.close()
    except IOError:
        log.warn("Error: can\'t find file or read data")
    return False
