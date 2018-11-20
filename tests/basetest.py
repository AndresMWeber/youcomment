from unittest import TestCase
from youcomment.database import wipe_db


class BaseTest(TestCase):

    def setUp(self):
        wipe_db()
        super(BaseTest, self).setUp()

    def tearDown(self):
        wipe_db()
        super(BaseTest, self).tearDown()
