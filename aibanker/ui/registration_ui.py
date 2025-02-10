#REF

import re
import customtkinter as ctk
from typing import List, Tuple
from aibanker.config_files.config_ui import *
from aibanker.config_files.config import CURRENCY_DICT
from aibanker.ui.share.notification_frame import NotifFrame
import logging

logger = logging.getLogger(__name__)


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, user_service: any) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.parent = parent
        self.user_service = user_service
        self.place_configure(relx=0.5, rely=0.5, anchor=ctk.CENTER, width=430, height=510)
        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self) -> None:
        self.validate_command = self.register(self.validate_input)
        self.register_label = ctk.CTkLabel(
            self, text="SIGN UP", font=(FONT_REGULAR, 48), text_color=WHITE
        )
        self.minor_reg_label = ctk.CTkLabel(
            self,
            text="Please enter your future username and password!",
            text_color=LIGHT_GREY,
            font=(FONT_REGULAR, 14),
        )
        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Username",
            border_width=0,
            fg_color=GREY,
            corner_radius=25,
            width=240,
            height=40,
            font=(FONT_REGULAR, 16),
        )
        self.password_entry = ctk.CTkEntry(
            self,
            show="*",
            placeholder_text="Password",
            fg_color=GREY,
            border_width=0,
            corner_radius=25,
            width=240,
            height=40,
            font=(FONT_REGULAR, 16),
        )
        self.set_currency_label = ctk.CTkLabel(
            self, text="Set your currency:", font=(FONT_REGULAR, 16), text_color="#b9baba"
        )
        self.currency = ctk.CTkOptionMenu(
            self,
            fg_color=GREY,
            font=(FONT_REGULAR, 14),
            corner_radius=25,
            height=28,
            width=72,
            values=[f"{value}  {key}" for key, value in CURRENCY_DICT.items()],
            button_color=GREY,
            button_hover_color=DARK_DARK_GREY,
            dynamic_resizing=False,
        )
        self.daily_limit_label = ctk.CTkLabel(
            self, text="Set your daily limit:", font=(FONT_REGULAR, 16), text_color="#b9baba"
        )
        self.monthly_budget_label = ctk.CTkLabel(
            self, text="Set your monthly limit:", font=(FONT_REGULAR, 16), text_color="#b9baba"
        )
        self.daily_limit_entry = ctk.CTkEntry(
            self,
            validate="key",
            placeholder_text="Enter your daily limit",
            border_width=0,
            fg_color=GREY,
            corner_radius=25,
            validatecommand=(self.validate_command, "%P"),
            width=120,
            height=28,
            font=(FONT_REGULAR, 12),
        )
        self.monthly_limit_entry = ctk.CTkEntry(
            self,
            validate="key",
            placeholder_text="Enter your monthly budget",
            border_width=0,
            fg_color=GREY,
            corner_radius=25,
            validatecommand=(self.validate_command, "%P"),
            width=120,
            height=28,
            font=(FONT_REGULAR, 12),
        )
        self.place_for_error_msg = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, fg_color="transparent", font=(FONT_REGULAR, 12)
        )
        self.error_msg1 = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, font=(FONT_REGULAR, 10)
        )
        self.error_msg2 = ctk.CTkLabel(
            self, text="", text_color=PAS_GREEN, font=(FONT_REGULAR, 10)
        )
        self.error_msg3 = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, fg_color="transparent", font=(FONT_REGULAR, 10)
        )
        self.pass_error = ctk.CTkLabel(
            self, text="", text_color="#b9baba", font=(FONT_REGULAR, 12)
        )
        self.reg_but = ctk.CTkButton(
            self,
            text="Sign Up",
            border_width=0,
            fg_color=PAS_GREEN,
            hover_color=PAS_GREEN_LIGHT,
            corner_radius=35,
            text_color=BLACK,
            command=self.register_user,
            font=(FONT_REGULAR, 16),
            height=46,
            width=132,
        )
        self.change_to_login_btn = ctk.CTkButton(
            self,
            text="Already have an account? Log in!",
            text_color=LIGHT_GREY,
            fg_color=DARK_GREY,
            font=(FONT_REGULAR, 12),
            hover_color=DARK_GREY,
            command=self.change_to_login,
        )

    def _place_widgets(self) -> None:
        self.register_label.place(relx=0.5, y=53.5, anchor=ctk.CENTER)
        self.minor_reg_label.place(relx=0.5, y=94, anchor=ctk.CENTER)
        self.username_entry.place(relx=0.5, y=145, anchor=ctk.CENTER)
        self.password_entry.place(relx=0.5, y=200, anchor=ctk.CENTER)
        self.set_currency_label.place(relx=0.456, y=262.7, anchor=ctk.E)
        self.currency.place(relx=0.625, y=262.7, anchor=ctk.W)
        self.monthly_budget_label.place(relx=0.335, y=298.4, anchor=ctk.CENTER)
        self.monthly_limit_entry.place(relx=0.705, y=298.4, anchor=ctk.CENTER)
        self.daily_limit_label.place(relx=0.31, y=334, anchor=ctk.CENTER)
        self.daily_limit_entry.place(relx=0.705, y=334, anchor=ctk.CENTER)
        self.place_for_error_msg.place(relx=0.5, y=380, anchor=ctk.CENTER)
        self.error_msg1.place(relx=0.467, y=400, anchor=ctk.CENTER)
        self.error_msg2.place(relx=0.568, y=420, anchor=ctk.CENTER)
        self.error_msg3.place(relx=0.535, y=440, anchor=ctk.CENTER)
        self.pass_error.place(relx=0.31, y=380, anchor=ctk.CENTER)
        self.reg_but.place(relx=0.5, y=420, anchor=ctk.CENTER)
        self.change_to_login_btn.place(relx=0.5, y=472, anchor=ctk.CENTER)

    def register_user(self) -> None:
        self.update_frame()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        monthly_limit_str = self.monthly_limit_entry.get().strip()
        daily_limit_str = self.daily_limit_entry.get().strip()
        currency = self.currency.get().strip()

        if not username:
            self.show_error("Please enter a username")
            self.username_entry.configure(border_width=1, border_color=PAS_RED)
            return
        if not password:
            self.show_error("Please enter a password")
            self.password_entry.configure(border_width=1, border_color=PAS_RED)
            return
        if not monthly_limit_str:
            self.show_error("Please enter a monthly limit")
            self.monthly_limit_entry.configure(border_width=1, border_color=PAS_RED)
            return
        if not daily_limit_str:
            self.show_error("Please enter a daily limit")
            self.daily_limit_entry.configure(border_width=1, border_color=PAS_RED)
            return

        try:
            daily_limit = float(daily_limit_str)
            monthly_limit = float(monthly_limit_str)
        except ValueError:
            self.monthly_limit_entry.configure(border_width=1, border_color=PAS_RED)
            self.daily_limit_entry.configure(border_width=1, border_color=PAS_RED)
            self.show_error("Daily/Monthly limits must be numeric.")
            return

        if daily_limit > monthly_limit:
            self.show_error("Your daily limit cannot exceed your monthly budget")
            self.daily_limit_entry.configure(border_width=1, border_color=PAS_RED)
            return

        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password):
            self._handle_password_error(password)
            return

        logger.info("Attempting registration for user '%s'", username)
        success = self.user_service.register_user(
            username=username,
            plain_password=password,
            daily_limit=daily_limit,
            monthly_limit=monthly_limit,
            currency=currency,
        )
        if success:
            logger.info("User '%s' registered successfully", username)
            NotifFrame(self.parent, "positive", "Registration Successful")
            self.change_to_login()
        else:
            logger.warning("Registration failed for user '%s'", username)
            self.show_error(f"Username '{username}' is already taken")
            self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def change_to_login(self) -> None:
        RegisterFrame.place_forget(self)

    def validate_input(self, value: str) -> bool:
        return value == "" or value.isdigit() or (value.count(".") == 1 and value.replace(".", "").isdigit())

    def show_error(self, message: str) -> None:
        self.reg_but.place_configure(y=428)
        self.place_for_error_msg.configure(text=message)

    def _handle_password_error(self, password: str) -> None:
        checks: List[Tuple[str, str]] = []
        checks.append(("✓", PAS_GREEN) if re.match(r"^([A-Za-z\d@$!%*?&]{8,})", password) else ("×", PAS_RED))
        checks.append(("✓", PAS_GREEN) if re.match(r"^(?=.*[A-Z])(?=.*[a-z])", password) else ("×", PAS_RED))
        checks.append(("✓", PAS_GREEN) if re.match(r"^(?=.*\d)(?=.*[@$!%*?&])", password) else ("×", PAS_RED))
        self.password_error(checks)

    def password_error(self, checks: List[Tuple[str, str]]) -> None:
        self.place_configure(height=580)
        self.reg_but.place_configure(y=503)
        self.change_to_login_btn.place_configure(y=550)
        self.password_entry.configure(border_width=1, border_color=PAS_RED)
        self.pass_error.configure(text="Your password needs to:")
        self.error_msg1.configure(text=f"{checks[0][0]} be at least 8 characters long", text_color=checks[0][1])
        self.error_msg2.configure(text=f"{checks[1][0]} include one uppercase and one lowercase letter", text_color=checks[1][1])
        self.error_msg3.configure(text=f"{checks[2][0]} have one digit and one special character", text_color=checks[2][1])

    def update_frame(self) -> None:
        self.place_configure(height=510)
        self.reg_but.place_configure(y=420)
        self.change_to_login_btn.place_configure(y=472)
        self.username_entry.configure(border_width=0)
        self.password_entry.configure(border_width=0)
        self.monthly_limit_entry.configure(border_width=0)
        self.daily_limit_entry.configure(border_width=0)
        self.place_for_error_msg.configure(text="")
        self.error_msg1.configure(text="")
        self.error_msg2.configure(text="")
        self.error_msg3.configure(text="")
        self.pass_error.configure(text="")
