'''
Created on 19.02.2014

@author: RKlinger
'''

from ConfigParser import ConfigParser
import json
import logging
import os

from src.persistence.FileHandler import read_file, write_file


# @see: http://pymotw.com/2/json/
log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class Glossary(object):
    '''
    Class for reading and manipulating the glossary.
    '''
    SECTION_NAME = 'glossary'

    def __init__(self, sodocu_path):
        self.__sodocu_path = sodocu_path
        # dictionary with key as term and value as description
        self.__entries = dict()
        # read the glossary from file
        self.read_glossary()


    def get_sodocu_path(self):
        return self.__sodocu_path


    def get_entries(self):
        return self.__entries


    def get_entries_as_json(self):
        entry_list = []
        for key in sorted(self.get_entries().keys()):
            entry_list.append({'term':key, 'description':self.get_entries()[key]})
        log.debug('entry_list: ' + str(entry_list))
#         return json.dumps(entry_list, indent=2)
        return json.dumps(entry_list)


    def add_entry(self, key, value):
        self.__entries[key] = value


    def clear_entries(self):
        return self.__entries.clear()


    def read_glossary(self):
        self.clear_entries()
        log.debug('sodocu_path: ' + str(self.sodocu_path))
        conf_file = os.path.join(self.sodocu_path, 'glossary.txt')
        log.debug('conf_file: ' + conf_file)
        config = read_file(conf_file)
        
        for option in config.options(Glossary.SECTION_NAME):
            self.add_entry(option, config.get(Glossary.SECTION_NAME, option))
        

    def write_glossary(self):
        log.debug('write_glossary(' + self.sodocu_path + ')')
        conf_file = os.path.join(self.sodocu_path, 'glossary.txt')
        log.debug('conf_file: ' + conf_file)

        config = ConfigParser()
        config.add_section(Glossary.SECTION_NAME)
        for term in self.get_entries():
            config.set(Glossary.SECTION_NAME, term, self.entries[term])

        return write_file(config, conf_file)

        
    def update_glossary(self):
        self.write_glossary()
        self.read_glossary()


    entries = property(get_entries, None, None, None)
    sodocu_path = property(get_sodocu_path, None, None, None)
        