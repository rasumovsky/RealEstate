################################################################################
#
# The mortgage class contains methods for accessing mortgage payments and debts.
# Public methods:
#  * init(principal_loan_amount, annual_interest_rate, mortgage_term_in_years)
#  * get_annual_payment()
#  * get_monthly_payment()
#  * calculate_debt_at_year(year, additional_annual_payment)
#  * calculate_debt_at_month(month, additional_monthly_payment)
#  * calculate_years_until_paid_off(additional_annual_payment)
#  * calculate_months_until_paid_off(additional_monthly_payment)
#  * print_mortgage(additional_monthly_payment)
#
################################################################################

import matplotlib.pyplot as plt
import scipy as scipy

class mortgage:
    """
    A class for computing mortgage-related parameters.
    """
    def __init__(self, principal_loan_amount, loan_down_payment,
                 annual_interest_rate, mortgage_term_years):
        """
        Initializes the mortgage class.
        Args:
          * principal_loan_amount: the principal amount of the loan.
          * loan_down_payment: the down payment on the loan.
          * annual_interest_rate: the annual interest rate on the loan.
          * mortgage_term_years: the number of years until the loan is paid.
        """
        self.principal_loan_amount_ = principal_loan_amount
        self.loan_down_payment_ = loan_down_payment
        self.annual_interest_rate_ = annual_interest_rate
        self.mortgage_term_years_ = mortgage_term_years

    def get_annual_payment(self):
        """
        Calculates the annual payment amount.
        Returns:
          * the annual payment amount.
        """
        annual_payment = (
            (self.principal_loan_amount_ *
             ((1.0 + self.annual_interest_rate_)**self.mortgage_term_years_) *
             self.annual_interest_rate_) /
            (((1.0 + self.annual_interest_rate_)**self.mortgage_term_years_) -
             1.0))
        return annual_payment
    
    def get_monthly_payment(self):
        return self.get_annual_payment() / 12.0

    def calculate_debt_at_year(self, year, additional_annual_payment = 0.0):
        """
        Calculates the debt total after a number of years.
        Args:
          * year: the number of years that have passed since loan issue.
          * additional_annual_payment: the amount paid each year beyond the
            minimum required by the mortgage.
        Returns:
          * the amount of remaining debt after a specified number of years.
        """
        payment = self.get_annual_payment() + additional_annual_payment
        z = (1.0 + self.annual_interest_rate_)
        debt = ((self.principal_loan_amount_ * (z**year)) -
                payment * ((z**year - 1) / (z - 1)))
        return debt

    def calculate_debt_at_month(self, month, additional_monthly_payment = 0.0):
        """
        Calculates the debt total after a number of months.
        Args:
          * month: the number of months that have passed since loan issue.
          * additional_monthly_payment: the amount paid each month beyond the
            minimum required by the mortgage.
        Returns:
          * the amount of remaining debt after a specified number of months.
        """
        return self.calculate_debt_at_year(month / 12.0,
                                           12.0 * additional_monthly_payment)

    def calculate_years_until_paid_off(self, additional_annual_payment = 0.0):
        """
        Calculates the number of years until the mortgage is paid.
        Args:
          * additional_annual_payment: the amount paid each year beyond the
            minimum required by the mortgage.
        Returns:
          * the number of years until the mortgage is paid.
        """
        for year in range(self.mortgage_term_years_ + 1):
            if self.calculate_debt_at_year(year, additional_annual_payment) < 0:
                return year
        return self.mortgage_term_years_

    def calculate_months_until_paid_off(self, additional_monthly_payment = 0.0):
        """
        Calculates the number of months until the mortgage is paid.
        Args:
          * additional_monthly_payment: the amount paid each month beyond the
            minimum required by the mortgage.
        Returns:
          * the number of months until the mortgage is paid.
        """
        for month in range(12 * int(self.mortgage_term_years_) + 1):
            if self.calculate_debt_at_month(
                month, additional_monthly_payment) < 0:
                return month
        return (self.mortgage_term_years_ * 12.0)

    def print_mortgage(self, additional_monthly_payment = 0.0):
        """
        Prints the mortgage parameters.
        Args:
          * additional_monthly_payment: the amount paid each month beyond the
            minimum required by the mortgage.
        """
        print(str('Mimimum required monthly payment: $%2.2f' %
                  self.get_monthly_payment()))
        print(str('Total monthly payment: $%2.2f' %
                  (self.get_monthly_payment() + additional_monthly_payment)))
        years_until_paid_off = float(self.calculate_months_until_paid_off(
            additional_monthly_payment)) / 12.0
        print(str('Years until paid off: %2.0f' % years_until_paid_off))

