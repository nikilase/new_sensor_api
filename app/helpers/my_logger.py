import logging
from datetime import datetime

logger = logging.getLogger("uvicorn.error")


def log_info(function: str, message: str = ""):
    current_date = datetime.now().strftime("%d.%b %Y %H:%M:%S")
    logger.info(f'{current_date} - \033[1m"{function}"\033[0m {message}')


def log_warn(function: str, message: str = ""):
    current_date = datetime.now().strftime("%d.%b %Y %H:%M:%S")
    logger.warning(f'{current_date} - \033[1m"{function}"\033[0m {message}')


def log_error(function: str, message: str = ""):
    current_date = datetime.now().strftime("%d.%b %Y %H:%M:%S")
    logger.error(f'{current_date} - \033[1m"{function}"\033[0m {message}')
