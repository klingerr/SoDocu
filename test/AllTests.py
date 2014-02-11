'''
Created on 11.02.2014

@author: RKlinger
'''
import unittest


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader.discover( '.' )
    test_runner = unittest.TextTestRunner(verbosity=3)
    test_runner.run( test_loader ) 
