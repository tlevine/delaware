import sys

def directions():
    while True:
        file_number_str = input('File number (for example, "0833421"): ')
        try:
            file_number = int(file_number_str)
        except ValueError:
            sys.stdout.write('\r')
        else:
            break
    return file_number, 'localhost'

def respond(before_address, file_number, finished, response):
    finished_str = 'Finished' if finished else 'Not finished'
    sys.stdout.write('%s with %d after %s\n' % (finished_str, file_number, response.url))
