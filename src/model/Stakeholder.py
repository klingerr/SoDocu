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
        
    def __str__(self):
        return 'Stakeholder {' + AbstractItem.__str__(self) + str(self.get_meta_data()) + '}' 


    def __config__(self):
        meta_config = self.get_meta_data().__config__()
        abstract_config = AbstractItem.__config__(self)
        config = merge_item_configs(meta_config, abstract_config)
        return config        
