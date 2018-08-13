import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
from prettytable import PrettyTable

#colors = ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']
colors = ['#FFFF00', '#FF9933', '#FF3366', '#990099', '#9966CC', '#99CCFF', '#66FFCC', '#0099FF', '#0033CC']

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

def create_table(names, values, title):
    x = PrettyTable()
    x.field_names = ['Item', 'Amount']
    for i in range(len(names)):
        x.add_row([names[i], str('$%2.2f' % values[i])])
    x.add_row(['', ''])
    x.add_row(['Total', str('$%2.2f' % np.sum(values))])
    x.align["Item"] = "l"
    x.align["Amount"] = "r"
    print(x.get_string(title=title), '\n')
