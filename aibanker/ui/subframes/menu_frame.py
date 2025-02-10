#refactored


from typing import Callable, Any
import logging
import customtkinter as ctk

from aibanker.config_files.config_ui import *
from aibanker.ui.subframes.expense_adding_widget import ExpenseAddingWidget

logger = logging.getLogger(__name__)


class MenuFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        username: str,
        expense_service: Any,
        save_expense_callback: Callable[[], None],
        currency:str

    ) -> None:
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, border_width=0, corner_radius=0)
        self.parent = parent
        self.username = username
        self.currency = currency
        self.expense_service = expense_service
        self.save_expense_callback = save_expense_callback

        self.grid(column=0, rowspan=3, sticky="nsew")
        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self) -> None:
        self.separator_upper = ctk.CTkLabel(self, text="_____________________", text_color=GREY)
        self.name_label = ctk.CTkLabel(
            self,
            text="AI Banker",
            font=(FONT_REGULAR, 24),
            text_color=BLACK,
            fg_color=PAS_PURPLE,
            corner_radius=12,
            height=46,
        )
        self.home_menu_btn = ctk.CTkButton(
            self,
            text="Main Overview",
            border_width=0,
            fg_color=GREY,
            hover_color=GREY,
            corner_radius=12,
            font=(FONT_REGULAR, 16),
            text_color=WHITE,
            height=42,
            anchor="w",
        )
        self.new_expense_btn = ctk.CTkButton(
            self,
            text="New Expense",
            border_width=0,
            command=self.button_event,
            fg_color=DARK_DARK_GREY,
            hover_color=GREY,
            corner_radius=12,
            font=(FONT_REGULAR, 16),
            text_color=WHITE,
            height=42,
            anchor="w",
        )
        self.settings_btn =ctk.CTkButton(self,
            text="⚙️",
            fg_color=DARK_DARK_GREY,
            font=(FONT_REGULAR, 26),
            anchor="CENTER",
            corner_radius=15,
            hover_color=GREY,
            border_width=0,
            height=42,
        )
        self.separator_lower = ctk.CTkLabel(self, text="_____________________", text_color=GREY)
        self.logout_btn = ctk.CTkButton(
            self,
            text="Log Out",
            border_width=0,
            command=self.quit,
            fg_color=PAS_RED,
            hover_color=PAS_RED_LIGHT,
            corner_radius=25,
            font=(FONT_REGULAR, 14),
            text_color=BLACK,
            height=36,
            anchor="center",
        )

    def _place_widgets(self) -> None:
        self.separator_upper.place(relx=0.49, rely=0.12, anchor=ctk.CENTER, relwidth=1)
        self.name_label.place(relx=0.5, rely=0.07, relwidth=0.9, anchor=ctk.CENTER)
        self.home_menu_btn.place(relx=0.44, rely=0.25, anchor=ctk.CENTER, relwidth=0.63)
        self.new_expense_btn.place(relx=0.44, rely=0.35, anchor=ctk.CENTER, relwidth=0.63)
        self.settings_btn.place(relx=0.7, rely=0.93, anchor=ctk.CENTER, relwidth=0.25)
        self.separator_lower.place(relx=0.49, rely=0.86, anchor=ctk.CENTER, relwidth=1)
        self.logout_btn.place(relx=0.35, rely=0.93, anchor=ctk.CENTER, relwidth=0.4)

    def button_event(self) -> None:
        ExpenseAddingWidget(
            parent=self,
            expense_service=self.expense_service,
            master=self.parent,
            save_expense_callback=self.save_expense_callback,
            currency= self.currency
        )
        logger.info("ExpenseAddingWidget invoked from MenuFrame.")

    # def button_size(self, event: Any) -> None:
    #     if event.width < 216:
    #         pass
    #     elif event.width == 218:
    #         pass
