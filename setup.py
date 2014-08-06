from functools import partial
import os
from distutils.core import setup

from delaware_shared.version import VERSION

requirements = [
    'randua>=0.0.1',
    'requests>=2.3.0',
    'picklecache>=0.0.4'
]
extras = {
    'manager': ['dataset>=0.5.2', 'bottle>=0.12.7', 'cherrypy>=3.5.0'],
    'reader': ['lxml>=3.3.5'],
}

setup(
    name = "delaware",
    version = VERSION,

    author = "Thomas Levine",
    author_email = "_@thomaslevine.com",
    description = "Get company registration data for the State of Delaware.",
    license = "AGPL",
    url = "https://github.com/tlevine/delaware",

    install_requires = requirements,
    extras_require = extras,
    tests_require = ['nose'],

    packages = ['delaware_' + suffix for suffix in ['shared', 'manager','worker','reader']],
    data_files = [('certificates', ['certificates/delaware.dada.pink.crt'])],
    scripts = [os.path.join('bin',script) for script in ['delaware', 'delemanager','deleworker','delereader']],

    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

