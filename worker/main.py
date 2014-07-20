
def look(firm_file_numbers):
    'Given a firm file number, try to get the information.'
    home_response = home()
    for firm_file_number in firm_file_numbers:
        search_response = search(home_response, firm_file_number)
        if True:
            result_response = result(search_response, firm_file_number):
    
