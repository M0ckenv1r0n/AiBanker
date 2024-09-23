import customtkinter as ctk
from settings import *
from PIL import Image


class MinorFrameLower(ctk.CTkFrame):
    def __init__(self, parent, ai_response):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY,
                         border_width=0, corner_radius=0)
        self.grid(column=2, row=1, sticky='nsew')

        self.ai_response = ai_response

        self.name_label = ctk.CTkLabel(self, text="AI Adviser", font=(FONT_REGULAR, 18),
                                       text_color=BLACK, fg_color=PAS_PURPLE, corner_radius=18, height=35)
        self.name_label.place(relx=0.5, rely=0.06, anchor=ctk.CENTER)
        self.scrollable_frame = MinorFrameLowerScrollable(self)
        self.send_icon = ctk.CTkImage(light_image=Image.open("img/icons/send_icon.png"),
                                      size=(20, 20))

        self.user_input_entry = ctk.CTkEntry(self, font=(FONT_REGULAR, 14), placeholder_text='Type your question',
                                             fg_color=GREY, height=35, border_width=0)

        self.user_input_entry.bind('<KeyRelease>', self.on_key_release)

        self.user_input_entry.bind('<Return>', self.get_user_input)

        self.user_input_entry.place(relx=0.49, rely=0.95, anchor=ctk.CENTER, relwidth=0.79)

        self.send_button = ctk.CTkButton(self.user_input_entry, text='', image=self.send_icon,
                                         command=self.get_user_input, fg_color=GREY, hover_color=DARK_DARK_GREY,
                                         width=20, height=20)
        self.send_button.place(relx=0.921, rely=0.49, anchor=ctk.CENTER)

    def on_key_release(self, event):
        if len(self.user_input_entry.get()) > 0:
            self.send_button.configure(state='normal')
            self.send_button.configure(fg_color=DARK_DARK_GREY)
        else:
            self.send_button.configure(state='disabled')
            self.send_button.configure(fg_color=GREY)

    def get_user_input(self, event=None):
        user_input = self.user_input_entry.get()

        if user_input == '':
            return

        self.send_button.configure(state='disabled')

        self.user_input_entry.delete(0, 'end')
        UserInputFrame(self.scrollable_frame, user_input)

        response = self.ai_response(user_input)

        if response is not None:
            AiAnswerFrame(self.scrollable_frame, response)

        else:
            AiAnswerFrame(self.scrollable_frame, 'Request failed')

        self.scrollable_frame._parent_canvas.yview_moveto(1.0)  # scrolls to the bottom




class MinorFrameLowerScrollable(ctk.CTkScrollableFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY, border_width=0, corner_radius=0)
        self.place(relx=0.5, rely=0.52, relwidth=1,
                   relheight=0.8, anchor=ctk.CENTER)
        self.ai_answer_frame = AiAnswerFrame(self, "Hey!\nHow can I assist you today?")


class AiAnswerFrame(ctk.CTkFrame):
    def __init__(self, parent, response):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY,
                         border_width=0, corner_radius=10)
        self.pack(pady=5, anchor='w')

        self.label_banker = ctk.CTkLabel(self, text='Banker', text_color=WHITE, font=(FONT_REGULAR, 14))
        self.label_banker.pack(pady=0, anchor='w', padx=50)

        self.banker_answer_frame = AiAnswerSubFrame(self,response)

        self.banker_photo = ctk.CTkImage(light_image=Image.open("img/icons/banker_icon.png"),
                                         size=(42, 42))
        self.banker = ctk.CTkLabel(self, image=self.banker_photo, text='', fg_color=DARK_DARK_GREY, width=32, height=32,
                                   corner_radius=0)
        self.banker.place(relx=0.02, rely=0.02)


