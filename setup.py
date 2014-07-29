from functools import partial
import os
from distutils.core import setup

from shared.version import VERSION

requirements = [
    'randua>=0.0.1',
    'requests>=2.3.0',
    'picklecache>=0.0.4'
]
extras = {
    'manager': ['dataset>=0.5.2', 'bottle>=0.12.7', 'cherrypy>=3.5.0'],
    'reader': [],
}

setup(
    name = "delaware",
    version = VERSION,

    author = "Thomas Levine",
    author_email = "_@thomaslevine.com",
    description = "Get company registration data for the State of Delaware.",
    license = "AGPL",
    url = "http://thomaslevine.com"

    install_requires = requirements,
    extras_require = extras,
    tests_require = ['nose'],

    packages = ['manager','worker','reader'],
    scripts = list(map(partial(os.path.join('bin', ['delemanager','deleworker','delereader'])))),

    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
)

