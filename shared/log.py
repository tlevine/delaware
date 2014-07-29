import logging

def output(name, level = logging.DEBUG):
    logger = logging.getLogger(name)
    fp_stream = logging.StreamHandler()
    fp_stream.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(fp_stream)
    return logger
