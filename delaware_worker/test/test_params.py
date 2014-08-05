import os
import filecmp
import tempfile
from shutil import copyfile

import nose.tools as n

import delaware_worker.params as p

CONFIG = os.path.join('delaware_worker','test','fixtures','config')

def test_installation_id():
    observed = p.installation_id()
    n.assert_equal(len(observed), 36)

def test_read_config_params():
    tmp = tempfile.NamedTemporaryFile()
    copyfile(CONFIG, tmp.name)
    observed = p.read_config_params(tmp.name)
    expected = ('the-ca-bundle-file.crt',
                'https://delaware.dada.pink', 'tlevine',
                '065db5d3-924c-4129-9c93-2360538a4ce5')
    n.assert_tuple_equal(observed, expected)

def test_write_config_params():
    tmp = tempfile.NamedTemporaryFile()
    copyfile(CONFIG, tmp.name)
    p.write_config_params('the-ca-bundle-file.crt',
                          'https://delaware.dada.pink', 'tlevine',
                          '065db5d3-924c-4129-9c93-2360538a4ce5', tmp.name)
    n.assert_true(filecmp.cmp(tmp.name, CONFIG))
