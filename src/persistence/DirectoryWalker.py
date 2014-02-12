'''
Created on 31.01.2014

@author: RKlinger
'''

import os

class DirectoryWalker(object):
    '''
    Identifies all SoDocu files in given directory.
    '''
    
    file_extension = '.txt'

    def __init__(self, path):
        '''
        Sets the path of SoDocu for further file reading. 
        '''
        self.__sodocuPath = path
        self.__filenames = set()
        self.find_all_files()


    def get_sodocu_path(self):
        return self.__sodocuPath


    def get_filenames(self):
        return self.__filenames


    def add_filename(self, filename):
        return self.__filenames.add(filename)


    def find_all_files(self):
        for root, dirs, files in os.walk(self.get_sodocu_path()):
            for myFile in files:
#                 print os.path.abspath(os.path.join(root, myFile))
                if myFile.endswith(self.file_extension):
                    self.add_filename(os.path.abspath(os.path.join(root, myFile)))


    sodocuPath = property(get_sodocu_path, None, None, None)
    filenames = property(get_filenames, None, None, None)
        