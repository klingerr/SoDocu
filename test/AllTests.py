'''
Created on 11.02.2014

@author: RKlinger
'''
import nose
# import unittest
# import unittest2
# import logging.config
 
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


if __name__ == '__main__':
    nose.config.Config().configureLogging()
    result = nose.run()
#     print result
    
#     test_loader = unittest.defaultTestLoader.discover( '.' )
#     print test_loader
#     test_runner = unittest.TextTestRunner(verbosity=3)
#     print test_runner
#     test_runner.run( test_loader ) 

#     loader = unittest2.TestLoader()
#     tests = loader.discover('.')
#     testRunner = unittest2.runner.TextTestRunner()
#     testRunner.run(tests)
