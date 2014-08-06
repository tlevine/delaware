import os
import json
import csv
import sys

from delaware_reader.args import parser
import delaware_reader.parse as parse

def main():
    sink = getsink(sys.stdout)
    requestdir = parser.parse_args().requestdir
    for filename, salted_installation, datetime in files(requestdir):
        with open(filename, 'r') as fp:
            data = json.load(fp)
        try:
            result = parse.parse(data)
        except:
            sys.stderr.write('Error at %s\n' % filename)
        else:
            if result != None:
                sink.writerow(result)

def files(requestdir):
    for salted_installation in os.listdir(requestdir):
        for datetime in os.listdir(os.path.join(requestdir, salted_installation)):
            filename = os.path.join(requestdir, salted_installation, datetime)
            yield filename, salted_installation, datetime

def getsink(fp):
    fieldnames = [
        'datetime_received',
    ] + list(parse.KEY_MAPPING.values())
    writer = csv.DictWriter(fp, fieldnames = fieldnames)
    writer.writeheader()
    return writer
