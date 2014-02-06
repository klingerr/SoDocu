'''
Created on 03.02.2014

@author: RKlinger
'''

import datetime

class MetaData(object):
    '''
    Abstract class with common meta for all items.
    '''

    def __init__(self):
        self.__createdBy = None
        self.__createdAt = None
        self.__changedBy = None
        self.__changedAt = None

    def get_created_by(self):
        return self.__createdBy

    def set_created_by(self, value):
        self.__createdBy = value

    def get_created_at(self):
        return self.__createdAt

    def set_created_at(self, value):
        self.__createdAt = value

    def set_created_now(self):
        self.__createdAt = datetime.datetime.now()

    def get_changed_by(self):
        return self.__changedBy

    def set_changed_by(self, value):
        self.__changedBy = value

    def get_changed_at(self):
        return self.__changedAt

    def set_changed_at(self, value):
        self.__changedAt = value

    def set_changed_now(self):
        self.__changedAt = datetime.datetime.now()

    createdBy = property(get_created_by, set_created_by, None, None)
    createdAt = property(get_created_at, set_created_at, None, None)
    changedBy = property(get_changed_by, set_changed_by, None, None)
    changedAt = property(get_changed_at, set_changed_at, None, None)

    def __str__(self):
        createdBy = str(self.get_created_by()) if hasattr(self, 'createdBy') else 'None'
        createdAt = str(self.get_created_at()) if hasattr(self, 'createdAt') else 'None'
        return '[createdBy=' + createdBy + ', createdAt=' + createdAt + ']' 
