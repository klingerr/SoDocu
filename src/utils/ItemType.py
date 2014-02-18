'''
Created on 14.02.2014

@author: RKlinger
'''

class ItemType(object):
    '''
    Represents a valid item type in sodoku.
    '''

    def __init__(self, name, path, menu_position):
        self.__name = name
        self.__path = path
        self.__menu_position = menu_position


    def get_name(self):
        return self.__name


    def get_path(self):
        return self.__path


    def get_menu_position(self):
        return self.__menu_position


    name = property(get_name, None, None, None)
    path = property(get_path, None, None, None)
    menu_position = property(get_menu_position, None, None, None)


    def __str__(self):
        return 'name: ' + self.get_name() + ', path: ' + self.get_path() + ''


    def __repr__(self):
#         return '<ItemType(%s)>' % self.s
#         return "%s(%r)" % (self.__class__, self.__dict__)
        return "%r" % (self.__dict__)
