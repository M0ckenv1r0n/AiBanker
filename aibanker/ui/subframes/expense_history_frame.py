import customtkinter as ctk
from typing import Any, List, Tuple, Callable
import logging

from aibanker.config_files.config_ui import *
from aibanker.config_files.config import OPTION_DICT

logger = logging.getLogger(__name__)


class ExpenseHistoryFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, expense_service: Any, delete_expense_callback: Callable[[], None], currency:str) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, border_width=0, corner_radius=0)
        self.grid(column=1, row=1, sticky='nsew')
        self.expense_service = expense_service
        self.delete_expense_callback = delete_expense_callback
        self.currency = currency

        logger.info("Initializing ExpenseHistoryFrame")
        self.separator_label = ctk.CTkLabel(self, text='_____________________', text_color=GREY)
        self.separator_label.place(relx=0.5, rely=0.12, anchor=ctk.CENTER)

        self.title_label = ctk.CTkLabel(
            self,
            text="Recent Expenses",
            font=(FONT_REGULAR, 18),
            text_color=DARK_DARK_GREY,
            fg_color=PAS_PURPLE,
            corner_radius=12,
            height=35,
            width=120
        )
        self.title_label.place(relx=0.5, rely=0.06, anchor=ctk.CENTER)

        self.load_all_button = ctk.CTkButton(
            self,
            text="Load All",
            font=(FONT_REGULAR, 14),
            width=40,
            height=10,
            text_color=WHITE,
            fg_color=DARK_GREY,
            corner_radius=15,
            text_color_disabled=LIGHT_GREY,
            hover_color=GREY,
            command=None  # set after subframe creation
        )
        self.load_all_button.place(relx=0.12, rely=0.18, anchor=ctk.CENTER)

        self.load_less_button = ctk.CTkButton(
            self,
            text="Load Less",
            font=(FONT_REGULAR, 14),
            text_color=WHITE,
            fg_color=DARK_GREY,
            corner_radius=15,
            width=40,
            height=10,
            state='disabled',
            text_color_disabled=LIGHT_GREY,
            hover_color=GREY,
            command=self.on_load_less_click
        )
        self.load_less_button.place(relx=0.35, rely=0.18, anchor=ctk.CENTER)

        self.scrollable_frame = ScrollableExpenseList(self, self.expense_service, self.delete_expense_callback, self.currency)
        self.load_all_button.configure(command=self.scrollable_frame.on_load_all_click)

    def on_load_less_click(self) -> None:
        logger.info("Load Less button clicked")
        self.scrollable_frame.show_less()


class ScrollableExpenseList(ctk.CTkScrollableFrame):
    def __init__(self, parent: ExpenseHistoryFrame, expense_service: Any, delete_expense_callback:Callable[[], None], currency:str) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, border_width=0, corner_radius=0)
        self.place(relx=0.5, rely=0.62, relwidth=0.95, relheight=0.76, anchor=ctk.CENTER)
        self.parent = parent
        self.expense_service = expense_service
        self.delete_expense_callback = delete_expense_callback

        self.all_rows: List[Tuple[Any, ...]] = self._fetch_all_expenses()
        self.shown_count: int = 10
        logger.info("Fetched %d expense rows", len(self.all_rows))
        self._create_item_frames(self.all_rows[:self.shown_count])
        self._update_buttons()

    def _fetch_all_expenses(self) -> List[Tuple[Any, ...]]:
        return self.expense_service.list_expenses()

    def _clear_item_frames(self) -> None:
        for child in self.winfo_children():
            child.destroy()

    def _create_item_frames(self, rows: List[Tuple[Any, ...]]) -> None:
        for row in rows:
            expense_id = row[0]
            amount = row[2]
            category = row[3]
            date = row[5]
            ExpenseItemFrame(self, expense_id, amount, category, date)

    def on_load_all_click(self) -> None:
        logger.info("Load All button clicked")
        self._clear_item_frames()
        self.shown_count = len(self.all_rows)
        self._create_item_frames(self.all_rows)
        self._update_buttons()

    def show_less(self) -> None:
        logger.info("Showing fewer expense items")
        self._clear_item_frames()
        self.shown_count = 10
        self._create_item_frames(self.all_rows[:min(10, len(self.all_rows))])
        self._update_buttons()

    def request_delete_item(self, expense_id: Any, item_frame: ctk.CTkFrame) -> None:
        success = self.expense_service.delete_expense(expense_id)
        if success:
            self.all_rows = [r for r in self.all_rows if r[0] != expense_id]
            item_frame.pack_forget()
            if self.shown_count > len(self.all_rows):
                self.shown_count = len(self.all_rows)
            self._update_buttons()
            logger.info("Deleted expense with ID %s", expense_id)
            
            self.delete_expense_callback()
        else:
            logger.warning("Failed to delete expense with ID %s", expense_id)

    def _update_buttons(self) -> None:
        total_items = len(self.all_rows)
        if total_items <= 10:
            self.parent.load_all_button.configure(state='disabled')
            self.parent.load_less_button.configure(state='disabled')
        elif self.shown_count < total_items:
            self.parent.load_all_button.configure(state='normal')
            self.parent.load_less_button.configure(state='disabled')
        else:
            self.parent.load_all_button.configure(state='disabled')
            self.parent.load_less_button.configure(state='normal')


class ExpenseItemFrame(ctk.CTkFrame):
    def __init__(self, parent: ScrollableExpenseList, expense_id: Any, amount: float,
                 category: str, date: str) -> None:
        super().__init__(master=parent, fg_color=GREY)
        self.configure(height=45)
        self.parent = parent
        self.expense_id = expense_id
        self.pack(padx=(20, 10), pady=5, expand=True, fill='x')

        self.remove_button = ctk.CTkButton(
            self,
            text='X',
            text_color=BLACK,
            corner_radius=2,
            fg_color=PAS_RED,
            font=(FONT_REGULAR, 7),
            hover_color=PAS_RED_LIGHT,
            command=self._on_remove_click,
            height=10,
            width=15
        )
        self.remove_button.pack(side='right', anchor='n', padx=5, pady=5, ipadx=1, ipady=1)

        self.amount_label = ctk.CTkLabel(
            self,
            text=f'{amount} {parent.parent.currency}',
            fg_color=PAS_ORANGE,
            text_color=BLACK,
            font=(FONT_REGULAR, 16),
            corner_radius=15
        )
        self.amount_label.pack(side='left', padx=(16, 0), pady=10)

        cat_color = OPTION_DICT.get(category, PAS_ORANGE_LIGHT)
        self.category_label = ctk.CTkLabel(
            self,
            text=category,
            fg_color=cat_color,
            text_color=BLACK,
            corner_radius=15,
            font=(FONT_REGULAR, 10)
        )
        self.category_label.pack(side='left', padx=5, pady=10)

        self.date_label = ctk.CTkLabel(
            self,
            text=date,
            fg_color='transparent',
            text_color=PAS_ORANGE_LIGHT,
            font=(FONT_REGULAR, 12)
        )
        self.date_label.pack(side='right', padx=10, pady=10)

    def _on_remove_click(self) -> None:
        self.parent.request_delete_item(self.expense_id, self)
