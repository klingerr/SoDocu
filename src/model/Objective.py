'''
Created on 01.04.2014

@author: RKlinger
'''
import logging

from src.model.AbstractItem import AbstractItem
from src.utils.Utils import merge_item_configs

log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class Objective(AbstractItem):
    '''
    An idea isn't a direct requirement artifact. It has to be investigated for 
    business objectivs.
    '''

    def __init__(self, item_type, identity, name):
        '''
        Creates a new objective with given id and name.
        '''
        super(Objective, self).__init__(item_type, identity, name)
        # another objective
        self.__conflicts_with = set()
        # another objective
        self.__depends_on = set()

    def get_conflicts_with(self):
        return self.__conflicts_with


    def get_depends_on(self):
        return self.__depends_on


    def set_conflicts_with(self, value):
        self.__conflicts_with = value


    def set_depends_on(self, value):
        self.__depends_on = value


    def add_conflicts_with(self, value):
        self.__conflicts_with.add(value)


    def add_depends_on(self, value):
        self.__depends_on.add(value)


    conflicts_with = property(get_conflicts_with, set_conflicts_with, None, None)
    depends_on = property(get_depends_on, set_depends_on, None, None)

    
    def __config__(self):
        abstract_config = AbstractItem.__config__(self)
        meta_config = self.get_meta_data().__config__()
        relations_config = self.get_relations().__config__()
        config = merge_item_configs(abstract_config, meta_config)
        config = merge_item_configs(config, relations_config)
        return config        


    def __str__(self):
        return 'Objective {' + AbstractItem.__str__(self) \
                             + self.get_meta_data().__str__() \
                             + self.get_relations().__str__() + '}' 
