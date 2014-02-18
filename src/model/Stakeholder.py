'''
Created on 03.02.2014

@author: RKlinger
'''
from AbstractItem import AbstractItem
from MetaData import MetaData
from src.model.MetaData import merge_meta_config


class Stakeholder(AbstractItem, MetaData):
    '''
    An stakeholder is affected by the results of this project. It is an 
    invaluable source of information for necessary requirements.
    '''

    def __init__(self, identity, name):
        '''
        Constructor
        '''
        super(Stakeholder, self).__init__(identity, name)
        
    def __str__(self):
        return 'Stakeholder {' + AbstractItem.__str__(self) + MetaData.__str__(self) + '}' 


    def __config__(self):
        meta_config = MetaData.__config__(self)
        abstract_config = AbstractItem.__config__(self)
        config = merge_meta_config(meta_config, abstract_config)
        return config        
