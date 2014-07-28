import nose.tools as n

import worker.download as d

def test_headers():
    expected = {
        'User-Agent': 'the user agent',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    observed = headers('the user agent', None, None)
    n.assert_dict_equal(observed, expected)

    expected.update({
        'Cookie': 'the cookie',
        'Referer': 'the referer',
    })
    observed = headers('the user agent', 'the cookie', 'the referer')
    n.assert_dict_equal(observed, expected)

    with n.assert_raises(ValueError):
        headers('the user agent', 'the cookie', None)

  # What about this one?
  # with n.assert_raises(ValueError):
  #     headers('the user agent', None, 'the referer')
