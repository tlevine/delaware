
import compose as c

def home():
    return c.home(datetime.datetime.now(), user_agent = get_user_agent())

def search(home_response, firm_file_number):
    user_agent = home_response.request.headers['User-Agent']
    cookie = home_response.request.cookies
    return c.search(firm_file_number, user_agent = user_agent, cookie = cookie)

def result(search_response, firm_file_number):
    user_agent = home_response.request.headers['User-Agent']
    cookie = home_response.request.cookies
    return c.result(firm_file_number, user_agent = user_agent, cookie = cookie)
