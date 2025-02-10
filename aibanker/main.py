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

    # logger.debug("Initializing application configuration...")

    # if len(sys.argv) < 2:
    #     logger.warning("No mode provided. Usage: python -m aibanker [cli|gui]")
    #     sys.exit(1)

    # mode = sys.argv[1].lower()
    # logger.info(f"Running in {mode} mode...")

    # if mode == "cli":
    #     pass

    # elif mode == "gui":
    #     logger.info("Launching GUI...")
    #     run_gui(user_service)
    # else:
    #     logger.error("Invalid mode: %s. Use 'cli' or 'gui'.", mode)
    #     sys.exit(1)

if __name__ == "__main__":
    main()
