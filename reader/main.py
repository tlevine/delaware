import sys
from args import parser

def main():
    sink = getsink()
    requestdir = parser.parse_args().request_directory
    for filename, salted_installation, datetime in files(requestdir):
        with open(filename, 'r') as fp:
            data = json.load(fp)
        result = parse(data)
        if result != None:
            result['datetime'] = datetime
            sink.writerow(result)

def files(requestdir):
    for salted_installation in os.listdir(requestdir):
        for datetime in os.listdir(os.path.join(requestdir, salted_installation)):
            filename = os.path.join(requestdir, salted_installation, datetime)
            yield filename, salted_installation, datetime

def sink(fp = sys.stdout):
    fieldnames = [
        'datetime',
        'file_number',
        # ...
    ]
    csv.DictWriter(fp, fieldnames = fieldnames)
