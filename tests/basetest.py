from unittest import TestCase
import youcomment.database as db
import warnings


class BaseTest(TestCase):

    def setUp(self):
        db.wipe_db()
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        super(BaseTest, self).setUp()

    def tearDown(self):
        db.wipe_db()
        super(BaseTest, self).tearDown()
