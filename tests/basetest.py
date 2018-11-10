from unittest import TestCase
from youcomment.config import CHECKED_FILE
import os

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
    