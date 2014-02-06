'''
Created on 31.01.2014

@author: RKlinger
'''

import ConfigParser

class FileReader(object):
    '''
    Give methods for reading files.
    '''

    def readTxtFile(self, filename):
        '''
        Reads a textfile as a config file from filesystem and returns its 
        content as a config.
        '''
        config = ConfigParser.ConfigParser()
        config.read(filename)
        return config
    