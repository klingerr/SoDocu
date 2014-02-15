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
    if path is not None:
        head, tail = ntpath.split(path)
        filename = tail or ntpath.basename(head)
        return os.path.splitext(filename)[0]
    return None


def new_line_to_br(value):
    '''
    Custom jinja2 filter for replacing carriage return and new line with <br />.
    '''
    return value.replace("\n", "<br />")


def get_max_id(abstract_items):
    if len(abstract_items) == 0:
        return 0
    
    identifier = 0
    for abstract_item in abstract_items:
        number = abstract_item.get_id().split('-')[1]
        if int(number) > int(identifier):
            identifier = int(number)
    return identifier
    