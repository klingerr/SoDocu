'''
Created on 03.02.2014

@author: RKlinger
'''
import logging

from src.model.AbstractItem import AbstractItem
from src.model.Stakeholder import Stakeholder
from src.utils.Utils import merge_item_configs


log = logging.getLogger(__name__)


class Idea(AbstractItem):
    '''
    An idea isn't a direct requirement artifact. It has to be investigated for 
    business targets.
    '''

    def __init__(self, item_type, identity, name):
        '''
        Creates a new idea with given id and name.
        '''
        super(Idea, self).__init__(item_type, identity, name)
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
        abstract_config = AbstractItem.__config__(self)
        meta_config = self.get_meta_data().__config__()
        relations_config = self.get_relations().__config__()
        config = merge_item_configs(abstract_config, meta_config)
        config = merge_item_configs(config, relations_config)
        config.set('idea', 'inventedBy', self.get_invented_by() if hasattr(self, 'inventedBy') else '')
        return config        


    def __str__(self):
        return 'Idea {' + AbstractItem.__str__(self) \
                        + self.get_meta_data().__str__() \
                        + self.get_relations().__str__() + '}' 
