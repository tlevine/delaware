import os
import datetime
from collections import Counter

import dataset

TIMESPAN = datetime.timedelta(days = 1)
LIMIT = 100

class Dadabase:
    def __init__(self, dburl, requestdir, highest_file_number = 8e6):
        self.highest_file_number = int(highest_file_number)
        self.disk = dataset.connect(dburl)
        if not os.path.isdir(requestdir):
            os.makedirs(requestdir)
        self.disk.query('CREATE TABLE IF NOT EXISTS file_numbers ( file_number INTEGER );')
        self.disk.query('CREATE TABLE IF NOT EXISTS requests ( datetime DATETIME, ip_address TEXT );')
        self._init_cache()

    def _init_cache(self):
        '(Re)initialize the cache.'

        # This takes a long time, unsurprisingly
        self.file_numbers = {file_number:0 for file_number in range(1, self.highest_file_number)}

        sql = 'SELECT file_number, count(*) FROM file_numbers GROUP BY file_number'
        for row in self.disk.query(sql):
            self.file_numbers[row['file_number']] = row['count(*)']

    def file_number(self):
        '''
        Choose a file number to download.
        It is randomly chosen among the file numbers with the fewest responses.
        '''
        lowest = min(self.file_numbers.values())
        population = [file_number for file_number, count in self.file_numbers.items() if count == lowest]
        if len(population) > 0:
            return random.choice(population)
        else:
            return self.random_file_number()

    def under_limit(self, ip_address, now = None):
        'Return True if we are under the limit and it is safe to query the website.'
        if now == None:
            now = datetime.date.today()
        params = ((now - TIMESPAN).isoformat(), ip_address)
        result = self.disk.query('SELECT count(*) FROM requests WHERE datetime > "%s" AND ip_address = "%s"' % params)
        return next(result)['count(*)'] < LIMIT

    def increment_file_number(self, file_number):
        self.disk.insert({'file_number':file_number})
        self.file_numbers['file_number'] += 1

    def save_request(self, request, filename = datetime.date.today().isoformat(), now = None):
        data = {
            'date': datetime.datetime.today().ctime() if now == None else now,
            'ip_address': request.remote_addr,
            'method': request.method,
            'url': request.url,
            'data': request.data,
        }
        with open(os.path.join(self.requestdir, filename, 'a')) as fp:
            fp.write(json.dumps(data) + '\n')
