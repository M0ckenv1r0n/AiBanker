import customtkinter as ctk
import threading
from typing import Any, Dict, Callable
import logging

from aibanker.ui.subframes.menu_frame import MenuFrame
from aibanker.ui.subframes.bar_chart_frame import BarChartFrame
from aibanker.ui.subframes.expense_history_frame import ExpenseHistoryFrame
from aibanker.ui.subframes.donut_charts_frame import DonutChartFrame
from aibanker.ui.subframes.chat_frame_ui import ChatFrame
from aibanker.services.diagram_service import DiagramDrawer
from aibanker.ai.LLM_with_tools import LLMChat



from aibanker.config_files.config_ui import *

logger = logging.getLogger(__name__)


class DashboardFrame:
    def __init__(self, parent: ctk.CTkFrame, expense_service: Any, username: str, get_user_limits: Callable[[], Dict[str, float]], get_user_currency: Callable[[], str]) -> None:
        self.parent = parent

        self.get_user_limits = get_user_limits
        self.get_user_currency = get_user_currency

        self.username = username
        
        self.expense_service = expense_service

        self._init_user_config()
        self.diagram_service = DiagramDrawer()

        tools = [
            get_user_limits,
            self.add_expense_with_callback,
            self.expense_service.list_expenses,
            self.expense_service.get_recent_expenses,
            self.expense_service.get_expenses_for_current_day,
            self.expense_service.get_expenses_for_current_month,
            self.expense_service.get_expenses_for_period]
        self.llm_chat_with_tools = LLMChat(
            currency= self.get_user_currency(), tools=tools)       

        self.draw_diagrams()
        logger.info("Initializing DashboardFrame for user '%s'", self.username)
        self.frames: Dict[str, Any] = {}
        self._init_frames()

    def _init_frames(self) -> None:
        logger.debug("Creating MenuFrame and ExpenseHistoryFrame")
        self.frames["MenuFrame"] = MenuFrame(
            parent=self.parent,
            username=self.username,
            expense_service=self.expense_service,
            save_expense_callback=self._expense_callback,
            currency=self.currency
        )
        self.frames["ExpenseHistoryFrame"] = ExpenseHistoryFrame(
            parent=self.parent,
            expense_service=self.expense_service,
            delete_expense_callback = self._expense_callback,
            currency = self.currency
        )

        self.frames["BarChartFrame"] = BarChartFrame(
            parent=self.parent,
            plain_image=self.monthly_bar_diagram_image
            )
        
        self.frames["DonutChartFrame"]= DonutChartFrame(parent=self.parent,
            plain_image_daily=self.donut_daily_limit_image,
            plain_image_monthly = self.donut_monthly_limit_image,
            daily_limit=self.daily_limit,
            monthly_limit=self.monthly_limit,
            currency=self.currency)
        
        self.frames["ChatFrame"] = ChatFrame(parent=self.parent, llm_add_message=self.llm_add_message)





    def _expense_callback(self) -> None:

        self.frames["ExpenseHistoryFrame"].destroy()

        self.frames["ExpenseHistoryFrame"] = ExpenseHistoryFrame(
            parent=self.parent,
            expense_service=self.expense_service,
            delete_expense_callback = self._expense_callback,
            currency = self.currency
        )

        self.frames["BarChartFrame"].destroy()
        self.frames["DonutChartFrame"].destroy()

        self.draw_diagrams()

        self.frames["BarChartFrame"] = BarChartFrame(
            parent=self.parent,
            plain_image=self.monthly_bar_diagram_image
            )
        
        self.frames["DonutChartFrame"]= DonutChartFrame(parent=self.parent,
            plain_image_daily=self.donut_daily_limit_image,
            plain_image_monthly = self.donut_monthly_limit_image,
            daily_limit=self.daily_limit,
            monthly_limit=self.monthly_limit,
            currency=self.currency)
        
        

    def draw_diagrams(self):
        self.monthly_bar_diagram_image = self.diagram_service.monthly_bar_diagram(self.expense_service.list_expenses())
        self.donut_daily_limit_image = self.diagram_service.donut_limit( 
            records=self.expense_service.get_expenses_for_current_day(), _limit = self.daily_limit, currency= self.currency)
        self.donut_monthly_limit_image = self.diagram_service.donut_limit( 
            records=self.expense_service.get_expenses_for_current_month(), _limit = self.monthly_limit, currency= self.currency)
    

    def llm_add_message(self, input:str) -> str:
        output = self.llm_chat_with_tools.add_message(input)
        return output


    def _init_user_config(self):
        user_limits = self.get_user_limits()
        self.daily_limit = user_limits["daily_limit"]
        self.monthly_limit = user_limits["monthly_limit"]

        self.currency = self.get_user_currency()[0]
    
    def change_limits():
        pass

    def add_expense_with_callback(self, amount: float, category: str, date: str, description: str = ""):
        """
        Adds a new expense entry.

        Args:
        amount (float): The monetary value of the expense.
        category (str): The expense category, which must be one of the approved categories.
        date (str): The date of the expense in 'YYYY-MM-DD' format.

        Returns:
        bool: True if the expense was added successfully, otherwise False.
        """
        if self.expense_service.add_expense(amount = amount, category = category, date = date, description = description):
            thread = threading.Thread(target=self._expense_callback)
            thread.start()
            return True
        
        return False

