from unittest import TestCase
from tempfile import tempdir

from db import Dadabase

TMP = os.path.join(tempdir, 'test-dadabase')

class TestDadabase(TestCase):
    def setUp(self):
        if os.path.exists(TMP):
            pass # remove it
        os.makedir(TMP)
        self.dburl = 'sqlite:///' + os.path.join(TMP, 'dadabase.db')
        self.requestdir = os.path.join(TMP, 'requests')
        self.db = Dadabase(self, self.dburl, self.requestdir)

    def test_init(self):
        # do something to dburl and requestdir
        db = Dadabase(self, self.dburl, self.requestdir)
        n.assert_set_equal(set(db.file_numbers.values()), {0})

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
       #result = db.query('SELECT count(*) FROM requests WHERE datetime > ? AND ip_address > ?', params)
       #return next(result['count(*)']) < LIMIT

    def test_increment_file_number(self):
        file_number = 82342

        self.db.disk['file_numbers'] # and select stuff
        self.db.file_numbers[file_number]

        self.db.increment_file_number(file_number)

        self.db.disk['file_numbers'] # and select stuff
        self.db.file_numbers[file_number]

    def test_save_request(self):
        pass
