

import customtkinter as ctk
from typing import Any, Dict, Callable
import logging

from aibanker.ui.subframes.menu_frame import MenuFrame
from aibanker.ui.subframes.bar_chart_frame import BarChartFrame
from aibanker.ui.subframes.expense_history_frame import ExpenseHistoryFrame
from aibanker.ui.subframes.donut_charts_frame import DonutChartFrame
from aibanker.ui.subframes.chat_frame_ui import ChatFrame
from aibanker.services.diagram_service import DiagramDrawer



from aibanker.config_files.config_ui import *

logger = logging.getLogger(__name__)


class DashboardFrame:
    def __init__(self, parent: ctk.CTkFrame, expense_service: Any, username: str, user_config:Dict[str, str]) -> None:
        self.parent = parent

        self.daily_limit = user_config["daily_limit"]
        self.monthly_limit = user_config["monthly_limit"]
        self.currency = user_config["currency"][0]

        self.username = username
        
        self.expense_service = expense_service
        
        self.diagram_service = DiagramDrawer()
       
        self.draw_diagrams()

        self.frames: Dict[str, Any] = {}

        
        logger.info("Initializing DashboardFrame for user '%s'", self.username)
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
        
        self.frames["ChatFrame"] = ChatFrame(parent=self.parent, ai_response=self.ai_response)





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
    

    def ai_response(self, string):
        return string