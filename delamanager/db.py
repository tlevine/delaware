from collections import Counter

import dataset

class Dadabase:
    def __init__(self, url):
        self.disk = dataset.connect(url)
        self.file_numbers = {file_number:0 for file_number in range(1, 8 * 10**6)}
        sql = 'SELECT file_number, count(*) FROM file_numbers GROUP BY file_number'
        for row in self.disk.query(sql):
            self.file_numbers[row['file_number']] = row['count(*)']
    def query(self, *args, **kwargs):
        return self.disk.query(*args, **kwargs)
    def increment_file_number(self, file_number):
        self.disk.insert({'file_number':file_number})
        self.file_numbers['file_number'] += 1

db = Dadabase('sqlite:////home/tlevine/foo.db')

    blah = db.query('SELECT count(*) FROM requests WHERE datetime > ? AND ip_address > ?', params)
