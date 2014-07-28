import os
import datetime
from collections import Counter
import datetime

import dataset

TIMESPAN = 10
LIMIT = 100

class Dadabase:
    def __init__(self, dburl, requestdir):
        self.disk = dataset.connect(dburl)
        if not os.path.isdir(requestdir):
            os.makedirs(requestdir)
        self.file_numbers = {file_number:0 for file_number in range(1, 8 * 10**6)}
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

    def under_limit(self, ip_address):
        'Return True if we are under the limit and it is safe to query the website.'
        params = [datetime.date.today() - TIMESPAN, ip_address]
        result = db.query('SELECT count(*) FROM requests WHERE datetime > ? AND ip_address > ?', params)
        return next(result['count(*)']) < LIMIT

    def increment_file_number(self, file_number):
        self.disk.insert({'file_number':file_number})
        self.file_numbers['file_number'] += 1

    def save_request(self, request, filename = datetime.date.today().isoformat()):
        data = {
            'date': datetime.datetime.today().ctime(),
            'ip_address', request.remote_addr,
            'method': request.method,
            'url': request.url,
            'data': request.data,
        }
        with open(os.path.join(self.requestdir, filename, 'a') as fp:
            fp.write(json.dumps(data) + '\n')