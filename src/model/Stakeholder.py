'''
Created on 03.02.2014

@author: RKlinger
'''
from src.model.AbstractItem import AbstractItem
from src.utils.Utils import merge_item_configs


class Stakeholder(AbstractItem):
    '''
    An stakeholder is affected by the results of this project. It is an 
    invaluable source of information for necessary requirements.
    '''

    def __init__(self, item_type, identity, name):
        '''
        Constructor
        '''
        super(Stakeholder, self).__init__(item_type, identity, name)
        
        
    def __config__(self):
        abstract_config = AbstractItem.__config__(self)
        meta_config = self.get_meta_data().__config__()
        relations_config = self.get_relations().__config__()
        config = merge_item_configs(abstract_config, meta_config)
        config = merge_item_configs(config, relations_config)
        return config        


    def __str__(self):
        return 'Stakeholder {' + AbstractItem.__str__(self) \
                               + self.get_meta_data().__str__() \
                               + self.get_relations().__str__() + '}' 
