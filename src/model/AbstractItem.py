'''
Created on 31.01.2014

@author: RKlinger
'''
import ConfigParser

class AbstractItem(object):
    '''
    Abstract class with common properties for all items.
    '''

    def __init__(self, identity, name):
        '''
        Creates a new Item with an ID an a name.
        '''
        self.__id = identity
        self.__name = name
        self.__description = None

    def get_id(self):
        return self.__id

    def set_id(self, value):
        self.__id = value

    def get_name(self):
        return self.__name

    def set_name(self, value):
        self.__name = value

    def get_description(self):
        return self.__description

    def set_description(self, value):
        self.__description = value

    id = property(get_id, set_id, None, None)
    name = property(get_name, set_name, None, None)
    description = property(get_description, set_description, None, None)

    
    def __str__(self):
        return '[id=' + str(self.get_id()) + ', name=' + self.get_name() + ']' 


    def __config__(self):
        config = ConfigParser.ConfigParser()
        
        section_name = self.__class__.__name__.lower()
        config.add_section(section_name)
        config.set(section_name, 'id', self.get_id())
        config.set(section_name, 'name', self.get_name())
        config.set(section_name, 'description', self.get_description() if hasattr(self, 'description') else '')
        return config        
