'''
Created on 31.01.2014

@author: RKlinger
'''

import ConfigParser

class FileHandler(object):
    '''
    Provides methods for reading and writing config files.
    '''

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
        pass