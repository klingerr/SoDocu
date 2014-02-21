'''
Created on 03.02.2014

@author: RKlinger
'''
from ConfigParser import ConfigParser
import logging

log = logging.getLogger(__name__)
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)

class Relations(object):
    '''
    Abstract class with all kinds of relations for all items.
    '''
    SECTION_NAME = 'relations'

    def __init__(self):
        # userStory
        self.__accomplished_by = set()
        # target
        self.__accomplished_from = set()
        # requirement
        self.__extracted_by =  set()
        # userStory
        self.__extracted_from = set()
        # topic
        self.__grouped_by = set()
        # idea, userStory
        self.__grouped_from = set()
        # stakeholder 
        self.__invented_by = set()
        # problem, target, idea
        self.__invented_from = set()
        # target
        self.__refined_by = set()
        # target
        self.__refined_from = set()
        # target
        self.__solved_by = set()
        # problem
        self.__solved_from = set()
        # userStory
        self.__specified_by = set()
        # idea
        self.__specified_from = set()
        # acceptenceCriteria
        self.__verified_by = set()
        # userStory
        self.__verified_from = set()

    def get_accomplished_by(self):
        return self.__accomplished_by


    def get_accomplished_from(self):
        return self.__accomplished_from


    def get_extracted_by(self):
        return self.__extracted_by


    def get_extracted_from(self):
        return self.__extracted_from


    def get_grouped_by(self):
        return self.__grouped_by


    def get_grouped_from(self):
        return self.__grouped_from


    def get_invented_by(self):
        return self.__invented_by


    def get_invented_from(self):
        return self.__invented_from


    def get_refined_by(self):
        return self.__refined_by


    def get_refined_from(self):
        return self.__refined_from


    def get_solved_by(self):
        return self.__solved_by


    def get_solved_from(self):
        return self.__solved_from


    def get_specified_by(self):
        return self.__specified_by


    def get_specified_from(self):
        return self.__specified_from


    def get_verified_by(self):
        return self.__verified_by


    def get_verified_from(self):
        return self.__verified_from


    def set_accomplished_by(self, value):
        self.__accomplished_by = set(value.split(','))


    def set_accomplished_from(self, value):
        self.__accomplished_from = set(value.split(','))


    def set_extracted_by(self, value):
        self.__extracted_by = set(value.split(','))


    def set_extracted_from(self, value):
        self.__extracted_from = set(value.split(','))


    def set_grouped_by(self, value):
        self.__grouped_by = set(value.split(','))


    def set_grouped_from(self, value):
        self.__grouped_from = set(value.split(','))


    def set_invented_by(self, value):
        self.__invented_by = set(value.split(','))


    def set_invented_from(self, value):
        self.__invented_from = set(value.split(','))


    def set_refined_by(self, value):
        self.__refined_by = set(value.split(','))


    def set_refined_from(self, value):
        self.__refined_from = set(value.split(','))


    def set_solved_by(self, value):
        self.__solved_by = set(value.split(','))


    def set_solved_from(self, value):
        self.__solved_from = set(value.split(','))


    def set_specified_by(self, value):
        self.__specified_by = set(value.split(','))


    def set_specified_from(self, value):
        self.__specified_from = set(value.split(','))


    def set_verified_by(self, value):
        self.__verified_by = set(value.split(','))


    def set_verified_from(self, value):
        self.__verified_from = set(value.split(','))


    def add_accomplished_by(self, value):
        self.__accomplished_by.add(value)


    def add_accomplished_from(self, value):
        self.__accomplished_from.add(value)


    def add_extracted_by(self, value):
        self.__extracted_by.add(value)


    def add_extracted_from(self, value):
        self.__extracted_from.add(value)


    def add_grouped_by(self, value):
        self.__grouped_by.add(value)


    def add_grouped_from(self, value):
        self.__grouped_from.add(value)


    def add_invented_by(self, value):
        self.__invented_by.add(value)


    def add_invented_from(self, value):
        self.__invented_from.add(value)


    def add_refined_by(self, value):
        self.__refined_by.add(value)


    def add_refined_from(self, value):
        self.__refined_from.add(value)


    def add_solved_by(self, value):
        self.__solved_by.add(value)


    def add_solved_from(self, value):
        self.__solved_from.add(value)


    def add_specified_by(self, value):
        self.__specified_by.add(value)


    def add_specified_from(self, value):
        self.__specified_from.add(value)


    def add_verified_by(self, value):
        self.__verified_by.add(value)


    def add_verified_from(self, value):
        self.__verified_from.add(value)

        
    def get_existing_relations(self):
        items = []
        for key in self.__dict__.keys():
