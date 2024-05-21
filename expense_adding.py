import customtkinter as ctk
from settings import *
from tkcalendar import Calendar
import tkinter as tk


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.place(relx=0.5, rely=0.45, relwidth=0.9, relheight=0.5, anchor=ctk.CENTER)


class ExpenseAddingMenu(MenuFrame):

    def __init__(self, parent, username, save_expense, conn, cursor, currency):
        super().__init__(parent=parent)

        self.save_expense = save_expense
        self.username = username
        self.conn = conn
        self.cursor = cursor

        self.separator = ctk.CTkLabel(self, text='____________________________', text_color=GREY)
        self.separator.place(relx=0.5, rely=0.12, anchor=ctk.CENTER, relwidth=1)

        self.text_label = ctk.CTkLabel(self, text='EXPENSE ADDING', fg_color='transparent', text_color=WHITE,
                                       font=(FONT_REGULAR, 16))
        self.text_label.place(relx=0.5, rely=0.08, anchor=ctk.CENTER)

        self.validate_command = self.register(self.validate_input)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="Enter amount", border_width=0, fg_color=GREY,
                                         text_color=WHITE, font=(FONT_REGULAR, 14), corner_radius=25, validate="key",
                                         validatecommand=(self.validate_command, '%P'))

        self.amount_entry.place(relx=0.5, rely=0.215, relwidth=0.75, anchor=ctk.CENTER)

        self.test = ctk.CTkLabel(self.amount_entry, text=currency)
        self.test.place(relx=0.9, rely=0.5, anchor=ctk.CENTER)

        self.categories = ctk.CTkOptionMenu(self,
                                            values=list(OPTION_DICT.keys()), fg_color=GREY, button_color=GREY,
                                            button_hover_color=DARK_DARK_GREY, text_color=WHITE,
                                            corner_radius=25, width=240, height=24, font=(FONT_REGULAR, 14))
        self.categories.place(relx=0.5, rely=0.325, relwidth=0.75, anchor=ctk.CENTER)

        # self.data_entry = DateEntry(master=None)
        # self.data_entry.place(relx=0.5, rely=0.62, relwidth=0.95, relheight=0.45, anchor=tk.CENTER)

        self.calendar = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd', showweeknumbers=False,
                                 showothermonthdays=False, background=DARK_DARK_GREY,
                                 foreground=WHITE, font=(FONT_REGULAR, 11),bordercolor = 'yellow',
                                 headersbackground='green',
                                 headersforeground=WHITE, normalforeground = 'black')  # selectbackground=PAS_GREEN, selectforeground=BLACK
        self.calendar.place(relx=0.5, rely=0.62, relwidth=0.95, relheight=0.46, anchor=tk.CENTER)

        self.cancel_button = ctk.CTkButton(self, text='Cancel', text_color=BLACK, command=self.cancel_event,
                                           fg_color=PAS_RED, font=(FONT_REGULAR, 11), hover_color=PAS_RED_LIGHT)
        self.cancel_button.place(relx=0.75, rely=0.92, anchor=ctk.CENTER, relwidth=0.35)

        self.save_button = ctk.CTkButton(self, text='Save', text_color=BLACK, command=self.save_event,
                                         fg_color=PAS_GREEN, font=(FONT_REGULAR, 11), hover_color=PAS_GREEN_LIGHT)
        self.save_button.place(relx=0.25, rely=0.92, anchor=ctk.CENTER, relwidth=0.35)

    def validate_input(self, value):  # need to explained
        if value.isdigit() or value == "":
            return True
        elif value.count('.') == 1 and value.replace('.', '').isdigit():
            return True
        return False

    def cancel_event(self):
        self.place_forget()  # Changed from grid_forget to pack_forget

    def save_event(self):
        if self.amount_entry.get() == '':
            self.amount_entry.configure(border_width=1, border_color=PAS_RED)
            return
        self.place_forget()

        date = self.calendar.get_date()
        amount = self.amount_entry.get()
        category = self.categories.get()

        self.cursor.execute(f"INSERT INTO {self.username}_expenses (amount, category, date) VALUES (?, ?, ?)",
                            (amount, category, date))
        self.conn.commit()

        self.cursor.execute(f"SELECT * FROM {self.username}_expenses")

        self.save_expense()


        rows = self.cursor.fetchall()
        print(f'amount: {amount}, category: {category}, date: {date}')
        for row in rows:
            print(row)


