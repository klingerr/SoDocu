'''
Created on 19.02.2014

@author: RKlinger
'''

import os
import logging
# @see: http://pymotw.com/2/json/
import json

from src.persistence.FileHandler import read_file

log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class Glossary(object):
    '''
    Class for reading and manipulating the glossary.
    '''
    SECTION = 'glossary'

    def __init__(self):
        # dictionary with key as term and value as description
        self.__entries = dict()


    def get_entries(self):
        return self.__entries


    def get_entries_as_json(self):
        entry_list = []
        for key in sorted(self.get_entries().keys()):
            entry_list.append({'term':key, 'description':self.get_entries()[key]})
        log.debug('entry_list: ' + str(entry_list))
        return json.dumps(entry_list, indent=2)


    def add_entry(self, key, value):
        self.__entries[key] = value


    def clear_entries(self):
        return self.__entries.clear()


    def read_glossary(self, sodocu_path):
        self.clear_entries()
        log.debug('sodocu_path: ' + str(sodocu_path))
        conf_file = os.path.join(sodocu_path, 'glossary.txt')
        log.debug('conf_file: ' + conf_file)
        config = read_file(conf_file)
        
        for option in config.options(Glossary.SECTION):
            self.add_entry(option, config.get(Glossary.SECTION, option))
        

    entries = property(get_entries, None, None, None)
        