#             log.debug('key: ' + str(key.replace('_Relations__', '')))
            getter_method = getattr(self, 'get_' + key.replace('_Relations__', ''))
#             log.debug('getter_method: ' + str(getter_method))
            items += list(getter_method())
        return items
 
 
    accomplished_by = property(get_accomplished_by, set_accomplished_by, None, None)
    accomplished_from = property(get_accomplished_from, set_accomplished_from, None, None)
    extracted_by = property(get_extracted_by, set_extracted_by, None, None)
    extracted_from = property(get_extracted_from, set_extracted_from, None, None)
    grouped_by = property(get_grouped_by, set_grouped_by, None, None)
    grouped_from = property(get_grouped_from, set_grouped_from, None, None)
    invented_by = property(get_invented_by, set_invented_by, None, None)
    invented_from = property(get_invented_from, set_invented_from, None, None)
    refined_by = property(get_refined_by, set_refined_by, None, None)
    refined_from = property(get_refined_from, set_refined_from, None, None)
    solved_by = property(get_solved_by, set_solved_by, None, None)
    solved_from = property(get_solved_from, set_solved_from, None, None)
    specified_by = property(get_specified_by, set_specified_by, None, None)
    specified_from = property(get_specified_from, set_specified_from, None, None)
    verified_by = property(get_verified_by, set_verified_by, None, None)
    verified_from = property(get_verified_from, set_verified_from, None, None)
    existing_relations = property(get_existing_relations, None, None, None)


    def get_related_items_by_relation_name(self, relation_name):
        getter_method = getattr(self, 'get_' + relation_name)
        return getter_method()


    def __str__(self):
        return_string = 'Relations ['
        for related_item in self.get_existing_relations():
            return_string += str(related_item) + ', '
        
        return_string += ']'
        return return_string
 
 
    def __config__(self):
        config = ConfigParser()
         
        config.add_section(self.SECTION_NAME)
        config.set(self.SECTION_NAME,'accomplished_by', str(self.get_accomplished_by) if hasattr(self,'accomplished_by') else'')
        config.set(self.SECTION_NAME,'accomplished_from', str(self.get_accomplished_from) if hasattr(self,'accomplished_from') else'')
        config.set(self.SECTION_NAME,'extracted_by', str(self.get_extracted_by) if hasattr(self,'extracted_by') else'')
        config.set(self.SECTION_NAME,'extracted_from', str(self.get_extracted_from) if hasattr(self,'extracted_from') else'')
        config.set(self.SECTION_NAME,'grouped_by', str(self.get_grouped_by) if hasattr(self,'grouped_by') else'')
        config.set(self.SECTION_NAME,'grouped_from', str(self.get_grouped_from) if hasattr(self,'grouped_from') else'')
        config.set(self.SECTION_NAME,'invented_by', str(self.get_invented_by) if hasattr(self,'invented_by') else'')
        config.set(self.SECTION_NAME,'invented_from', str(self.get_invented_from) if hasattr(self,'invented_from') else'')
        config.set(self.SECTION_NAME,'refined_by', str(self.get_refined_by) if hasattr(self,'refined_by') else'')
        config.set(self.SECTION_NAME,'refined_from', str(self.get_refined_from) if hasattr(self,'refined_from') else'')
        config.set(self.SECTION_NAME,'solved_by', str(self.get_solved_by) if hasattr(self,'solved_by') else'')
        config.set(self.SECTION_NAME,'solved_from', str(self.get_solved_from) if hasattr(self,'solved_from') else'')
        config.set(self.SECTION_NAME,'specified_by', str(self.get_specified_by) if hasattr(self,'specified_by') else'')
        config.set(self.SECTION_NAME,'specified_from', str(self.get_specified_from) if hasattr(self,'specified_from') else'')
        config.set(self.SECTION_NAME,'verified_by', str(self.get_verified_by) if hasattr(self,'verified_by') else'')
        config.set(self.SECTION_NAME,'verified_from', str(self.get_verified_from) if hasattr(self,'verified_from') else'')
        return config       
