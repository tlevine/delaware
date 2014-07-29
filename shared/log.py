import logging

def output(name, level = logging.DEBUG, filename = None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream = logging.StreamHandler()
    stream.setLevel(level)
    logger.addHandler(stream)

    if filename != None:
        logfile = logging.FileHandler(filename, 'a')
        logfile.setLevel(level)
        logger.addHandler(logfile)

    return logger
