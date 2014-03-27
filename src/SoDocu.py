'''
Created on 03.02.2014

@author: RKlinger
'''

import json
import logging.config

from src.persistence.DirectoryWalker import DirectoryWalker
from src.persistence.FileHandler import FileHandler, read_file
from src.utils.Config import Config
from src.utils.Glossary import Glossary
from src.utils.ItemType import ItemType
from src.utils.Utils import create_item, get_setter_method
from src.view.Gui import create_gui


log = logging.getLogger('SoDocu')
# console logger
# log.addHandler(logging.StreamHandler())
# log.setLevel(logging.DEBUG)


class SoDocu(object):
    '''
    This is the start point of SoDocu.
    '''

    def __init__(self, sodocu_config):
        '''
        Reads all items into memory.
        '''
        self.__config = sodocu_config
        self.__fileHandler = FileHandler(self.__config)
        self.__path = self.__config.get_sodocu_path()
        self.__glossary = Glossary(self.__path)
        # dictionary/map with item_type_name as key and set of items as value
        self.__items = self.initialize_items_dictionary()
        self.read_all_items(self.__config)


    def initialize_items_dictionary(self):
        '''
        Creates a dictionary with one key for each item type and an empty set as value.
        '''
        items = dict()
        for item_type_name in self.get_config().get_item_types_as_string():
            items[item_type_name] = set()
        return items 


    def get_glossary(self):
        return self.__glossary


    def get_config(self):
        return self.__config


    def get_path(self):
        return self.__path


    def get_file_handler(self):
        return self.__fileHandler


    def get_items(self):
        return self.__items


    def get_items_by_type(self, item_type):
        log.debug('get_items_by_type(' + str(item_type) + ')')
        try:
            return self.__items[item_type.get_name()]
        except KeyError:
            log.info('There are no items of type <' + str(item_type) + '>')
        return None


    def get_items_by_type_name_as_json(self, item_type_name):
        item_list = []
        for item in self.get_items_by_type(ItemType(item_type_name, '')):
            item_list.append({'label':item.name, 'id':item.id})
        log.debug('item_list: ' + str(item_list))
        return json.dumps(item_list, indent=2)


    def get_all_items_as_json(self):
        '''
        Returns all items for D3js as JSON data in form: 
           {"nodes":[{"node":0,"name":"node0"}, ... ], 
            "links":[{"source":0,"target":2,"value":2}, ... ]}
        '''
        nodes = []
        links = []
        graph = {"nodes":nodes, "links":links}
        i = 0
        
        # fill list of nodes separatly because of identifying index number source and targets for links later
        for item_type in self.get_config().get_item_types():
            for item in self.get_items_by_type(item_type):
                nodes.append({"node":i, "name":item.id, "img_url":item.item_type.img_url})
                i = i + 1

        log.debug('nodes: ' + str(nodes))

        # filling list of links between nodes with by-relations
        for node in nodes:
            item = self.get_item_by_id(ItemType(node['name'].split('-')[0], '') , node['name'])
            log.debug('item: ' + str(item))
            for key in item.item_type.valid_relations.keys():
                if key.endswith('_by'):
                    for related_item_id in item.relations.get_related_items_by_relation_name(key):
                        if next((x for x in nodes if x['name'] == related_item_id), None) != None:
                            links.append({'source':next((x for x in nodes if x['name'] == item.get_id()), None)['node'], 
                                          'target':next((x for x in nodes if x['name'] == related_item_id), None)['node'],
                                          'name':key})
                
        log.debug('graph: ' + str(graph))
        return json.dumps(graph, indent=2)


    def add_item(self, item):
        log.debug('add_item(' + str(item) + ')')
        item_type = item.get_item_type()
        items = self.get_items_by_type(item_type)
#         if items is None:
#             self.__items[item_type.get_name()] = set()
#             items = self.get_items_by_type(item_type)
        items.add(item)

        
    glossary = property(get_glossary, None, None, None)
    path = property(get_path, None, None, None)
    fileHandler = property(get_file_handler, None, None, None)
    items = property(get_items_by_type, None, None, None)
    config = property(get_config, None, None, None)

        
    def read_all_items(self, sodocu_config):
        directoryWalker = DirectoryWalker(self.get_path())
        log.debug('directoryWalker.get_filenames(): ' + str(directoryWalker.get_filenames()))
        for filename in directoryWalker.get_filenames():
            item_config = read_file(filename)
            item = create_item(sodocu_config, item_config, filename)
            self.add_item(item)


    def set_attribut(self, item, attribute, value):
        log.debug('set_attribut: ' + str(item) + ', ' + attribute + ', ' + value + ')')
        setter_method = get_setter_method(item, attribute)
        log.debug('setter_method: ' + str(setter_method))
        setter_method(value)


    def get_item_by_id(self, item_type, identifier):
        log.debug('get_item_by_id(' + str(item_type) + ', ' + str(identifier) + ')') 
        items = self.get_items_by_type(item_type)
        if items is None:
            log.debug('return: ' + str(None)) 
            return None
        
        for item in items:
            if item.get_id() == identifier:
                log.debug('return item: ' + str(item)) 
                return item


    def save_item(self, item):
        log.info('save_item(' + str(item) + ')')
        return self.get_file_handler().update_file(item)
        
        
    def delete_item(self, item):
        log.info('delete_item(' + str(item) + ')')
        if self.get_file_handler().delete_file(item):
            return self.remove_item(item)
        return False
        

    def remove_item(self, item):
        '''
        Removes the given item from set of item_types
        '''
        items = self.get_items_by_type(item.get_item_type())
        if items is None:
            return False
        
        try:
            items.remove(item)
            return True
        except KeyError:
            log.info('There is no item <' + item.get_id() + '> to remove!')
        return False


    def search(self, search_string):
        results = set()
        for key in self.get_items().keys():
            item_type = self.get_config().get_item_type_by_name(key)
            for value in self.get_items_by_type(item_type):
                if value.contains_text(search_string):
                    results.add(value)
        return results


    def get_glossary_entries_as_json(self):
        return self.get_glossary().get_entries_as_json()
        

    def get_glossary_entries(self):
        return self.get_glossary().get_entries()
        

    def get_relations_by_item(self, item):
        log.debug('get_relations_by_item(' + str(item) + ')')
        relations = dict()
        
        for valid_relation_type in item.item_type.valid_relations.keys(): 
            log.debug('valid_relation_type: ' + valid_relation_type)
            items = []
            for item_id in item.relations.get_related_items_by_relation_name(valid_relation_type):
                log.debug('item_id: ' + item_id)
                if item_id and item_id != '':
                    item_type = self.config.get_item_type_by_name(item_id.split('-')[0].strip())
                    related_item = self.get_item_by_id(item_type, item_id.strip())
                    log.debug('related_item: ' + str(related_item))
                    if related_item != None:
                        items += [related_item]
                    log.debug('items: ' + str(items))
            relations[valid_relation_type] = items
        return relations
    

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
    log.info('starting ...')
    config = Config()
    sodoku = SoDocu(config)
    gui = create_gui(sodoku)
    
    from werkzeug.serving import run_simple
    run_simple('127.0.0.1', 8000, gui, use_debugger=True, use_reloader=True)
