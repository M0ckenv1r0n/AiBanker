import hashlib
import re
from settings import *
import customtkinter as ctk
import sqlite3


class Login(ctk.CTkFrame):
    def __init__(self, parent, import_func, conn, cursor):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)

        self.parent = parent
        self.place_configure(relx=0.5, rely=0.5, anchor=ctk.CENTER, width=430, height=410)
        self.import_func = import_func
        self.conn = conn
        self.cursor = cursor



        self.login_label = ctk.CTkLabel(self, text="LOGIN", font=(FONT_REGULAR, 48), text_color=WHITE)
        self.login_label.place(relx=0.5, rely=0.17, anchor=ctk.CENTER)

        self.minor_login_label = ctk.CTkLabel(self, text="Please enter your username and password!",
                                              text_color=LIGHT_GREY,
                                              font=(FONT_REGULAR, 14))
        self.minor_login_label.place(relx=0.5, rely=0.285, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", border_width=0, fg_color=GREY,
                                           corner_radius=25, width=240, height=42,
                                           font=(FONT_REGULAR, 16))
        self.username_entry.place(relx=0.5, rely=0.42, anchor=ctk.CENTER)

        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Password", fg_color=GREY,
                                           border_width=0, corner_radius=25, width=240, height=42,
                                           font=(FONT_REGULAR, 16))
        self.password_entry.place(relx=0.5, rely=0.57, anchor=ctk.CENTER)

        self.error_msg = ctk.CTkLabel(self, text="", text_color=PAS_RED, fg_color='transparent',
                                      font=(FONT_REGULAR, 12))
        self.error_msg.place(relx=0.5, rely=0.66, anchor=ctk.CENTER)

        self.login_btn = ctk.CTkButton(self, text='Log In', border_width=0,
                                       command=self.check_login, fg_color=PAS_GREEN, hover_color=PAS_GREEN_LIGHT,
                                       corner_radius=35, text_color=BLACK,
                                       font=(FONT_REGULAR, 16), height=46, width=132)
        self.login_btn.place(relx=0.5, rely=0.795, anchor=ctk.CENTER)

        self.change_to_register_btn = ctk.CTkButton(self, text="Don't have an account? Sign Up", text_color=LIGHT_GREY,
                                                    fg_color=DARK_GREY, command=self.change_to_register,
                                                    font=(FONT_REGULAR, 12),
                                                    hover_color=DARK_GREY)
        self.change_to_register_btn.place(relx=0.5, rely=0.91, anchor=ctk.CENTER)



    def check_login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        self.cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        stored_password = self.cursor.fetchone()

        if stored_password and hashed_password == stored_password[0]:
            print("Login successful!")
            self.import_func(username)

        else:
            self.show_error()
            print("Invalid username or password")

    def show_error(self):
        self.error_msg.configure(text="Invalid username or password")
        self.password_entry.configure(border_width=1, border_color=PAS_RED)
        self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def change_to_register(self):
        Register(self.parent, self.conn, self.cursor)


