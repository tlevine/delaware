import re
import json
import os
import random
import datetime
from collections import Counter

import dataset

TIMESPAN = datetime.timedelta(days = 1)
LIMIT = 5e5 # a bit high, but we do need to make sixteen million requests, and I don't want it to take forever
GLOBAL_LIMIT = 1e7 # Maximum of a million requests per day---a decent Apache 2.2.3 server should be able to handle this, right?

class Dadabase:
    def __init__(self, dburl, requestdir, highest_file_number = 8e6):
        self.highest_file_number = int(highest_file_number)
        self.disk = dataset.connect(dburl)
        self.requestdir = requestdir

        if not os.path.isdir(requestdir):
            os.makedirs(requestdir)
        self.disk.query('CREATE TABLE IF NOT EXISTS file_numbers ( file_number INTEGER );')
        self.disk.query('CREATE TABLE IF NOT EXISTS requests ( datetime INTEGER, ip_address TEXT );')

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

    def under_limit(self, ip_address, now = None, limit = LIMIT, global_limit = GLOBAL_LIMIT):
        'Return True if we are under the limit and it is safe to query the website.'
        if now == None:
            now = datetime.datetime.now()
        if not isinstance(ip_address, str):
            raise TypeError('ip_address must be str.')
        params = {
            'now': int((now - TIMESPAN).timestamp()),
            'ip_address': ip_address,
            'ip_address_limit': limit,
            'global_limit': global_limit,
        }
        sql = '''
        SELECT
      ( SELECT count(*) FROM requests WHERE datetime > %(now)d AND ip_address = "%(ip_address)s" ) < %(ip_address_limit)d,
      ( SELECT count(*) FROM requests WHERE datetime > %(now)d ) < %(global_limit)d;
        ''' % params
        result = self.disk.query(sql)
        return all(next(result).values())

    def increment_file_number(self, file_number):
        self.disk['file_numbers'].insert({'file_number':file_number})
        self.file_numbers[file_number] += 1

    def save_request(self, request, filename = None, now = None):
        body = json.loads(request.body.read().decode('utf-8'))

        if now == None:
            now = datetime.datetime.now()

        if re.match(r'^[0-9a-z]{40}$', body['salted_installation']):
            dirname = body['salted_installation']
        else:
            dirname = 'invalid-salted_installation'

        if filename == None:
            try:
                os.makedirs(os.path.join(self.requestdir, dirname))
            except FileExistsError:
                pass
            path = os.path.join(self.requestdir, dirname, now.isoformat())
        else:
            path = filename

        data = {
            'date': now.isoformat(),
            'ip_address': request.remote_addr[0],
            'method': request.method,
            'url': request.url,
            'body': body,
        }
        with open(path, 'a') as fp:
            fp.write(json.dumps(data) + '\n')
        d = int(now.timestamp())
        self.disk['requests'].insert({'datetime': d, 'ip_address': data['ip_address']})
        if 'before_address' in data['body'] and data['body']['before_address'] != data['ip_address']:
            self.disk['requests'].insert({'datetime': d, 'ip_address': data['body']['before_address']})

