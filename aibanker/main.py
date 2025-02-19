# aibanker/main.py
import sys
import logging
from aibanker.utils.logger import init_logger, get_logger
from aibanker.ui.app import run_gui
from aibanker.config_files.config import DB_FILE_CREDENTIALS
from aibanker.services.user_service import UserService


def main():
    init_logger(logging.INFO)

    user_service = UserService(db_path=DB_FILE_CREDENTIALS)

    logger = get_logger(__name__)

    logger.info("Launching GUI...")
    run_gui(user_service)

if __name__ == "__main__":
    main()
