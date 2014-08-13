import sys
try:
    import xmlrpclib
except ImportError:
    import xmlrpc.client as xmlrpclib

VERSION = '0.0.4'

message = '''
Updates to the delaware scraper are available! 
You are running version %s, and the most recent
version is %s. If you have pip, you can upgrade
like so.

    sudo pip install --upgrade deleware

If you don't have pip, follow the directions at
http://dada.pink/dada/XXX to upgrade.
'''

def check_version():
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    releases = client.package_releases('delaware')
    if len(releases) > 0 and releases[0] > VERSION:
        newest = releases[0]
        sys.stderr.write(message % (VERSION, newest))
