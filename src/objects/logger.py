import logging

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# Create a file handler that logs to a file named myapp.log
file_handler = logging.FileHandler('app.log')

# Create a stream handler that logs to the console
stream_handler = logging.StreamHandler()

# Create a formatter for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handlers
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
