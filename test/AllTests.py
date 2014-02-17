'''
run at console:
nosetests --with-coverage --cover-package=../src/ --cover-inclusive --cover-html --cover-erase

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
