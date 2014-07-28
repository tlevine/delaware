from unittest import TestCase

from db import Dadabase

class TestDadabase(TestCase):
    def setUp(self):
        self.db = Dadabase(self, dburl, requestdir):

    def test_init(self):
        pass
    def test_file_number(self):
        'The file number should be among those with the lowest counts.'
        self.db.file_numbers = {
            1: 4,
            9: 2,
            2: 3,
            12: 2,
        }
        n.assert_in({9,12}, self.db.file_number())

    def test_under_limit(self):
        pass

    def test_increment_file_number(self):
        file_number = 82342

        self.db.disk['file_numbers'] # and select stuff
        self.db.file_numbers[file_number]

        self.db.increment_file_number(file_number)

        self.db.disk['file_numbers'] # and select stuff
        self.db.file_numbers[file_number]

    def test_save_request(self):
        pass
