from unittest import TestCase
import youcomment.conf as conf
import os

CHECKED_FILE = conf.CHECKED_FILE

class BaseTest(TestCase):
    original_data = ''

    @classmethod
    def setUpClass(cls):
        if not os.path.exists(CHECKED_FILE):
            with open(CHECKED_FILE, 'w') as f:
                f.write('')
        else:
            with open(CHECKED_FILE, 'r') as f:
                cls.original_data = f.read()
        
    @classmethod
    def tearDownClass(cls):
        with open(CHECKED_FILE, 'w') as f:
            f.write(cls.original_data)
    
    def setUp(self):
        with open(CHECKED_FILE, 'w'):
            pass

    def tearDown(self):
        with open(CHECKED_FILE, 'w'):
            pass
    