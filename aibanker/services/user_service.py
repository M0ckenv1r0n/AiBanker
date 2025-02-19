#refactored

import sqlite3
import logging
from passlib.hash import bcrypt
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class UserService:
    """
    Handles user registration, authentication, and limit management
    in an SQLite database.
    """

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self.username = 'Dmjkef@33434' #temp
        self._init_db()

    def _init_db(self) -> None:
        logger.debug("Initializing the database and creating table if needed.")
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        daily_limit REAL,
                        monthly_limit REAL,
                        currency TEXT
                    )
                """)
            logger.debug("Database initialized successfully.")
        except Exception as e:
            logger.error("Error initializing database: %s", e)

    def register_user(
        self,
        username: str,
        plain_password: str,
        daily_limit: float,
        monthly_limit: float,
        currency: str
    ) -> bool:
        


        logger.debug("Attempting to register user '%s'.", username)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
                if cursor.fetchone():
                    logger.warning("Attempt to register existing user '%s'.", username)
                    return False

                hashed_password = bcrypt.hash(plain_password)
                cursor.execute("""
                    INSERT INTO users (username, password, daily_limit, monthly_limit, currency)
                    VALUES (?, ?, ?, ?, ?)
                """, (username, hashed_password, daily_limit, monthly_limit, currency))
                logger.info("User '%s' registered successfully.", username)
                return True

        except Exception as e:
            logger.error("Error registering user '%s': %s", username, e)
            return False

    def authenticate(self, username: str, plain_password: str) -> bool:
        logger.debug("Authenticating user '%s'.", username)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
                row = cursor.fetchone()

            if not row:
                logger.debug("User '%s' does not exist or no rows returned.", username)
                return False

            hashed_password = row[0]
            valid = bcrypt.verify(plain_password, hashed_password)
            if valid:
                logger.debug("User '%s' authentication successful.", username)
                self._init_username(username)
            else:
                logger.debug("User '%s' authentication failed (wrong password).", username)
            return valid

        except Exception as e:
            logger.error("Error authenticating user '%s': %s", username, e)
            return False

    def get_user_limits(self) -> Optional[Dict[str, Any]]:
         
        """
        Returns the user's spending limits.

        This function retrieves the user's daily and monthly spending limits and returns them as a dictionary.

        Returns:
        dict: A dictionary containing the keys 'daily_limit' and 'monthly_limit' with their respective float values.
        """

        logger.debug("Fetching limits for user '%s'.", self.username)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT daily_limit, monthly_limit
                    FROM users WHERE username = ?
                """, (self.username,))
                row = cursor.fetchone()

            if not row:
                logger.debug("No limit data found for user '%s'.", self.username)
                return None

            return {
                "daily_limit": row[0],
                "monthly_limit": row[1],
            }
        except Exception as e:
            logger.error("Error fetching limits for user '%s': %s", self.username, e)
            return None
        
    def get_user_currency(self) -> str:
        logger.debug("Fetching currency for user '%s'.", self.username)
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT currency
                    FROM users WHERE username = ?
                """, (self.username,))
                row = cursor.fetchone()

            if not row:
                logger.debug("No currency data found for user '%s'.", self.username)
                return None
            return row[0]
        except Exception as e:
            logger.error("Error currency for user '%s': %s", self.username, e)
            return None
        
    def update_user_limits(
        self,
        daily_limit: float,
        monthly_limit: float,
        currency: str
    ) -> bool:
        logger.debug(
            "Updating user limits for '%s': daily_limit=%s, monthly_limit=%s, currency=%s",
            self.username, daily_limit, monthly_limit, currency
        )
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET daily_limit = ?, monthly_limit = ?, currency = ?
                    WHERE username = ?
                """, (daily_limit, monthly_limit, currency, self.username))
                updated_rows = cursor.rowcount

            if updated_rows > 0:
                logger.info("Limits updated successfully for user '%s'.", self.username)
            else:
                logger.warning("No rows updated when attempting to set limits for user '%s'.", username)
            return updated_rows > 0

        except Exception as e:
            logger.error("Error updating user limits for '%s': %s", self.username, e)
            return False

    def _init_username(self, username: str):
        self.username = username