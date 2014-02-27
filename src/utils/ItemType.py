'''
Created on 14.02.2014

@author: RKlinger
'''

class ItemType(object):
    '''
    Represents a valid item type in sodoku.
    '''

    def __init__(self, name, path):
        self.__name = name
        self.__path = path
        self.__menu_position = None
        self.__form_template = None
        self.__table_template = None
        self.__valid_relations = dict()


    def get_name(self):
        return self.__name


    def get_path(self):
        return self.__path


    def get_menu_position(self):
        return self.__menu_position


    def get_form_template(self):
        return self.__form_template


    def get_table_template(self):
        return self.__table_template


    def set_menu_position(self, value):
        self.__menu_position = value


    def set_form_template(self, value):
        self.__form_template = value


    def set_table_template(self, value):
        self.__table_template = value


    def get_valid_relations(self):
        return self.__valid_relations


    def add_valid_relation(self, key, value):
        self.__valid_relations[key] = value


    name = property(get_name, None, None, None)
    path = property(get_path, None, None, None)
    menu_position = property(get_menu_position, set_menu_position, None, None)
    form_template = property(get_form_template, set_form_template, None, None)
    table_template = property(get_table_template, set_table_template, None, None)
    valid_relations = property(get_valid_relations, None, None, None)


    def __str__(self):
        return 'ItemType {name: ' + self.get_name() + ', path: ' + self.get_path() + '}'


    def __repr__(self):
#         return '<ItemType(%s)>' % self.s
#         return "%s(%r)" % (self.__class__, self.__dict__)
        return "%r" % (self.__dict__)
