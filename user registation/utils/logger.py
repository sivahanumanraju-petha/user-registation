import logging

logger = logging.getLogger("user_logger")

def init_logger():
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("user_activity.log")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
