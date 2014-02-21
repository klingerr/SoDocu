'''
Created on 31.01.2014

@author: RKlinger
'''
import ConfigParser

from src.model.MetaData import MetaData
from src.model.Relations import Relations
from src.utils.Utils import make_camel_case


class AbstractItem(object):
    '''
    Abstract class with common properties for all items.
    '''

    def __init__(self, item_type, identity, name):
        '''
        Creates a new Item with an ID an a name.
        '''
        self.__id = identity
        self.__name = name
        self.__description = ''
        self.__filename = None
        self.__item_type = item_type
        self.__meta_data = MetaData()
        self.__relations = Relations()

    def get_meta_data(self):
        return self.__meta_data

    def get_relations(self):
        return self.__relations

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

    def get_filename(self):
        return self.__filename

    def set_filename(self, value):
        self.__filename = value

    def get_camel_case_name(self):
        '''
        Returns the basename of the file made off the "camel cased" name.
        '''
        return make_camel_case(self.get_name())

    def get_item_type(self):
        return self.__item_type

    id = property(get_id, set_id, None, None)
    name = property(get_name, set_name, None, None)
    description = property(get_description, set_description, None, None)
    filename = property(get_filename, set_filename, None, None)
    item_type = property(get_item_type, None, None, None)
    meta_data = property(get_meta_data, None, None, None)
    relations = property(get_relations, None, None, None)


    def contains_text(self, text):
        if text.lower() in self.get_id().lower() \
        or text.lower() in self.get_name().lower() \
        or text.lower() in self.get_description().lower():
            return True
        return False 
        
    
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
    

    def __eq__(self, other):
        '''
        Together with __hash__ method necessary for object identity in a set.
        '''
#         return self.__dict__ == other.__dict__
        return self.get_id() == other.get_id()


    def __hash__(self):
        '''
        Together with __eq__ method necessary for object identity in a set.
        '''
        return hash(self.get_id())
    