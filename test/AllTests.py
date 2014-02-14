'''
Created on 11.02.2014

@author: RKlinger
'''
import unittest
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader.discover( '.' )
    test_runner = unittest.TextTestRunner(verbosity=3)
    test_runner.run( test_loader ) 
