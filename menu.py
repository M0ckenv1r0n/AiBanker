import customtkinter as ctk
from settings import *
from tkinter import Canvas
from PIL import Image


class Menu(ctk.CTkFrame):
    def __init__(self, parent, username, open_expense_adding_menu):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, border_width=0, corner_radius=0)
        self.grid(column=0, rowspan=3, sticky='nsew')

        self.open_expense_adding_menu = open_expense_adding_menu

        self.username = username  # for futura username label

        # self.menu_frame = ctk.CTkFrame(master=self, fg_color=DARK_DARK_GREY)
        # self.menu_frame.pack(fill='both', padx=5, expand=True)

        self.separator_upper = ctk.CTkLabel(self, text='_____________________', text_color=GREY)
        self.separator_upper.place(relx=0.49, rely=0.12, anchor=ctk.CENTER, relwidth=1)

        self.name_label = ctk.CTkLabel(self, text="AI Banker", font=(FONT_REGULAR, 24),
                                       text_color=BLACK, fg_color=PAS_PURPLE, corner_radius=12, height=46)
        self.name_label.place(relx=0.5, rely=0.07, relwidth=0.9, anchor=ctk.CENTER)

        # photo = PhotoImage(file=r"icon.png")
        # photoimage = photo.subsample(3, 3)

        self.home_menu_btn = ctk.CTkButton(self, text='Main Overview',
                                           border_width=0,
                                           fg_color=GREY, hover_color=GREY,
                                           corner_radius=12, font=(FONT_REGULAR, 16), text_color=WHITE,
                                           height=42, anchor='w'
                                           )
        self.home_menu_btn.place(relx=0.44, rely=0.25, anchor=ctk.CENTER, relwidth=0.63)

        self.new_expense_btn = ctk.CTkButton(self, text='New Expense',
                                             border_width=0, command=self.button_event,
                                             fg_color=DARK_DARK_GREY, hover_color=GREY,
                                             corner_radius=12, font=(FONT_REGULAR, 16), text_color=WHITE,
                                             height=42, anchor='w'
                                             )
        self.new_expense_btn.place(relx=0.44, rely=0.35, anchor=ctk.CENTER, relwidth=0.63)

        # self.statistics_btn = ctk.CTkButton(self, text='Get Statistics',  //coming soon
        #                                     border_width=0,
        #                                     fg_color=DARK_DARK_GREY, hover_color=GREY,
        #                                     corner_radius=12, font=(FONT_REGULAR, 16), text_color=WHITE,
        #                                     height=42, anchor='w'
        #                                     )
        # self.statistics_btn.place(relx=0.44, rely=0.45, anchor=ctk.CENTER, relwidth=0.63)

        self.separator_lower = ctk.CTkLabel(self, text='_____________________', text_color=GREY)
        self.separator_lower.place(relx=0.49, rely=0.86, anchor=ctk.CENTER, relwidth=1)

        self.logout_btn = ctk.CTkButton(self, text='Log Out',
                                        border_width=0, command=self.quit,
                                        fg_color=PAS_RED, hover_color=PAS_RED_LIGHT,
                                        corner_radius=25, font=(FONT_REGULAR, 14), text_color=BLACK,
                                        height=36, anchor='center'
                                        )
        self.logout_btn.place(relx=0.35, rely=0.93, anchor=ctk.CENTER, relwidth=0.4)
        self.bind('<Configure>', self.button_size)

    def button_event(self):
        self.open_expense_adding_menu()

    def button_size(self, event):

        if event.width < 216:
            pass
            # self.home_menu_btn.place_configure(relx=0.44, rely=0.35, anchor=ctk.CENTER)
            # self.new_expense_btn.configure(width=137)
            # self.statistics_btn.configure(width=137)
            # self.logout_btn.configure(width=87)

        elif event.width == 218:
            pass


class MajorFrameUpper(Canvas):
    def __init__(self, parent, resize_image, path):
        super().__init__(master=parent, background=DARK_GREY, bd=0, highlightthickness=0, relief='ridge')
        self.grid(column=1, row=0, sticky='nsew')
        self.resize_image = resize_image

        try:
            self.image = Image.open(path)
            self.image_ratio = self.image.size[0] / self.image.size[1]
        except FileNotFoundError:
            print("Can't find image")
            return

        self.bind('<Configure>', self.img_configure)

    def img_configure(self, event):
        self.resize_image(self, event)


