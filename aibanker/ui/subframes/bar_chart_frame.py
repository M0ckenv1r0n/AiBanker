from aibanker.config_files.config_ui import *

from tkinter import Canvas
from PIL import ImageTk, Image

from typing import Any


class BarChartFrame(Canvas):
    def __init__(self, parent, plain_image: Image):
        super().__init__(master=parent, background=DARK_GREY, bd=0, highlightthickness=0, relief='ridge')
        self.grid(column=1, row=0, sticky='nsew')

        self.image = plain_image
        self.image_ratio = self.image.size[0] / self.image.size[1]

        self.bind('<Configure>', self.img_configure)

    def img_configure(self, event):
        canvas_ratio = event.width / event.height

        if canvas_ratio > self.image_ratio:  # canvas is wider than the image
            image_height = int(event.height)
            image_width = int(image_height * self.image_ratio)

        else:  # canvas is taller
            image_width = int(event.width)
            image_height = int(image_width / self.image_ratio)

        resized_image = self.image.resize((image_width, image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)

        self.delete('all')
        self.create_image(event.width / 2, event.height / 2, image=self.image_tk)




