#refactored

import sqlite3
import logging
from typing import Optional, List, Tuple, Any

logger = logging.getLogger(__name__)


class ExpenseService:
    def __init__(self, username: str, db_path: str) -> None:
        self.username = username
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category TEXT,
                        description TEXT,
                        date TEXT
                    )
                    """
                )
                conn.commit()
            logger.debug("Expenses table ensured in database.")
        except Exception as e:
            logger.error("Error creating 'expenses' table: %s", e)

    def add_expense(
        self, amount: float, category: str, date: str, description: str = ""
    ) -> bool:
        """
        Adds a new expense entry.

        Args:
        amount (float): The monetary value of the expense.
        category (str): The expense category, which must be one of the approved categories.
        date (str): The date of the expense in 'YYYY-MM-DD' format.

        Returns:
        bool: True if the expense was added successfully, otherwise False.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO expenses (username, amount, category, description, date)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.username, amount, category, description, date),
                )
                conn.commit()
            logger.info(
                "Expense added for user '%s': amount=%.2f, category=%s, desc=%s, date=%s",
                self.username,
                amount,
                category,
                description,
                date,
            )
            return True
        except Exception as e:
            logger.error("Error adding expense for user '%s': %s", self.username, e)
            return False

    def list_expenses(self) -> List[Tuple[Any, ...]]:
        """
    Lists all recorded expenses.

    This function returns a comprehensive list of all expense entries stored for the user.
    
    Returns:
        List[Tuple[Any, ...]]: A list where each tuple contains details of an individual expense entry.
    """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, username, amount, category, description, date
                    FROM expenses
                    WHERE username = ?
                    ORDER BY date DESC
                    """,
                    (self.username,),
                )
                rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error("Error listing expenses for user '%s': %s", self.username, e)
            return []

    def delete_expense(self, expense_id: int) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    DELETE FROM expenses
                    WHERE id = ? AND username = ?
                    """,
                    (expense_id, self.username),
                )
                deleted_count = cur.rowcount
                conn.commit()
            if deleted_count > 0:
                logger.info("Deleted expense with ID=%d for user '%s'", expense_id, self.username)
                return True
            else:
                logger.warning("No expense found with ID=%d for user '%s'", expense_id, self.username)
                return False
        except Exception as e:
            logger.error("Error deleting expense %d for user '%s': %s", expense_id, self.username, e)
            return False

    def update_expense(
        self,
        expense_id: int,
        amount: Optional[float] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
    ) -> bool:
        try:
            updates = []
            params: List[Any] = []
            if amount is not None:
                updates.append("amount = ?")
                params.append(amount)
            if category is not None:
                updates.append("category = ?")
                params.append(category)
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            if not updates:
                return False
            set_clause = ", ".join(updates)
            query = f"UPDATE expenses SET {set_clause} WHERE id = ? AND username = ?"
            params.extend([expense_id, self.username])
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(query, params)
                updated_count = cur.rowcount
                conn.commit()
            if updated_count > 0:
                logger.info("Updated expense ID=%d for user '%s'", expense_id, self.username)
                return True
            else:
                logger.warning("No matching expense with ID=%d for user '%s'", expense_id, self.username)
                return False
        except Exception as e:
            logger.error("Error updating expense %d for user '%s': %s", expense_id, self.username, e)
            return False



    def get_recent_expenses(self, limit: int = 10) -> List[Tuple[Any, ...]]:
        """
        Retrieves the most recent expense entries.

        Args:
        limit (int): The number of most recent expense entries to retrieve.

        Returns:
        List[Tuple[Any, ...]]: A list of tuples representing the 'n' most recent expenses.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, username, amount, category, description, date
                    FROM expenses
                    WHERE username = ?
                    ORDER BY date DESC
                    LIMIT ?
                    """,
                    (self.username, limit),
                )
                rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error("Error listing recent expenses for user '%s': %s", self.username, e)
            return []
        
    def get_expenses_for_current_day(self) -> List[Tuple[Any, ...]]:
        """
        Retrieves the user's daily spendings.

        This function collects expense data for the current day and returns it as a list of tuples, with each tuple representing an individual expense entry.

        Returns:
        List[Tuple[Any, ...]]: A list of tuples containing details of expenses made today.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, username, amount, category, description, date
                    FROM expenses
                    WHERE username = ?
                      AND strftime('%Y-%m-%d', date) = strftime('%Y-%m-%d', 'now')
                    ORDER BY date DESC
                    """,
                    (self.username,),
                )
                rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error("Error retrieving current day expenses for user '%s': %s", self.username, e)
            return []
        
        
    def get_expenses_for_current_month(self) -> List[Tuple[Any, ...]]:
        """
        Retrieves the user's monthly spendings.

        This function gathers expense data for the current month and returns it as a list of tuples, where each tuple represents a spending entry.

        Returns:
        List[Tuple[Any, ...]]: A list of tuples detailing the expenses incurred during the current month.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, username, amount, category, description, date
                    FROM expenses
                    WHERE username = ?
                      AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
                    ORDER BY date DESC
                    """,
                    (self.username,),
                )
                rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error("Error retrieving current month expenses for user '%s': %s", self.username, e)
            return []
        

    def get_expenses_for_period(self, start_date: str, end_date: str) -> List[Tuple[Any, ...]]:
        """
        Retrieves expenses between specified dates.

        Args:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

        Returns:
        List[Tuple[Any, ...]]: A list of tuples containing expense records within the specified date range.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT id, username, amount, category, description, date
                    FROM expenses
                    WHERE username = ?
                      AND date BETWEEN ? AND ?
                    ORDER BY date DESC
                    """,
                    (self.username, start_date, end_date),
                )
                rows = cur.fetchall()
            return rows
        except Exception as e:
            logger.error("Error retrieving expenses for period %s to %s for user '%s': %s", start_date, end_date, self.username, e)
            return []


