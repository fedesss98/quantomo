import logging

def setup_logger(level=logging.INFO):
    # This configures the 'my_package' logger and all its children
    logger = logging.getLogger('quantomo') 
    logger.setLevel(level)
    
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
