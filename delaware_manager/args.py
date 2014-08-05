import os
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
import argparse

c = ConfigParser()
c.read(os.path.join(os.path.expanduser('~'), '.delaware', 'config'))
if 'manager' in c.sections():
    defaults = dict(c['manager'])
else:
    defaults = {}

parser = argparse.ArgumentParser()
parser.add_argument('--database', default = defaults.get('database', 'sqlite:////home/delaware/delaware.db'),
    help = 'SQLAlchemy-style relational database URL')
parser.add_argument('--request-directory', default = defaults.get('request_directory', '/home/delaware/requests'),
    help = 'Directory wherein data from workers will be stored')
parser.add_argument('--logfile', default = defaults.get('logfile', '/home/delaware/delaware.log'),
    help = 'File to which a summary of each request will be written')