class Register(ctk.CTkFrame):
    def __init__(self, parent, conn, cursor):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.place_configure(relx=0.5, rely=0.5, anchor=ctk.CENTER, width=430, height=510)
        self.conn = conn
        self.cursor = cursor
        self.parent = parent

        self.register_label = ctk.CTkLabel(self, text="SIGN UP", font=(FONT_REGULAR, 48), text_color=WHITE)
        self.register_label.place(relx=0.5, y=53.5, anchor=ctk.CENTER)

        self.minor_reg_label = ctk.CTkLabel(self, text="Please enter your futura username and password!",
                                            text_color=LIGHT_GREY,
                                            font=(FONT_REGULAR, 14))
        self.minor_reg_label.place(relx=0.5, y=94, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", border_width=0, fg_color=GREY,
                                           corner_radius=25, width=240, height=40,
                                           font=(FONT_REGULAR, 16))
        self.username_entry.place(relx=0.5, y=145, anchor=ctk.CENTER)
        self.username_entry.update()

        self.separator_upper = ctk.CTkLabel(self, text='_________________________', text_color=GREY)
        self.separator_upper.place(relx=0.5, y=227, anchor=ctk.CENTER, relwidth=1)

        self.separator_lower = ctk.CTkLabel(self, text='_________________________', text_color=GREY)
        self.separator_lower.place(relx=0.5, y=357, anchor=ctk.CENTER, relwidth=1)

        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Password", fg_color=GREY,
                                           border_width=0, corner_radius=25, width=240, height=40,
                                           font=(FONT_REGULAR, 16))
        self.password_entry.place(relx=0.5, y=200, anchor=ctk.CENTER)
        self.password_entry.update()

        self.set_currency_label = ctk.CTkLabel(self, text="Set your currency:", font=(FONT_REGULAR, 16),
                                               text_color='#b9baba')
        self.set_currency_label.place(relx=0.456, y=262.7, anchor=ctk.E)

        self.currency = ctk.CTkOptionMenu(self, fg_color=GREY, font=(FONT_REGULAR, 14), corner_radius=25, height=28,
                                          width=72, values=[f'{value}  {key}' for key, value in CURRENCY_DICT.items()],
                                          button_color=GREY,
                                          button_hover_color=DARK_DARK_GREY, dynamic_resizing=False)
        self.currency.place(relx=0.625, y=262.7, anchor=ctk.W)

        self.daily_limit_label = ctk.CTkLabel(self, text='Set your daily limit:', font=(FONT_REGULAR, 16),
                                              text_color='#b9baba')
        self.daily_limit_label.place(relx=0.31, y=334, anchor=ctk.CENTER)

        self.monthly_budget_label = ctk.CTkLabel(self, text="Set your monthly limit:", font=(FONT_REGULAR, 16),
                                                 text_color='#b9baba')
        self.monthly_budget_label.place(relx=0.335, y=298.4, anchor=ctk.CENTER)

        self.validate_command = self.register(self.validate_input)

        self.daily_limit_entry = ctk.CTkEntry(self, validate="key",
                                              placeholder_text="Enter your daily limit",
                                              validatecommand=(self.validate_command, '%P'), border_width=0,
                                              fg_color=GREY,
                                              corner_radius=25, width=120, height=28,
                                              font=(FONT_REGULAR, 12))
        self.daily_limit_entry.place(relx=0.705, y=334, anchor=ctk.CENTER)

        self.monthly_limit_entry = ctk.CTkEntry(self, validate="key",
                                                placeholder_text="Enter your monthly budget",
                                                validatecommand=(self.validate_command, '%P'), border_width=0,
                                                fg_color=GREY,
                                                corner_radius=25, width=120, height=28,
                                                font=(FONT_REGULAR, 12))
        self.monthly_limit_entry.place(relx=0.705, y=298.4, anchor=ctk.CENTER)

        self.place_for_error_msg = ctk.CTkLabel(self, text="", text_color=PAS_RED, fg_color='transparent',
                                                font=(FONT_REGULAR, 12))
        self.place_for_error_msg.place(relx=0.5, y=380, anchor=ctk.CENTER)

        self.error_msg1 = ctk.CTkLabel(self, text='', text_color=PAS_RED,
                                       font=(FONT_REGULAR, 10))
        self.error_msg1.place(relx=0.467, y=400, anchor=ctk.CENTER)

        self.error_msg2 = ctk.CTkLabel(self, text='',
                                       text_color=PAS_GREEN,
                                       font=(FONT_REGULAR, 10))
        self.error_msg2.place(relx=0.568, y=420, anchor=ctk.CENTER)

        self.error_msg3 = ctk.CTkLabel(self, text_color=PAS_RED, text='',
                                       fg_color='transparent',
                                       font=(FONT_REGULAR, 10))
        self.error_msg3.place(relx=0.535, y=440, anchor=ctk.CENTER)

        self.pass_error = ctk.CTkLabel(self, text_color='#b9baba', text='',
                                       font=(FONT_REGULAR, 12))
        self.pass_error.place(relx=0.31, y=380, anchor=ctk.CENTER)

        self.reg_but = ctk.CTkButton(self, text='Sign Up', border_width=0,
                                     fg_color=PAS_GREEN, hover_color=PAS_GREEN_LIGHT,
                                     corner_radius=35, text_color=BLACK, command=self.register_user,
                                     font=(FONT_REGULAR, 16), height=46, width=132)
        self.reg_but.place(relx=0.5, y=420, anchor=ctk.CENTER)

        self.change_to_login_btn = ctk.CTkButton(self, text="Already have a account? Log in!",
                                                 text_color=LIGHT_GREY,
                                                 fg_color=DARK_GREY,
                                                 font=(FONT_REGULAR, 12),
                                                 hover_color=DARK_GREY,
                                                 command=self.change_to_login)
        self.change_to_login_btn.place(relx=0.5, y=472, anchor=ctk.CENTER)


    def register_user(self):
        self.update_frame()

        username = self.username_entry.get()
        password = self.password_entry.get()
        monthly_limit = self.monthly_limit_entry.get()
        daily_limit = self.daily_limit_entry.get()
        currency = self.currency.get()

        if username == '':
            self.show_error('Please enter a username')
            self.username_entry.configure(border_width=1, border_color=PAS_RED)
            return

        if password == '':
            self.show_error('Please enter a password')
            self.password_entry.configure(border_width=1, border_color=PAS_RED)
            return

        if monthly_limit == '':
            self.show_error('Please enter a monthly limit')
            self.monthly_limit_entry.configure(border_width=1, border_color=PAS_RED)
            return

        if daily_limit == '':
            self.show_error('Please enter a daily limit')
            self.daily_limit_entry.configure(border_width=1, border_color=PAS_RED)
            return


        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            temp = []

            print(
                "Password must contain at least 8 characters, including one uppercase, one lowercase, one digit, and one special character.")

            if re.match(r"^([A-Za-z\d@$!%*?&]{8,})", password):
                temp.append(('✓', PAS_GREEN))

            else:
                temp.append(('×', PAS_RED))

            if re.match(r"^(?=.*[A-Z])(?=.*[a-z])", password):
                temp.append(('✓', PAS_GREEN))

            else:
                temp.append(('×', PAS_RED))

            if re.match(r"^(?=.*\d)(?=.*[@$!%*?&])", password):
                temp.append(('✓', PAS_GREEN))

            else:
                temp.append(('×', PAS_RED))

            self.password_error(temp)
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            self.cursor.execute("INSERT INTO users (username, password, monthly_limit, daily_limit, currency) VALUES (?, ?, ?, ?, ?)", (username, hashed_password, monthly_limit, daily_limit, currency[0]))
            self.conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username already exists. Please choose a different username.")
            self.show_error('Username already exists')
            self.username_entry.configure(border_width=1, border_color=PAS_RED)
            return

        success_reg = SuccessfulReg(self.parent)

        self.after(10000, lambda: success_reg.place_forget())

        self.change_to_login()

    def password_error(self, ls):
        self.place_configure(height=580)
        self.reg_but.place_configure(y=503)
        self.change_to_login_btn.place_configure(y=550)
        self.password_entry.configure(border_width=1, border_color=PAS_RED)

        self.pass_error.configure(text="Your password needs to:")
        self.error_msg1.configure(text=f"{ls[0][0]} be at least 8 characters long", text_color=ls[0][1])
        self.error_msg2.configure(text=f"{ls[1][0]} include one uppercase and one lowercase letter",
                                  text_color=ls[1][1])
        self.error_msg3.configure(text=f"{ls[2][0]} have one digit and one special character", text_color=ls[2][1])

    def show_error(self, error):
        self.reg_but.place_configure(y=428)
        self.place_for_error_msg.configure(text=error)

    def change_to_login(self):
        Register.place_forget(self)

    def validate_input(self, value):
        if value.isdigit() or value == "":
            return True
        elif value.count('.') == 1 and value.replace('.', '').isdigit():
            return True
        return False

    def update_frame(self):
        self.place_configure(height=510)
        self.reg_but.place_configure(y=420)
        self.change_to_login_btn.place_configure(y=472)

        self.username_entry.configure(border_width=0)
        self.password_entry.configure(border_width=0)
        self.monthly_limit_entry.configure(border_width=0)
        self.daily_limit_entry.configure(border_width=0)

        self.place_for_error_msg.configure(text='')
        self.error_msg1.configure(text='')
        self.error_msg2.configure(text='')
        self.error_msg3.configure(text='')
        self.pass_error.configure(text='')


class SuccessfulReg(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0, border_color= PAS_GREEN, border_width=1)
        self.place_configure(relx=0.99, rely=0.01, anchor=ctk.NE, width=200, height=75)
        self.label = ctk.CTkLabel(self, text = 'Registration Successful', text_color= PAS_GREEN, font=(FONT_REGULAR, 16))
        self.label.place(relx=0.5, rely = 0.5, anchor=ctk.CENTER)