class MajorFrameLower(ctk.CTkFrame):
    def __init__(self, parent, expense_conn, expense_cursor, username, currency, reload):
        super().__init__(master=parent, fg_color=DARK_GREY, border_width=0, corner_radius=0)
        self.grid(column=1, row=1, sticky='nsew')
        self.expense_cursor = expense_cursor
        self.expense_conn = expense_conn
        self.username = username
        self.currency = currency
        self.reload = reload #temp

        self.separator_upper = ctk.CTkLabel(self, text='_____________________', text_color=GREY)
        self.separator_upper.place(relx=0.5, rely=0.12, anchor=ctk.CENTER)

        self.name_label = ctk.CTkLabel(self, text="Recent expenses", font=(FONT_REGULAR, 18),
                                       text_color=DARK_DARK_GREY, fg_color=PAS_PURPLE, corner_radius=12, height=35,
                                       width=120)
        self.name_label.place(relx=0.5, rely=0.06, anchor=ctk.CENTER)

        self.scrollable_frame = ScrollableFrame(self, self.expense_conn, self.expense_cursor, self.username,
                                                self.currency)

        self.more_button = ctk.CTkButton(self, text="Load All", font=(FONT_REGULAR, 14), width=40, height=10,
                                         text_color=WHITE, fg_color=DARK_GREY, corner_radius=15,
                                         text_color_disabled=LIGHT_GREY,
                                         command=self.scrollable_frame.process_remaining_rows, hover_color=GREY)
        self.more_button.place(relx=0.12, rely=0.18, anchor=ctk.CENTER)

        self.less_button = ctk.CTkButton(self, text="Load Less", font=(FONT_REGULAR, 14),
                                         text_color=WHITE, fg_color=DARK_GREY, corner_radius=15, width=40,
                                         height=10, state='disabled', text_color_disabled=LIGHT_GREY,
                                         command=self.less_button_func, hover_color=GREY)
        self.less_button.place(relx=0.35, rely=0.18, anchor=ctk.CENTER)

    def less_button_func(self):
        self.less_button.configure(state='disabled')
        self.more_button.configure(state='normal')
        self.reload() #temp

        # self.scrollable_frame = ScrollableFrame(self, self.expense_conn, self.expense_cursor, self.username,
        #                                         self.currency)


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, parent, conn_expense, cursor_expense, username, currency):
        super().__init__(master=parent, fg_color=DARK_GREY, border_width=0, corner_radius=0)
        self.place(relx=0.5, rely=0.62, relwidth=0.95, relheight=0.76, anchor=ctk.CENTER)
        self.parent = parent
        self.cursor_expense = cursor_expense
        self.conn_expense = conn_expense
        self.username = username
        self.currency = currency

        self.cursor_expense.execute(f'SELECT amount, category, date FROM {self.username}_expenses ORDER BY date DESC')

        # Iterate over the rows in reverse order
        # Retrieve the first 10 rows
        initial_rows = self.cursor_expense.fetchmany(10)

        # Create FrameScrlContent instances for the first 10 rows
        for row in initial_rows:
            amount = row[0]
            category = row[1]
            date = row[2]
            FrameScrlContent(self, amount, category, self.currency, date)

        # Function to handle the event and process the remaining rows

    def process_remaining_rows(self):
        self.parent.more_button.configure(state='disabled')
        self.parent.less_button.configure(state='normal')

        remaining_rows = self.cursor_expense.fetchall()
        for row in remaining_rows:
            amount = row[0]
            category = row[1]
            date = row[2]
            FrameScrlContent(self, amount, category, self.currency, date)


class FrameScrlBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=GREY)
        self.configure(height=45)
        self.pack(padx=(20, 10), pady=5, expand=True, fill='x')


