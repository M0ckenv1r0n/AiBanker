#REF

import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from typing import Any, Callable
import logging

from aibanker.config_files.config_ui import *
from aibanker.config_files.config import OPTION_DICT
from aibanker.ui.share.notification_frame import NotifFrame

logger = logging.getLogger(__name__)


class Box(ctk.CTkFrame):
    def __init__(self, parent: Any) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.5, anchor=ctk.CENTER)


class ExpenseAddingWidget(Box):
    def __init__(
        self,
        parent: ctk.CTkFrame,
        expense_service: Any,
        save_expense_callback: Callable[[], None],
        master: ctk.CTkFrame,
        currency: str
    ) -> None:
        super().__init__(parent=parent)
        self.master = master
        self.expense_service = expense_service
        self.save_expense_callback = save_expense_callback
        self.currency = currency

        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self) -> None:
        self.separator = ctk.CTkLabel(self, text='____________________________', text_color=GREY)
        self.text_label = ctk.CTkLabel(
            self,
            text='EXPENSE ADDING',
            fg_color='transparent',
            text_color=WHITE,
            font=(FONT_REGULAR, 16)
        )
        self.validate_command = self.register(self.validate_input)
        self.amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter amount",
            border_width=0,
            fg_color=GREY,
            text_color=WHITE,
            font=(FONT_REGULAR, 14),
            corner_radius=25,
            validate="key",
            validatecommand=(self.validate_command, '%P')
        )
        self.currency_label = ctk.CTkLabel(self.amount_entry, text=self.currency)
        self.categories = ctk.CTkOptionMenu(
            self,
            values=list(OPTION_DICT.keys()),
            fg_color=GREY,
            button_color=GREY,
            button_hover_color=DARK_DARK_GREY,
            text_color=WHITE,
            corner_radius=25,
            width=240,
            height=24,
            font=(FONT_REGULAR, 14)
        )
        self.calendar = Calendar(
            self,
            selectmode='day',
            date_pattern='yyyy-mm-dd',
            showweeknumbers=False,
            showothermonthdays=False,
            background=DARK_DARK_GREY,
            foreground=WHITE,
            font=(FONT_REGULAR, 11),
            bordercolor='yellow',
            headersbackground='green',
            headersforeground=WHITE,
            normalforeground='black'
        )
        self.cancel_button = ctk.CTkButton(
            self,
            text='Cancel',
            text_color=BLACK,
            command=self.cancel_event,
            fg_color=PAS_RED,
            font=(FONT_REGULAR, 11),
            hover_color=PAS_RED_LIGHT
        )
        self.save_button = ctk.CTkButton(
            self,
            text='Save',
            text_color=BLACK,
            command=self.save_event,
            fg_color=PAS_GREEN,
            font=(FONT_REGULAR, 11),
            hover_color=PAS_GREEN_LIGHT
        )

    def _place_widgets(self) -> None:
        self.separator.place(relx=0.5, rely=0.12, anchor=ctk.CENTER, relwidth=1)
        self.text_label.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)
        self.amount_entry.place(relx=0.5, rely=0.215, relwidth=0.75, anchor=ctk.CENTER)
        self.currency_label.place(relx=0.9, rely=0.5, anchor=ctk.CENTER)
        self.categories.place(relx=0.5, rely=0.325, relwidth=0.75, anchor=ctk.CENTER)
        self.calendar.place(relx=0.5, rely=0.62, relwidth=0.95, relheight=0.46, anchor=tk.CENTER)
        self.cancel_button.place(relx=0.75, rely=0.92, anchor=ctk.CENTER, relwidth=0.35)
        self.save_button.place(relx=0.25, rely=0.92, anchor=ctk.CENTER, relwidth=0.35)

    def validate_input(self, value: str) -> bool:
        return value == "" or value.isdigit() or (value.count('.') == 1 and value.replace('.', '').isdigit())

    def cancel_event(self) -> None:
        logger.info("Cancel event triggered; hiding ExpenseAddingWidget")
        self.place_forget()

    def save_event(self) -> None:
        amount_str = self.amount_entry.get()
        if not amount_str:
            self.amount_entry.configure(border_width=1, border_color=PAS_RED)
            logger.warning("Save event: empty amount entry")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            logger.error("Save event: invalid amount '%s'", amount_str)
            return

        date = self.calendar.get_date()
        category = self.categories.get()
        success = self.expense_service.add_expense(
            amount=amount,
            category=category,
            date=date,
            description="An expense is added using the expense_adding_widget"
        )
        if success:
            logger.info("Expense added: %s in category %s on %s", amount, category, date)
            NotifFrame(self.master, "positive", "Expense added successfully")
            self.save_expense_callback()
        else:
            logger.warning("Expense addition failed")
            NotifFrame(self.master, "negative", "An error occurred")
        self.place_forget()
