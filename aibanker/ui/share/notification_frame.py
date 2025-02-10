import customtkinter as ctk
from aibanker.config_files.config_ui import *
from typing import Literal


class NotifFrame(ctk.CTkFrame):
    def __init__(self, parent, sentiment: Literal["positive", "negative"], text: str) -> None:
        background_colour = PAS_GREEN if sentiment == "positive" else PAS_RED

        super().__init__(master=parent, fg_color=background_colour, border_width=0)
        self.place_configure(relx=0.99, rely=0.01,
                             anchor=ctk.NE, width=300, height=70)
        self.label = ctk.CTkLabel(
            self, text=text, text_color=DARK_GREY, font=(FONT_REGULAR, 20))
        self.label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Hide notification after 1s
        self.after(1000, lambda: self.place_forget())