class AiAnswerSubFrame(ctk.CTkFrame):
    def __init__(self, parent, response):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=15)
        self.pack(padx=(25, 1), pady=(0, 10))
        self.textbox = ctk.CTkTextbox(self, activate_scrollbars=False, font=(FONT_REGULAR, 11), fg_color=DARK_GREY,
                                      border_spacing=1, wrap='word')
        self.insert_text(response)
        self.textbox.configure(state='disabled')
        lines = int(self.textbox.index('end-1c').split('.')[0])+1
        print(lines)
        self.textbox.pack(padx=(30, 10), pady=(15, 0), fill='x')
        self.textbox.configure(height=15 * lines)

        self.copy_icon = ctk.CTkImage(light_image=Image.open(
            "./img/icons/copy_icon.png"), size=(18, 18))

        self.copy_btn = ctk.CTkButton(self, text='Copy', font=(FONT_REGULAR, 12), width=80,
                                      height=30, image=self.copy_icon, corner_radius=10, fg_color=DARK_DARK_GREY,
                                      hover_color=GREY, command=self.copy)
        self.copy_btn.pack(anchor='e', padx=10, pady=10)

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('0.0', ctk.END))

    def insert_text(self, text):
        chunk_size = 35
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end >= len(text):
                end = len(text)
            else:
                while end > start and text[end] != ' ':
                    end -= 1
            self.textbox.insert(ctk.END, text[start:end].strip())
            if end != len(text):  # Avoid adding newline for the last chunk
                self.textbox.insert(ctk.END, '\n')
            start = end


class UserInputFrame(ctk.CTkFrame):
    def __init__(self, parent, user_input):
        super().__init__(master=parent, fg_color=DARK_DARK_GREY,
                         border_width=0, corner_radius=10)
        self.pack(pady=5, anchor='e')

        self.label_user = ctk.CTkLabel(
            self, text='You', text_color=WHITE, font=(FONT_REGULAR, 14))
        self.label_user.pack(pady=0, anchor='e', padx=50)

        self.user_answer_frame = UserInputSubFrame(self, user_input)

        self.user_photo = ctk.CTkImage(light_image=Image.open("img/icons/user_icon.png"),
                                       size=(42, 42))
        self.user = ctk.CTkLabel(self, image=self.user_photo, text='', fg_color=DARK_DARK_GREY, width=32, height=32,
                                 corner_radius=0)
        self.user.place(relx=0.82, rely=0.01)


class UserInputSubFrame(ctk.CTkFrame):
    def __init__(self, parent, user_input):
        super().__init__(master=parent, fg_color='green', corner_radius=15)
        self.pack(padx=(1, 25), pady=(0, 10))
        self.textbox = ctk.CTkTextbox(self, activate_scrollbars=False, font=(FONT_REGULAR, 11), fg_color=DARK_GREY,
                                      border_spacing=0, wrap='word')
        self.insert_text(user_input)
        self.textbox.configure(state='disabled')
        lines = int(self.textbox.index('end-1c').split('.')[0])+1
        print(lines)
        self.textbox.pack(padx=(10, 30), pady=(15, 0), expand=True, fill='x')
        self.textbox.configure(height=15 * lines)



        self.copy_icon = ctk.CTkImage(light_image=Image.open(
            "./img/icons/copy_icon.png"), size=(18, 18))

        self.copy_btn = ctk.CTkButton(self, text='Copy', font=(FONT_REGULAR, 12), width=80,
                                      height=30, image=self.copy_icon, corner_radius=10, fg_color=DARK_DARK_GREY,
                                      hover_color=GREY, command=self.copy)
        self.copy_btn.pack(anchor='w', padx=10, pady=10)

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.textbox.get('0.0', ctk.END))

    def insert_text(self, text):
        chunk_size = 35
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end >= len(text):
                end = len(text)
            else:
                while end > start and text[end] != ' ':
                    end -= 1
            self.textbox.insert(ctk.END, text[start:end].strip())
            if end != len(text):  # Avoid adding newline for the last chunk
                self.textbox.insert(ctk.END, '\n')
            start = end
