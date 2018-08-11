import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

colors = ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']

def plot_pie(names, values):
    # Plot a pie chart of expenses
    fig, ax = plt.subplots(figsize=(5,5))
    explode = [0.0] * len(names)
    ax.pie(values, labels=names, autopct='%1.1f%%', shadow=False, startangle=0,
           colors=colors, explode=explode)
    centre_circle = plt.Circle((0, 0), 0.7, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')
    plt.tight_layout()
    plt.show()

