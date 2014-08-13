import nose.tools as n

from delaware_worker.download import headers, _sleep_seconds

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
        headers(None, 'the cookie', 'the referer')

    with n.assert_raises(ValueError):
        headers('the user agent', None, 'the referer')

    with n.assert_raises(ValueError):
        headers('the user agent', 'the cookie', None)

def test_sleep_seconds():
    count = 1000
    histogram = (_sleep_seconds() for _ in range(count))
    n.assert_greater(sum(histogram) / count, 0.9)
