import argparse

parser = argparse.ArgumentParser()
parser.add_argument(metavar = 'requests directory', dest = 'requestdir',
    default = '/home/delaware/requests',
    help = 'Directory wherein data from workers will be stored')
