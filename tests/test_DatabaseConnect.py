import os
import tempfile
import unittest

from ClutterBaseCore import Connection
from ClutterBaseCore.Functions import create_new_database


class TestDatabaseConnect(unittest.TestCase):
    """create a temporary directory for all test to store data"""

    @classmethod
    def setUpClass(cls):
        cls.dir_name = tempfile.TemporaryDirectory()
        print(cls.dir_name)

    """cleanup the temporary directory"""

    @classmethod
    def tearDownClass(cls):
        cls.dir_name.cleanup()

    def test_create(self):
        # create an empty clutter base
        db_name = f"{self.dir_name.name}/test.db"
        self.assertTrue(create_new_database(db_name))
        # this should fail permission denied
        self.assertFalse(create_new_database("/usr/libtest.db"))

    def test_connect(self):
        self.assertTrue(create_new_database(f"{self.dir_name.name}/connect_test.db"))

        with Connection.ClutterBaseConnection(
            f"{self.dir_name.name}/connect_test.db"
        ) as connection:
            self.assertTrue(connection != None)

        db = Connection.ClutterBaseConnection(f"{self.dir_name.name}/connect_test.db")
        db.open()
        self.assertTrue(db.connection != None)
        db.close()

    def test_add_item(self):
        self.assertTrue(create_new_database("connect_test.db"))
        with Connection.ClutterBaseConnection("connect_test.db") as connection:
            self.assertTrue(connection != None)
            connection.add_item(
                "Whisk",
                "A whisk",
                "testdata/Whisk/whisk.obj",
                "testdata/Whisk/WhiskTop.png",
                "testdata/Whisk/WhiskPersp.png",
                "testdata/Whisk/WhiskSide.png",
                "testdata/Whisk/WhiskFront.png",
            )
