import logging
import os 
from datetime import datetime

# create log directory 
log_name = f'{datetime.utcnow()}.log'
log_dir = 'log'
log_path = log_dir + '/' + log_name
os.makedirs(log_dir, exist_ok=True)

# logger
logger = logging.getLogger('info_logger')
logger.setLevel(logging.INFO)

# create handler
file_handler = logging.FileHandler(log_path, mode='w')
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

# formatter
formatter = logging.Formatter('%(asctime)s - [%(levelname)s]: %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# addHandler
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
