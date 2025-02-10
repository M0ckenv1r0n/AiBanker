

import customtkinter as ctk
from aibanker.config_files.config_ui import *
from tkinter import Canvas
from PIL import Image, ImageTk
from typing import Any

class DonutChartFrame(ctk.CTkFrame):
    def __init__(self, parent, daily_limit: float, monthly_limit: float, plain_image_daily: Image.Image, plain_image_monthly: Image.Image, currency:str):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, corner_radius=0)
        self.grid(column=2, row=0, sticky='nsew')
        self.daily_limit = daily_limit
        self.monthly_limit = monthly_limit
        self.currency = currency

        self.plain_image_daily = plain_image_daily
        self.plain_image_monthly = plain_image_monthly

        self.donut_diagram = DonutDiagram(self, self.plain_image_daily)

        self.daily_donut_btn = ctk.CTkButton(
            self,
            text='Daily',
            fg_color='transparent',
            height=18,
            width=140,
            hover_color=GREY,
            font=(FONT_REGULAR, 14),
            text_color=WHITE,
            corner_radius=10,
            state="disabled",
            command=self.change_to_daily
        )
        self.daily_donut_btn.place(relx=0.25, rely=0.92, anchor=ctk.CENTER)

        # Create the Monthly button.
        self.monthly_donut_btn = ctk.CTkButton(
            self,
            text='Monthly',
            fg_color='transparent',
            height=18,
            width=140,
            font=(FONT_REGULAR, 14),
            hover_color=GREY,
            text_color=WHITE,
            corner_radius=10,
            command=self.change_to_monthly
        )
        self.monthly_donut_btn.place(relx=0.74, rely=0.92, anchor=ctk.CENTER)

        self.settings_btn = ctk.CTkButton(
            self,
            text=f"⚙️ Daily Limit: {self.daily_limit}{self.currency}",
            font=(FONT_REGULAR, 9),
            width=16,
            height=16,
            fg_color='transparent',
            hover_color=GREY,
            text_color=WHITE
        )
        self.settings_btn.place(relx=0.82, rely=0.15, anchor=ctk.CENTER)

    def change_to_monthly(self) -> None:
        self.settings_btn.configure(text=f"⚙️ Monthly Limit: {self.monthly_limit}{self.currency}")
        self.donut_diagram.update_image(self.plain_image_monthly)
        self.monthly_donut_btn.configure(state="disabled")
        self.daily_donut_btn.configure(state="normal")

    def change_to_daily(self) -> None:
        self.settings_btn.configure(text=f"⚙️ Daily Limit: {self.daily_limit}{self.currency}")
        self.donut_diagram.update_image(self.plain_image_daily)
        self.daily_donut_btn.configure(state="disabled")
        self.monthly_donut_btn.configure(state="normal")



class DonutDiagram(Canvas):
    def __init__(self, parent, plain_image: Image):
        super().__init__(master=parent, background=DARK_DARK_GREY, bd=0, highlightthickness=0, relief='ridge')
        self.place(relx=0.5, rely=0.512, relwidth=1, relheight=0.9, anchor=ctk.CENTER)
        self.image = plain_image
        self.image_ratio = self.image.size[0] / self.image.size[1]
        self.bind('<Configure>', self.img_configure)

    def img_configure(self, event) -> None:
        """
        Resizes the stored image to fit the current canvas dimensions and redraws it.
        """
        canvas_ratio = event.width / event.height
        if canvas_ratio > self.image_ratio:  # canvas is wider than the image
            image_height = int(event.height)
            image_width = int(image_height * self.image_ratio)
        else:  # canvas is taller than the image
            image_width = int(event.width)
            image_height = int(image_width / self.image_ratio)
        resized_image = self.image.resize((image_width, image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.delete('all')
        self.create_image(event.width / 2, event.height / 2, image=self.image_tk)

    def update_image(self, new_image: Image) -> None:
        """
        Updates the diagram's image with new_image and redraws the canvas.
        """
        self.image = new_image
        self.image_ratio = self.image.size[0] / self.image.size[1]
        # Force an update by calling the resize logic.
        width = self.winfo_width() or 1
        height = self.winfo_height() or 1
        # Create a dummy event-like object with width and height attributes.
        class DummyEvent:
            pass
        dummy = DummyEvent()
        dummy.width = width
        dummy.height = height
        self.img_configure(dummy)
