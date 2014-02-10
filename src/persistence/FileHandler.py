'''
Created on 31.01.2014

@author: RKlinger
'''

import ConfigParser


def make_camel_case(text):
    return text.title().replace(' ', '')


class FileHandler(object):
    '''
    Provides methods for reading and writing config files.
    '''
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
    

    def item_to_config(self, item, identifier):
        section_name = item.__class__.__name__.lower()

        config = ConfigParser.ConfigParser()
        
        config.add_section(section_name)
        config.set(section_name, 'id', item.get_id())
        config.set(section_name, 'name', item.get_name())
        config.set(section_name, 'description', item.get_description()  if hasattr(item, 'description') else '')
        
        config.add_section('meta')
        config.set('meta', 'createdBy', item.get_created_by() if hasattr(item, 'createdBy') else '')
        config.set('meta', 'createdAt', item.get_created_at() if hasattr(item, 'createdAt') else '')
        config.set('meta', 'changedBy', item.get_changed_by() if hasattr(item, 'changedBy') else '')
        config.set('meta', 'changedAt', item.get_changed_at() if hasattr(item, 'changedBy') else '')
        return config


    def write_file(self, item):
        identifier = make_camel_case(item.get_name())
        filename = identifier + '.txt'
        # TODO: make path configurable for item types 
        path = self.get_path() + '/sodocu' + '/0_ideas'
        config = self.item_to_config(item, identifier)
        try:
            cfgfile = open(path + '/' + filename, 'w')
            try:
                config.write(cfgfile)
            finally:
                cfgfile.close()
        except IOError:
            print "Error: can\'t find file or read data"


    def get_path(self):
        return self.__path
