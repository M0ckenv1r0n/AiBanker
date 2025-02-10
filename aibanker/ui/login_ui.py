#REF

from typing import Any, Callable
import customtkinter as ctk
from aibanker.config_files.config_ui import *
from aibanker.ui.registration_ui import RegisterFrame
import logging

logger = logging.getLogger(__name__)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTkFrame, user_service: Any, on_login_success: Callable[[str], None]) -> None:
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=0)
        self.parent = parent
        self.user_service = user_service
        self.on_login_success = on_login_success

        self.place_configure(relx=0.5, rely=0.5, anchor=ctk.CENTER, width=430, height=410)
        self._create_widgets()
        self._place_widgets()

    def _create_widgets(self) -> None:
        self.login_label = ctk.CTkLabel(
            self, text="LOGIN", font=(FONT_REGULAR, 48), text_color=WHITE
        )
        self.minor_login_label = ctk.CTkLabel(
            self,
            text="Please enter your username and password!",
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
            height=42,
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
            height=42,
            font=(FONT_REGULAR, 16),
        )
        self.error_msg = ctk.CTkLabel(
            self, text="", text_color=PAS_RED, fg_color="transparent", font=(FONT_REGULAR, 12)
        )
        self.login_btn = ctk.CTkButton(
            self,
            text="Log In",
            border_width=0,
            command=self.handle_login,
            fg_color=PAS_GREEN,
            hover_color=PAS_GREEN_LIGHT,
            corner_radius=35,
            text_color=BLACK,
            font=(FONT_REGULAR, 16),
            height=46,
            width=132,
        )
        self.change_to_register_btn = ctk.CTkButton(
            self,
            text="Don't have an account? Sign Up",
            text_color=LIGHT_GREY,
            fg_color=DARK_GREY,
            command=self.change_to_register,
            font=(FONT_REGULAR, 12),
            hover_color=DARK_GREY,
        )

    def _place_widgets(self) -> None:
        self.login_label.place(relx=0.5, rely=0.17, anchor=ctk.CENTER)
        self.minor_login_label.place(relx=0.5, rely=0.285, anchor=ctk.CENTER)
        self.username_entry.place(relx=0.5, rely=0.42, anchor=ctk.CENTER)
        self.password_entry.place(relx=0.5, rely=0.57, anchor=ctk.CENTER)
        self.error_msg.place(relx=0.5, rely=0.66, anchor=ctk.CENTER)
        self.login_btn.place(relx=0.5, rely=0.795, anchor=ctk.CENTER)
        self.change_to_register_btn.place(relx=0.5, rely=0.91, anchor=ctk.CENTER)

    def handle_login(self) -> None:
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            self.show_error("Username and password cannot be empty.")
            return
        logger.info("Attempting login for user: %s", username)
        if self.user_service.authenticate(username, password):
            logger.info("User '%s' logged in successfully.", username)
            self.on_login_success(username)
        else:
            logger.warning("Authentication failed for user: %s", username)
            self.show_error("Invalid username or password")


    def show_error(self, err_msg: str) -> None:
        self.error_msg.configure(text=err_msg)
        self.password_entry.configure(border_width=1, border_color=PAS_RED)
        self.username_entry.configure(border_width=1, border_color=PAS_RED)

    def change_to_register(self) -> None:
        logger.info("Switching to registration screen.")
        RegisterFrame(parent=self.parent, user_service=self.user_service)