'''
Created on 12.02.2014

@author: RKlinger
'''

import os
import ntpath
import logging

log = logging.getLogger(__name__)


def make_camel_case(text):
    return text.title().replace(' ', '')


def get_file_basename(path):
    log.debug('path: ' + str(path)) 
    head, tail = ntpath.split(path)
    filename = tail or ntpath.basename(head)
    return os.path.splitext(filename)[0]


def new_line_to_br(value):
    '''
    Custom jinja2 filter for replacing carriage return and new line with <br />.
    '''
    return value.replace("\n", "<br />")