class investment_property:
    """
    A class for computing investment property-related parameters.
    """
    def __init__(self, mortgage, balance_sheet, initial_property_value,
                 annual_appreciation_rate):
        """
        Initializes the property class.
        Args:
          * mortgage: the mortgage for the property.
          * balance_sheet: the balance sheet for the property.
          * initial_property_value: the initial value of the property.
          * annual_appreciation_rate: the annual rate of appreciation.
        """
        self.mortgage_ = mortgage
        self.balance_sheet_ = balance_sheet
        self.initial_property_value_ = initial_property_value
        self.annual_appreciation_rate_ = annual_appreciation_rate

    def get_property_value_at_year(self, year):
        """
        Calculates the total value of the property at a specified number of
        years following the purchase, assuming some initial value and annual
        appreciation rate.
        Args:
          * year: the number of years since the initial purchase.
        Returns:
          * property value after years.
        """
        return (self.initial_property_value_ *
                (1.0 + self.annual_appreciation_rate_) ** year)

    def get_property_value_at_month(self, month):
        """
        Calculates the total value of the property at a specified number of
        months following the purchase, assuming some initial value and annual
        appreciation rate.
        Args:
          * month: the number of months since the initial purchase.
        Returns:
          * property value after months.
        """
        return self.get_property_value_at_year(month / 12.0)

    def get_purchase_cap_rate(self):
        """
        Calculate the purchase capitalization rate, equal to the net income
        divided by the property value at time of purchase.
        """
        return (self.balance_sheet_.get_monthly_cash_flow() /
                self.initial_property_value_)
        
    def calculate_equity_at_year(self, year, additional_annual_payment = 0.0):
        """
        Calculates the total equity after a number of years.
        Args:
          * year: the number of years since the initial purchase.
          * additional_annual_payment: the amount paid each year beyond the
            minimum required by the mortgage.
        Returns:
          * the equity in a property after a specified number of years.
        """
        property_value = self.get_property_value_at_year(year)
        remaining_debt = self.mortgage_.calculate_debt_at_year(
            year, additional_annual_payment)
        return property_value - remaining_debt

    def calculate_equity_at_month(self, month,
                                  additional_monthly_payment = 0.0):
        """
        Calculates the total equity after a number of months.
        Args:
          * month: the number of months since the initial purchase.
          * additional_monthly_payment: the amount paid each month beyond the
            minimum required by the mortgage.
        Returns:
          * the equity in a property after a specified number of months.
        """
        property_value = self.get_property_value_at_month(month)
        remaining_debt = self.mortgage_.calculate_debt_at_month(
            month, additional_monthly_payment)
        return property_value - remaining_debt

    def calculate_all(self, additional_monthly_payment):
        """
        Calculates the equity, debt, value, and payment.
        Args:
          * additional_monthly_payment: extra monthly payment beyond minimum.
        Returns:
          * the amount of debt, equity, property value, and payment size.
          * the number of years until the property is paid off.
        """
        results = {
            'months': list(
                range(int(12 * self.mortgage_.mortgage_term_years_))),
            'debts': [], 'equities': [], 'payments': [], 'values': []
        }
        months_until_paid_off = 0
        for month in results['months']:
            debt = self.mortgage_.calculate_debt_at_month(
                month, additional_monthly_payment)
            equity = self.calculate_equity_at_month(
                month, additional_monthly_payment)
            value = self.get_property_value_at_month(month)
            results['debts'].append(debt if debt > 0 else 0.0)
            results['equities'].append(equity if equity < value else value)
            results['values'].append(value)
            results['payments'].append(
                (self.mortgage_.get_monthly_payment() +
                 additional_monthly_payment)
                if debt > 0 else 0.0)
            if debt > 0: months_until_paid_off = month
        return results, (months_until_paid_off / 12.0)

    def plot_equity_and_debt(self, additional_monthly_payment):
        """
        Plots and calculates the equity, debt, value, and payment.
        Args:
          * additional_monthly_payment: extra monthly payment beyond minimum.
        Returns:
          * A plot of the amount of debt, equity, property value, and payment size.
        """
        results, _ = self.calculate_all(additional_monthly_payment)
        fig, ax = plt.subplots(figsize=(10,5))
        years = [month / 12.0 for month in results['months']]
        ax.plot(years, results['debts'], label='Debt', color='r')
        ax.plot(years, results['values'], label='Property value', color='b')
        ax.plot(years, results['equities'], label='Equity', color='g')
        ax.fill_between(
            years, scipy.zeros(len(results['debts'])), results['debts'],
            facecolor='r', alpha=0.3)
        ax.fill_between(years, scipy.zeros(len(results['values'])),
        results['values'], facecolor='b', alpha=0.15)
        ax.fill_between(
            years, scipy.zeros(len(results['equities'])),
            results['equities'], facecolor='g', alpha=0.3)
        ax.legend(loc='upper left')
        ax.set(xlabel='Years', ylabel='Value [$]', title='Equity and debt by month')
        ax.grid()
        plt.show()

    def plot_gains(self, additional_monthly_payment):
        """
        Plots the capital gains.
        Args:
          * additional_monthly_payment: extra monthly payment beyond minimum.
        Returns:
          * A plot of the capital gains.
        """
        results, _ = self.calculate_all(additional_monthly_payment)
        years = [month / 12.0 for month in results['months']]
        gains = results['equities']
        cash_flow = self.balance_sheet_.get_cash_flow()
        one_time_costs = self.balance_sheet_.get_total_one_time_costs()
        for i in range(len(gains)):
            gains[i] += float(i * cash_flow)
            gains[i] -= one_time_costs
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(years, gains, label='Gains', color='g')
        ax.fill_between(
            years, scipy.zeros(len(gains)), gains, facecolor='g',
            alpha=0.3)
        ax.set(xlabel='Years', ylabel='Gains [$]', title='Capital gains')
        ax.grid()
        plt.show()
