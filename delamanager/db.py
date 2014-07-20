from collections import Counter
import datetime

import dataset

TIMESPAN = 10
LIMIT = 100

class Dadabase:
    def __init__(self, url):
        self.disk = dataset.connect(url)
        self.file_numbers = {file_number:0 for file_number in range(1, 8 * 10**6)}
        sql = 'SELECT file_number, count(*) FROM file_numbers GROUP BY file_number'
        for row in self.disk.query(sql):
            self.file_numbers[row['file_number']] = row['count(*)']
    def under_limit(self, ip_address):
        'Return True if we are under the limit and it is safe to query the website.'
        params = [datetime.date.today() - TIMESPAN, ip_address]
        result = db.query('SELECT count(*) FROM requests WHERE datetime > ? AND ip_address > ?', params)
        return next(result['count(*)']) < LIMIT

    def increment_file_number(self, file_number):
        self.disk.insert({'file_number':file_number})
        self.file_numbers['file_number'] += 1

db = Dadabase('sqlite:////home/tlevine/foo.db')

