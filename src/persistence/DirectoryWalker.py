'''
Created on 31.01.2014

@author: RKlinger
'''

import os

class DirectoryWalker(object):
    '''
    Identifies all SoDocu files in given directory.
    '''
    
    fileExtension = '.txt'
    files = []

    def __init__(self, path):
        '''
        Sets the path of SoDocu for further file reading. 
        '''
        self.sodocuPath = path
        self.findFilesInTree()

    def findFilesInTree(self):
        for root, dirs, files in os.walk(self.sodocuPath):
            for myFile in files:
                print os.path.abspath(os.path.join(root, myFile))
                if myFile.endswith(self.fileExtension):
                    self.files.append(os.path.abspath(os.path.join(root, myFile)))

    def getFilenames(self):
        '''
        Returns discovered filenames as a list.
        '''
        print self.files
        return self.files
        