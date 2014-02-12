'''
Created on 12.02.2014

@author: RKlinger
'''

import os
import ntpath
import logging

log = logging.getLogger('Utils')
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


def make_camel_case(text):
    return text.title().replace(' ', '')


def get_file_basename(path):
    log.debug('path: ' + str(path)) 
    head, tail = ntpath.split(path)
    filename = tail or ntpath.basename(head)
    return os.path.splitext(filename)[0]
