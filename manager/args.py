import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--database', default = 'sqlite:////home/delaware/delaware.db',
    help = 'SQLAlchemy-style relational database URL')
parser.add_argument('--request-directory', default = '/home/delaware/requests',
    help = 'Directory wherein data from workers will be stored')
parser.add_argument('--logfile', default = '/home/delaware/delaware.log',
    help = 'File to which a summary of each request will be written')
