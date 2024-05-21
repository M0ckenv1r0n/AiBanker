from login import Login
import sqlite3
from menu import Menu, MajorFrameLower, MajorFrameUpper, MinorFrameUpper, ScrollableFrame
from expense_adding import ExpenseAddingMenu
import customtkinter as ctk
from tkinter import Tk
import requests
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import pandas as pd
from settings import *
import datetime
from banker_frame import MinorFrameLower


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode('Dark')
        self.geometry('1100x600')
        self.title('AI Banker')
        self.minsize(800, 500)
        self.config(background=DARK_DARK_GREY)

        # layout
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=7)
        self.columnconfigure(0, weight=5, uniform='a')
        self.columnconfigure(1, weight=10, uniform='a')
        self.columnconfigure(2, weight=8, uniform='a')

        # initialize login database
        self.login_database()

        # widgets
        self.login = Login(self, self.open_menu, self.login_conn, self.login_cursor)

        # run
        self.mainloop()

    def login_database(self):
        self.login_conn = sqlite3.connect('./databases/user_credentials.db')
        self.login_cursor = self.login_conn.cursor()
        self.login_cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            username TEXT PRIMARY KEY,
                            password TEXT, monthly_limit INTEGER, daily_limit INTEGER, currency TEXT
                        )''')
        self.login_conn.commit()

    def expense_database(self):
        self.expense_conn = sqlite3.connect(f"./databases/{self.username}_expenses.db")
        self.expense_cursor = self.expense_conn.cursor()
        self.expense_cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.username}_expenses (amount INTEGER, category TEXT, date TEXT)")
        self.expense_conn.commit()

    def on_close(self):  # needs to be closed when things are done
        self.login_conn.close()
        self.destroy()
        # self.expense_conn.close()

    def open_menu(self, username):
        # self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.login.place_forget()

        self.username = username

        self.bar_diagram_path = f'./img/temp/bar_diagram_{self.username}.png'
        self.donut_daily_path = f'./img/temp/donut_daily_limit_diagram_{self.username}.png'
        self.donut_monthly_path = f'./img/temp/donut_monthly_limit_diagram_{self.username}.png'

        self.expense_database()

        self.monthly_limit, self.daily_limit, self.currency = self.get_user_data()

        self.menu = Menu(self, self.username, self.open_expense_adding_menu)

        self.major_frame_upper = MajorFrameUpper(self, self.resize_image, self.bar_diagram_path)

        self.major_frame_lower = MajorFrameLower(self, self.expense_conn, self.expense_cursor, self.username,
                                                 self.currency, self.reload_major_scroll)

        self.minor_frame_upper = MinorFrameUpper(self, self.resize_image,self.donut_daily_path, self.donut_monthly_path,  self.currency, self.daily_limit, self.monthly_limit)

        self.minor_frame_lower = MinorFrameLower(self, self.ai_response)

    def resize_image(self, cl, event):

        canvas_ratio = event.width / event.height

        if canvas_ratio > cl.image_ratio:  # canvas is wider than the image
            image_height = int(event.height)
            image_width = int(image_height * cl.image_ratio)

        else:  # canvas is taller
            image_width = int(event.width)
            image_height = int(image_width / cl.image_ratio)

        resized_image = cl.image.resize((image_width, image_height))
        cl.image_tk = ImageTk.PhotoImage(resized_image)

        cl.delete('all')
        cl.create_image(event.width / 2, event.height / 2, image=cl.image_tk)

    def open_expense_adding_menu(self):
        ExpenseAddingMenu(self.menu, self.username, self.save_expense_event, self.expense_conn, self.expense_cursor,
                          self.currency)

    def save_expense_event(self):

        self.reload_major_scroll()

        self.bar_monthly_diagram()
        self.donut_daily_limit()
        self.donut_monthly_limit()

        self.major_frame_upper.grid_forget()
        self.major_frame_upper = MajorFrameUpper(self, self.resize_image, self.bar_diagram_path)

        self.minor_frame_upper.grid_forget()
        self.minor_frame_upper = MinorFrameUpper(self, self.resize_image,
                                                 self.donut_daily_path, self.donut_monthly_path,  self.currency, self.daily_limit, self.monthly_limit)

    def bar_monthly_diagram(self):

        query = f"""
            SELECT DATE(date, 'start of month') AS month, category, SUM(amount) AS total_amount
            FROM {self.username}_expenses
            GROUP BY month, category
        """

        df = pd.read_sql_query(query, self.expense_conn)

        df['month'] = pd.to_datetime(df['month'], format='%Y-%m-%d')

        df_pivot = df.pivot_table(index='month', columns='category', values='total_amount', fill_value=0)

        color_map = {category: OPTION_DICT[category] for category in df['category'].unique()}

        fig, ax = plt.subplots(facecolor=DARK_GREY)

        fig.set_figwidth(476 * 0.0104)
        fig.set_figheight(258 * 0.0104)

        ax.set_facecolor(DARK_GREY)
        ax.spines['bottom'].set_color(WHITE)
        ax.spines['top'].set_color(WHITE)
        ax.spines['left'].set_color(WHITE)
        ax.spines['right'].set_color(WHITE)
        ax.tick_params(axis='x', colors=WHITE)
        ax.tick_params(axis='y', colors=WHITE)
        ax.yaxis.label.set_color(WHITE)
        ax.xaxis.label.set_color(WHITE)
        ax.title.set_color(WHITE)

        df_pivot.plot(kind='bar', stacked=True, width=0.8, color=[color_map.get(x, 'gray') for x in df_pivot.columns],
                      ax=ax)

        ax.set_xticklabels([d.strftime('%b %Y') for d in df_pivot.index])
        plt.xticks(rotation=0)

        ax.set_xlabel('')
        ax.set_ylabel('')

        plt.legend(fontsize="8", loc="upper right")
        plt.tight_layout()

        fig.savefig(self.bar_diagram_path, format='png', facecolor=DARK_GREY, edgecolor=DARK_GREY)

    def donut_daily_limit(self):
        today = datetime.date.today().strftime('%Y-%m-%d')

        query = f"SELECT category, SUM(amount) AS total_amount FROM {self.username}_expenses WHERE date = ? GROUP BY category"
        self.expense_cursor.execute(query, (today,))
        data = self.expense_cursor.fetchall()

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        daily_limit = self.daily_limit
        total_spent = sum(amounts)
        remaining_amount = max(0, daily_limit - total_spent)

        if remaining_amount > 0:
            amounts.append(remaining_amount)
            categories.append('Remaining')

        colors = [OPTION_DICT.get(category, GREY) for category in categories]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(amounts, colors=colors, startangle=90, wedgeprops=dict(width=0.4))

        center_circle = plt.Circle((0, 0), 0.6, fc=DARK_DARK_GREY)
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        legend_labels = [f"{category}: {amount:.2f}{self.currency}" for category, amount in zip(categories, amounts)]
        legend = plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(-0.35, 1), fontsize=17)
        legend.get_frame().set_facecolor(DARK_DARK_GREY)
        for text in legend.get_texts():
            text.set_color(WHITE)

        fig.patch.set_facecolor(DARK_DARK_GREY)
        ax.set_facecolor(DARK_DARK_GREY)

        ax.axis('off')

        plt.tight_layout()

        fig.savefig(self.donut_daily_path, format='png')
        plt.show()


    def donut_monthly_limit(self):

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        query = f"SELECT category, SUM(amount) AS total_amount FROM {self.username}_expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? GROUP BY category"
        self.expense_cursor.execute(query, (str(current_month).zfill(2), str(current_year)))
        data = self.expense_cursor.fetchall()

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        monthly_limit = self.monthly_limit
        total_spent = sum(amounts)
        remaining_amount = max(0, monthly_limit - total_spent)

        if remaining_amount > 0:
            amounts.append(remaining_amount)
            categories.append('Remaining')

        colors = [OPTION_DICT.get(category, 'gray') for category in categories]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(amounts, colors=colors, startangle=90, wedgeprops=dict(width=0.4))

        center_circle = plt.Circle((0, 0), 0.6, fc=DARK_DARK_GREY)
        fig = plt.gcf()
        fig.gca().add_artist(center_circle)

        legend_labels = [f"{category}: ${amount:.2f}{self.currency}" for category, amount in zip(categories, amounts)]
        legend = plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(-0.35, 1), fontsize=17)
        legend.get_frame().set_facecolor(DARK_DARK_GREY)
        for text in legend.get_texts():
            text.set_color(WHITE)

        fig.patch.set_facecolor(DARK_DARK_GREY)
        ax.set_facecolor(DARK_DARK_GREY)

        ax.axis('off')

        plt.tight_layout()
        fig.savefig(self.donut_monthly_path, format='png')
        plt.show()

    def get_user_data(self):
        self.login_cursor.execute('''SELECT monthly_limit FROM users WHERE username = ?''', (self.username,))
        monthly_limit = self.login_cursor.fetchone()[0]

        self.login_cursor.execute('''SELECT daily_limit FROM users WHERE username = ?''', (self.username,))
        daily_limit = self.login_cursor.fetchone()[0]

        self.login_cursor.execute("SELECT currency FROM users WHERE username = ?", (self.username,))
        currency = self.login_cursor.fetchone()[0]

        return monthly_limit, daily_limit, currency

    def ai_response (self, user_input):
        ngrokURL = 'https://7b92-34-41-211-145.ngrok-free.app'

        question = f'Your Profile: Advanced Finance Analytics and Banker. Your Experience: 15+ years in finance, specializing in analytics and banking services. Expert in financial modeling, risk management, and investment strategies. Extensive background in advising on mergers, acquisitions, and capital market trends. Your Skills: Financial Modeling and Analysis: Proficient in creating predictive models for market trends and investment opportunities. Utilizes advanced statistical tools and software to analyze large datasets. Investment Advisory: Offers insights into stocks, bonds, and alternative investments. Provides tailored advice on portfolio management to optimize risk-return ratios. Risk Management: Develops strategies to minimize financial risks. Expert in identifying market vulnerabilities and advising on hedging strategies. Regulatory Compliance: Deep understanding of global financial regulations, including Basel III, Dodd-Frank, and MiFID II. Advises companies on compliance best practices and regulatory reporting. Client Relationship Management: Experienced in handling high-net-worth individual portfolios, understanding client needs, and providing exceptional advisory services. Objective: To assist users with comprehensive financial insights and strategic advice to navigate complex financial landscapes effectively. Committed to leveraging expertise in analytics and banking to provide accurate forecasts, investment recommendations, and risk assessment. Answer user question: {user_input}'
        # Define the data to send in the POST request
        data = {
            "inputs": '''
                    Your Profile: Advanced Finance Analytics and Banker

                    Your Experience: 15+ years in finance, specializing in analytics and banking services. Expert in financial modeling, risk management, and investment strategies. Extensive background in advising on mergers, acquisitions, and capital market trends.

                    Your Skills:

                    Financial Modeling and Analysis: Proficient in creating predictive models for market trends and investment opportunities. Utilizes advanced statistical tools and software to analyze large datasets.
                    Investment Advisory: Offers insights into stocks, bonds, and alternative investments. Provides tailored advice on portfolio management to optimize risk-return ratios.
                    Risk Management: Develops strategies to minimize financial risks. Expert in identifying market vulnerabilities and advising on hedging strategies.
                    Regulatory Compliance: Deep understanding of global financial regulations, including Basel III, Dodd-Frank, and MiFID II. Advises companies on compliance best practices and regulatory reporting.
                    Client Relationship Management: Experienced in handling high-net-worth individual portfolios, understanding client needs, and providing exceptional advisory services.
                    Objective: To assist users with comprehensive financial insights and strategic advice to navigate complex financial landscapes effectively. Committed to leveraging expertise in analytics and banking to provide accurate forecasts, investment recommendations, and risk assessment.
                    Answer user' question: Give me some tips about saving money

        ''',
            # paramaters can be found here https://abetlen.github.io/llama-cpp-python/#llama_cpp.llama.Llama.create_completion
            "parameters": {"temperature": 0.1,
                           "max_tokens": 200}
            # higher temperature, more creative response is, lower more precise
            # max_token is the max amount of (simplified) "words" allowed to be generated
        }

        # Send the POST request
        response = requests.post(ngrokURL + "/generate/", json=data)

        # Check the response
        if response.status_code == 200:
            result = response.json()
            print("Generated Text:\n", data["inputs"], result["generated_text"].strip())

            response = result["generated_text"].strip()

            formatted = ''

            for i in response:
                if i != '*':
                    formatted += i

            return formatted

        else:
            print("Request failed with status code:", response.status_code)

    def reload_major_scroll(self): #needs to be fixed, the worst solution ever
        self.major_frame_lower.destroy()
        self.major_frame_lower = MajorFrameLower(self, self.expense_conn, self.expense_cursor, self.username,
                                                 self.currency, self.reload_major_scroll)


App()