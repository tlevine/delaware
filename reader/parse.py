from collections import OrderedDict
import lxml.html

KEY_MAPPING =  OrderedDict([
    ('File Number:', 'file_number'),
    ('Incorporation Date / Formation Date:', 'entity_date'),
    ('Entity Name:', 'entity_name'),
    ('Entity Kind:', 'entity_kind'),
    ('Entity Type:', 'entity_type'),
    ('Residency:', 'residency'),
    ('State:', 'state'),
    ('Name:', 'name'),
    ('Address:', 'address'),
    ('City:', 'city'),
    ('County:', 'country'),
    ('State:', 'state'),
    ('Postal Code:', 'postcode'),
    ('Phone:', 'phone'),
])

def text_contents(nodes):
    return (node.text_content() for node in nodes)

def parse(data):
    html = lxml.html.fromstring(text(data))

    # Get the appropriate fields.
    key_tds = html.xpath('//td[@bgcolor="#d7d7d7"]')
    value_tds = [td.xpath('following-sibling::td')[0] for td in key_tds]

    # Pair them nicely
    texts = zip(text_contents(key_tds), text_contents(value_tds))
    result = OrderedDict((KEY_MAPPING[key], value) for (key, value) in texts)

    # Clean them up a bit
    result['entity_date'] = result['entity_date'].replace('(mm/dd/yyyy)', '')

    # Add fields from outside the HTML
    result['datetime_received'] = data['date']
    result['username'] = data['body']['username']

    return result

def is_entity_detail(data):
    return 'FieldDesc.jsp' in text(data)

def text(data):
    'Return the text of the response from Delaware.'
    return data['body']['response']['text']
