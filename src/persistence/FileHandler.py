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
    

    def write_file(self, item):
        identifier = make_camel_case(item.get_name())
        filename = identifier + '.txt'
        # TODO: make path configurable for item types 
        path = self.get_path() + '/sodocu' + '/0_ideas'
        config = item.__config__()
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

    path = property(get_path, None, None, None)
