from shutil import rmtree
from unittest import TestCase
from tempfile import tempdir

from db import Dadabase, TIMESPAN, LIMIT

TMP = os.path.join(tempdir, 'test-dadabase')

class TestDadabase(TestCase):
    def setUp(self):
        if os.path.exists(TMP):
            rmtree(TMP)
        os.makedir(TMP)
        self.dburl = 'sqlite:///:memory:'
        self.db = Dadabase(self, self.dburl, TMP)

    def tearDown(self):
        rmtree(TMP)

    def test_init(self):
        n.assert_set_equal(set(self.db.file_numbers.values()), {0})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':8})
        self.db._init_cache()
        n.assert_set_equal(set(self.db.file_numbers.values()), {2,1,0})

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
        ip_address = '1.2.3.4'
        now = datetime.datetime(2014, 6, 24)

        for _ in range(LIMIT - 2):
            self.db['requests'].insert({'datetime': now, 'ip_address': ip_address}
        n.assert_true(self.under_limit(ip_address, now = now))

        for _ in range(4):
            self.db['requests'].insert({'datetime': now, 'ip_address': ip_address}
        n.assert_false(self.under_limit(ip_address, now = now))

        n.assert_true(self.under_limit(ip_address, now = now - (1.2 * TIMESPAN)))

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
