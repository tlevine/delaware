from io import BytesIO
import json
from shutil import rmtree
import datetime
import os
from unittest import TestCase
from tempfile import NamedTemporaryFile
from collections import namedtuple

import nose.tools as n

from delaware_manager.db import Dadabase, TIMESPAN, LIMIT

TMP = os.path.join('/tmp', 'test-dadabase')

class TestDadabase(TestCase):
    def setUp(self):
        if os.path.exists(TMP):
            rmtree(TMP)
        os.mkdir(TMP)
        self.dburl = 'sqlite:///' + os.path.join(TMP, 'test-dadabase.db')
        self.db = Dadabase(self.dburl, TMP, highest_file_number = 1e3)

    def tearDown(self):
        rmtree(TMP)

    def test_init(self):
        n.assert_set_equal(set(self.db.file_numbers.values()), {0})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':442})
        self.db.disk['file_numbers'].insert({'file_number':8})
        self.db._init_cache()
        n.assert_set_equal(set(self.db.file_numbers.values()), {3,1,0})

    def test_file_number(self):
        'The file number should be among those with the lowest counts.'
        self.db.file_numbers = {
            1: 4,
            9: 2,
            2: 3,
            12: 2,
        }
        n.assert_in(self.db.file_number(), {9,12})

    def test_under_limit(self):
        ip_address = '1.2.3.4'
        now = datetime.datetime(2014, 6, 24)

        for _ in range(LIMIT - 2):
            self.db.disk['requests'].insert({'datetime': now, 'ip_address': ip_address})
        n.assert_true(self.db.under_limit(ip_address, now = now))

        for _ in range(4):
            self.db.disk['requests'].insert({'datetime': now, 'ip_address': ip_address})
        n.assert_false(self.db.under_limit(ip_address, now = now))

        n.assert_true(self.db.under_limit(ip_address, now = now + (1.2 * TIMESPAN)))

    def test_increment_file_number(self):
        file_number = 342

        sql = 'SELECT count(*) FROM file_numbers WHERE file_number = %d'
        disk_before  = next(self.db.disk.query(sql % file_number))['count(*)']
        memory_before= self.db.file_numbers[file_number]

        self.db.increment_file_number(file_number)

        disk_after  = next(self.db.disk.query(sql % file_number))['count(*)']
        memory_after= self.db.file_numbers[file_number]

        n.assert_equal(disk_before + 1, disk_after)
        n.assert_equal(memory_before + 1, memory_after)

    def test_save_request(self):
        ip_address = '12.82.2.9'
        sql = 'SELECT count(*) FROM requests WHERE ip_address = "%s"'

        FakeRequest = namedtuple('Request', ['remote_addr', 'method', 'url', 'body'])
        data = {'salted_installation': 'a' * 40, 'before_address': '1.2.3.4'}
        body = BytesIO(json.dumps(data).encode('utf-8'))
        fakerequest = FakeRequest([ip_address], 'post', '/directions', body)

        now = datetime.datetime(2014,4,3)

        # Record db before.
        before = next(self.db.disk.query(sql % ip_address))['count(*)']
        
        # Do the actual thing.
        tmp = NamedTemporaryFile()
        self.db.save_request(fakerequest, filename = tmp.name, now = now)

        tmp.seek(0)
        one_log_line = json.load(open(tmp.name,'r'))
        expected = {
            'body': data,
            'date': '2014-04-03T00:00:00',
            'ip_address': ip_address,
            'method': 'post',
            'url': '/directions'
        }
        n.assert_dict_equal(one_log_line, expected)

        # Record db after.
        after  = next(self.db.disk.query(sql % ip_address))['count(*)']

        n.assert_equal(before + 1, after)
