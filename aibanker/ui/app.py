import customtkinter as ctk
import logging

from aibanker.ui.login_ui import LoginFrame
from aibanker.ui.dashboard_ui import DashboardFrame
from aibanker.config_files.config_ui import *
from aibanker.config_files.config import DB_EXPENSE_FILE
from aibanker.services.expense_service import ExpenseService
from aibanker.services.diagram_service import DiagramDrawer


logger = logging.getLogger(__name__)

class App(ctk.CTk):
    def __init__(self, user_service):
        # setup
        super().__init__()

        self.user_service = user_service

        ctk.set_appearance_mode('Dark')
        self.geometry('1100x600')
        self.title('AI Banker')
        self.minsize(800, 500)
        self.config(background=DARK_DARK_GREY)

        # layout
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=7)
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=8, uniform='a')

        self.frames = {}

        self.frames["LoginFrame"] = LoginFrame(
            parent=self, 
            user_service=self.user_service,
            on_login_success=self.on_login_success
        )



    def on_login_success(self, username):
        logger.info("User '%s' logged in successfully.", username)

        self.frames["LoginFrame"].place_forget()

        get_user_limits = self.user_service.get_user_limits
        get_user_currency = self.user_service.get_user_currency

        self.expense_service = ExpenseService(username, db_path=DB_EXPENSE_FILE)
    
        self.frames["DashboardFrame"] = DashboardFrame(
            parent=self, 
            username=username, 
            expense_service=self.expense_service,
            get_user_limits = get_user_limits,
            get_user_currency = get_user_currency
        )

def run_gui(user_service):
    app = App(user_service)
    logger.info("Starting AIBanker GUI...")
    app.mainloop()