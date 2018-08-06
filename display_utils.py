import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy

colors = ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']

def plot_values(results, plot_title):
    """
    Plots and calculates the equity, debt, value, and payment.
    Args:
      * results: a dictionary with lists of debt, equity, value, and payment.
      * plot_title: the title of the plot.
    Returns:
      * A plot of the amount of debt, equity, property value, and payment size.
    """
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(results['months'], results['debts'], label='Debt', color='r')
    ax.plot(results['months'], results['values'], label='Property value',
            color='b')
    ax.plot(results['months'], results['equities'], label='Equity', color='g')
    ax.fill_between(
        results['months'], scipy.zeros(len(results['debts'])), results['debts'],
        facecolor='r', alpha=0.3)
    ax.fill_between(
        results['months'], scipy.zeros(len(results['values'])),
        results['values'], facecolor='b', alpha=0.15)
    ax.fill_between(
        results['months'], scipy.zeros(len(results['equities'])),
        results['equities'], facecolor='g', alpha=0.3)
    ax.legend(loc='upper left')
    ax.set(xlabel='Months', ylabel='Value [$]', title=plot_title)
    ax.grid()
    plt.show()

def print_mortgage_text(monthly_payment, additional_monthly_payment,
                        years_until_paid_off):
    print(str('Mimimum required monthly payment: $%2.2f' %
              monthly_payment))
    print(str('Total monthly payment: $%2.2f' %
              (monthly_payment + additional_monthly_payment)))
    print(str('Years until paid off: %2.0f' % years_until_paid_off))

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

