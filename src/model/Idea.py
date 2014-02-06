'''
Created on 03.02.2014

@author: RKlinger
'''
from AbstractItem import AbstractItem
from MetaData import MetaData
from Stakeholder import Stakeholder

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
            raise Exception('InventedBy must be a stakeholder!')
        
    inventedBy = property(get_invented_by, set_invented_by, None, None)
    
    def __str__(self):
        return 'Idea {' + AbstractItem.__str__(self) + MetaData.__str__(self) + '}' 


def create_idea(config):
    idea = Idea(config.get('idea', 'id'), config.get('idea', 'name'))
    idea.set_description(config.get('idea', 'description'))
#     idea.set_invented_by(config.get('idea', 'description'))
    idea.set_created_by(config.get('meta', 'createdBy'))
    idea.set_created_at(config.get('meta', 'createdAt'))
    idea.set_changed_by(config.get('meta', 'changedBy'))
    idea.set_changed_at(config.get('meta', 'changedAt'))
    return idea