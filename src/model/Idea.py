'''
Created on 03.02.2014

@author: RKlinger
'''
import logging

from AbstractItem import AbstractItem
from MetaData import MetaData, merge_meta_config
from Stakeholder import Stakeholder


log = logging.getLogger(__name__)


class Idea(AbstractItem, MetaData):
    '''
    An idea isn't a direct requirement artifact. It has to be investigated for 
    business targets.
    '''

    def __init__(self, identity, name):
        '''
        Creates a new idea with given id and name.
        '''
        super(Idea, self).__init__(identity, name)
        self.__inventedBy = None


    def get_invented_by(self):
        return self.__inventedBy


    def set_invented_by(self, value):
        if isinstance(value, Stakeholder):
            self.__inventedBy = value
        else:
            log.warn('InventedBy must be a stakeholder!')
            raise Exception('InventedBy must be a stakeholder!')
        
    inventedBy = property(get_invented_by, set_invented_by, None, None)

    
    def __config__(self):
        meta_config = MetaData.__config__(self)
        abstract_config = AbstractItem.__config__(self)
        config = merge_meta_config(meta_config, abstract_config)
        abstract_config.set('idea', 'inventedBy', self.get_invented_by() if hasattr(self, 'inventedBy') else '')
        return config        


    def __str__(self):
        return 'Idea {' + AbstractItem.__str__(self) + MetaData.__str__(self) + '}' 
