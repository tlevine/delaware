import sys
try:
    # Python 3
    from configparser import ConfigParser
except ImportError:
    # Python 2
    from ConfigParser import ConfigParser
    input = raw_input
import os
import uuid
from getpass import getuser

SECTION = 'worker'
DIRECTORY = os.path.expanduser(os.path.join('~', '.delaware'))
CONFIG = os.path.join(DIRECTORY, 'config')

def params():
    from_config = read_config_params(CONFIG)
    if from_config == None:
        manager_address = 'https://delaware.dada.pink'
        username = prompt_params()
        installation = installation_id()
        if not os.path.exists(DIRECTORY):
            os.makedirs(DIRECTORY)

        ca_bundle_file = os.path.join(sys.prefix, 'certificates', 'delaware.dada.pink.crt')
        write_config_params(ca_bundle_file, manager_address, username, installation, CONFIG)
    else:
        ca_bundle_file, manager_address, username, installation = from_config

    return ca_bundle_file, manager_address, username, installation

def installation_id():
    return str(uuid.uuid4())

def prompt_params():
    question = '''
You are running a program that searches for data on companies registered
in the State of Deleware.

==============================
What it does
==============================
It contacts Tom's (http://dada.pink) server for directions, queries the
General Information Name Search directions, queries the General Information
Name Search (https://delecorp.delaware.gov/tin/GINameSearch.jsp) accordingly,
and sends the results to Tom's server. This will all happen without any
effort from you as long as you keep the program running.

==============================
Licensing
==============================
Your computer will collect data and send them to Tom, and Tom is going to
redistribute the data under either the Open Data Commons Open Database License
(http://opendatacommons.org/licenses/odbl/) or a public domain license, such
as CC0 (http://creativecommons.org/publicdomain/zero/1.0/).

==============================
How Delaware might react
==============================
Tom would like you to know that Delaware might get annoyed at you for running
this program. Tom heard from other people that this website bans IP addresses
after they have made a few hundred requests per day. He is skeptical that the
limit is actually this low, and Delaware told him that no such limit exists,
but the point is that you might get banned from the website.

Also, he has heard that Delaware sends scary letters to people who use this
website, so they might send you one.

==============================
Why access the data this way
==============================
It would be nice if there were a better way to get these data. Tom heard that
the Division of Corporations is exempt from freedom of information law, but
it might be worth looking further into that avenue.

It may be that some companies (http://corp.delaware.gov/directwebvend.shtml)
can sell you the data, but Tom isn't sure; he contacted the Delaware
Division of Corporations for information about this, and the response
wasn't helpful. He's working on a freedom of information request about
these vendors.

If you have any ideas on other ways of getting the company registration
information, Tom would love to know.

==============================
Is all this okay?
==============================
Is it okay that Tom is going to release the data and that Delaware might
get annoyed at you?

If so, type "yes"; if not, hit ctrl+c to exit the program.

'''
    wrong_answer = '''
You need to type "yes" to run the software. If you are not okay with how
Delaware might react or how Tom would redistribute the data, hit ctrl+c.

'''
    if input(question) != 'yes':
        while input(wrong_answer) != 'yes':
            pass

    default_username = 'Anonymous'
    username = input('Username (Leave blank for "%s".): ' % default_username)
    if username == '':
        username = default_username

    return username

def read_config_params(filename):
    c = ConfigParser()
    if c.read(filename) == []:
        return

    ca_bundle_file = c.get(SECTION, 'ca_bundle_file')
    manager_address = c.get(SECTION, 'manager_address')
    username = c.get(SECTION, 'username')
    installation = c.get(SECTION, 'installation')

    if ca_bundle_file != None and manager_address != None and username != None and installation != None:
        return ca_bundle_file, manager_address, username, installation

def write_config_params(ca_bundle_file, manager_address, username, installation, filename):
    c = ConfigParser()
    c.add_section(SECTION)
    c.set(SECTION, 'ca_bundle_file', value = ca_bundle_file)
    c.set(SECTION, 'manager_address', value = manager_address)
    c.set(SECTION, 'username', value = username)
    c.set(SECTION, 'installation', value = installation)
    with open(filename, 'w') as fp:
        c.write(fp)
