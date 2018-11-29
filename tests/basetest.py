from unittest import TestCase
import youcomment.database as db
import warnings
import sys


class BaseTest(TestCase):

    def setUp(self):
        db.wipe_db()
        if sys.version_info.major >= 3:
            warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        super(BaseTest, self).setUp()

    def tearDown(self):
        db.wipe_db()
        super(BaseTest, self).tearDown()
