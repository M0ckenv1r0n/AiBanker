# draw_expense_vs_monthly_limit_donut

import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from PIL import Image
from datetime import datetime


from aibanker.config_files.config_ui import *
from aibanker.config_files.config import OPTION_DICT

class DiagramDrawer:

    def __init__(self) -> None:

        plt.switch_backend("Agg")

    def monthly_bar_diagram(self, records) -> Image:
        if not records:
            # Create an empty plot with a message "Add your first expense"
            fig, ax = plt.subplots(facecolor=DARK_GREY)
            fig.set_figwidth(476 * 0.0104)
            fig.set_figheight(258 * 0.0104)
            ax.set_facecolor(DARK_GREY)
            for spine in ax.spines.values():
                spine.set_color(WHITE)
            ax.tick_params(axis='x', colors=WHITE)
            ax.tick_params(axis='y', colors=WHITE)
            ax.xaxis.label.set_color(WHITE)
            ax.yaxis.label.set_color(WHITE)
            ax.title.set_color(WHITE)
            # Place the message in the center of the plot
            ax.text(
                0.5, 0.5, "Add your first expense",
                transform=ax.transAxes,
                color=WHITE,
                fontsize=14,
                ha='center',
                va='center'
            )
            plt.tight_layout()
            buf = BytesIO()
            plt.savefig(buf, format='png', facecolor=DARK_GREY, edgecolor=DARK_GREY)
            plt.close(fig)
            buf.seek(0)
            return Image.open(buf)
        
        # If records exist, proceed to generate the monthly bar diagram
        df = pd.DataFrame(records, columns=['id', 'username', 'amount', 'category', 'description', 'date'])
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['month'] = df['date'].dt.to_period('M').dt.to_timestamp()
        
        df_pivot = df.pivot_table(index='month', columns='category', values='amount', aggfunc='sum', fill_value=0)
        
        unique_categories = df['category'].unique()
        color_map = {category: OPTION_DICT.get(category, 'gray') for category in unique_categories}
        
        fig, ax = plt.subplots(facecolor=DARK_GREY)
        fig.set_figwidth(476 * 0.0104)
        fig.set_figheight(258 * 0.0104)
        
        ax.set_facecolor(DARK_GREY)
        for spine in ax.spines.values():
            spine.set_color(WHITE)
        ax.tick_params(axis='x', colors=WHITE)
        ax.tick_params(axis='y', colors=WHITE)
        ax.xaxis.label.set_color(WHITE)
        ax.yaxis.label.set_color(WHITE)
        ax.title.set_color(WHITE)
        
        df_pivot.plot(
            kind='bar',
            stacked=True,
            width=0.8,
            color=[color_map.get(x, 'gray') for x in df_pivot.columns],
            ax=ax
        )
        
        ax.set_xticklabels([d.strftime('%b %Y') for d in df_pivot.index])
        plt.xticks(rotation=0)
        
        ax.set_xlabel('')
        ax.set_ylabel('')
        
        plt.legend(fontsize="8", loc="upper right")
        plt.tight_layout()
        
        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor=DARK_GREY, edgecolor=DARK_GREY)
        plt.close(fig)
        buf.seek(0)
        
        image = Image.open(buf)
        return image


    def donut_limit(self, records, _limit, currency) -> Image.Image:
        if records is None or len(records) == 0:
            total_spent = 0.0
            category_totals = {}
            remaining_amount = _limit
            amounts = [remaining_amount]
            categories = ['Remaining']
        else:
            category_totals = {}
            total_spent = 0.0
            for record in records:
                category = record[3]
                amount = record[2]
                total_spent += amount
                category_totals[category] = category_totals.get(category, 0) + amount

            categories = list(category_totals.keys())
            amounts = list(category_totals.values())

            remaining_amount = max(0, _limit - total_spent)
            if remaining_amount > 0:
                amounts.append(remaining_amount)
                categories.append('Remaining')

        colors = [OPTION_DICT.get(cat, GREY) for cat in categories]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(amounts, colors=colors, startangle=90, wedgeprops=dict(width=0.4))

        center_circle = plt.Circle((0, 0), 0.6, fc=DARK_DARK_GREY)
        fig.gca().add_artist(center_circle)

        legend_labels = [
            f"{cat}: {amt:.2f}{currency}" for cat, amt in zip(categories, amounts)
        ]
        legend = plt.legend(legend_labels, loc='upper left', bbox_to_anchor=(-0.35, 1), fontsize=17)
        legend.get_frame().set_facecolor(DARK_DARK_GREY)
        for text in legend.get_texts():
            text.set_color(WHITE)

        fig.patch.set_facecolor(DARK_DARK_GREY)
        ax.set_facecolor(DARK_DARK_GREY)
        ax.axis('off')

        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', facecolor=DARK_DARK_GREY, edgecolor=DARK_DARK_GREY)
        plt.close(fig)
        buf.seek(0)
        image = Image.open(buf)

        return image