class FrameScrlContent(FrameScrlBar):
    def __init__(self, parent, amount, category, currency, date):
        super().__init__(parent=parent)
        self.cancel_btn = ctk.CTkButton(self, text='X', text_color=BLACK, corner_radius=2,
                                        fg_color=PAS_RED, font=(FONT_REGULAR, 7), hover_color=PAS_RED_LIGHT,
                                        command=self.pack_forget, height=10, width=15)
        self.cancel_btn.pack(side='right', anchor='n', padx=5, pady=5, ipadx=1, ipady=1)

        self.text_label = ctk.CTkLabel(self, text=f'{amount} {currency}', fg_color=PAS_ORANGE, text_color=BLACK,
                                       font=(FONT_REGULAR, 16), corner_radius=15)
        self.text_label.pack(side='left', padx=(16, 0), pady=10)

        self.text_label_cat = ctk.CTkLabel(self, text=category, fg_color=OPTION_DICT[category], text_color=BLACK,
                                           corner_radius=15,
                                           font=(FONT_REGULAR, 10))
        self.text_label_cat.pack(side='left', padx=5, pady=10)

        self.text_label_cat = ctk.CTkLabel(self, text=date, fg_color='transparent', text_color=PAS_ORANGE_LIGHT,
                                           font=(FONT_REGULAR, 12))
        self.text_label_cat.pack(side='right', padx=10, pady=10)


class MinorFrameUpper(ctk.CTkFrame):
    def __init__(self, parent, resize_image, daily_path, monthly_path, currency, daily_limit, monthly_limit):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, corner_radius=0)
        self.grid(column=2, row=0, sticky='nsew')
        self.currency = currency
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.resize_image = resize_image
        self.daily_path = daily_path
        self.monthly_path = monthly_path

        self.donut_diagram_daily = DonutDiagramDaily(self, resize_image, self.daily_path)
        self.daily_donut_btn = ctk.CTkButton(self, text='Daily', fg_color=GREY, height=18, width=140, hover_color=GREY,
                                             font=(FONT_REGULAR, 14), text_color=WHITE, corner_radius=10)
        self.daily_donut_btn.place(relx=0.25, rely=0.92, anchor=ctk.CENTER)
        self.monthly_donut_btn = ctk.CTkButton(self, text='Monthly', fg_color='transparent', height=18, width=140,
                                               font=(FONT_REGULAR, 14), hover_color=GREY, text_color=WHITE,
                                               corner_radius=10, command=self.change_to_monthly)
        self.monthly_donut_btn.place(relx=0.74, rely=0.92, anchor=ctk.CENTER)
        self.photo = ctk.CTkImage(light_image=Image.open("img/icons/settings_icon.png"),
                                  size=(16, 16))
        self.settings_btn = ctk.CTkButton(self, text=f"Daily Limit: {self.daily_limit}{currency}",
                                          font=(FONT_REGULAR, 9), image=self.photo, width=16, height=16,
                                          fg_color='transparent', hover_color=GREY, text_color=WHITE)
        self.settings_btn.place(relx=0.82, rely=0.15, anchor=ctk.CENTER)

    def change_to_monthly(self):
        pass


class DonutDiagramDaily(Canvas):
    def __init__(self, parent, resize_image, path):
        super().__init__(master=parent, background=DARK_DARK_GREY, bd=0, highlightthickness=0, relief='ridge')
        self.place(relx=0.5, rely=0.512, relwidth=1, relheight=0.9, anchor=ctk.CENTER)
        self.resize_image = resize_image

        try:
            self.image = Image.open(path)
            self.image_ratio = self.image.size[0] / self.image.size[1]
        except FileNotFoundError:
            print("Can't find image")
            return

        self.bind('<Configure>', self.img_configure)

    def img_configure(self, event):
        self.resize_image(self, event)


class DonutDiagramMonthly(Canvas):
    def __init__(self, parent, resize_image, path):
        super().__init__(master=parent, background=DARK_DARK_GREY, bd=0, highlightthickness=0, relief='ridge')
        self.place(relx=0.5, rely=0.512, relwidth=1, relheight=0.9, anchor=ctk.CENTER)
        self.resize_image = resize_image

        try:
            self.image = Image.open(path)
            self.image_ratio = self.image.size[0] / self.image.size[1]
        except FileNotFoundError:
            print("Can't find image")
            return

        self.bind('<Configure>', self.img_configure)

    def img_configure(self, event):
        self.resize_image(self, event)

