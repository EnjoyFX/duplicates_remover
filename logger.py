import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_line = '%(asctime)s - %(filename)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(log_line)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
