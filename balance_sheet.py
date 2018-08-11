import display_utils as du
import numpy as np

class balance_sheet:
    
    # TODO(harda) add balance sheet to investment_property class.

    def __init__(self, mortgage):
        """
        """
        self.one_time_costs_ = {}
        self.monthly_income_ = {}
        self.annual_expenses_ = {}
        self.monthly_expenses_ = {}
        self.expenses_proportional_to_rent_ = {}
        # The format is ('name', period in years, dollar amount)
        self.capital_expenditures_ = {}

        # Set the mortgage.
        self.mortgage_ = mortgage
        self.monthly_expenses_['Mortgage'] = self.mortgage_.get_monthly_payment()
        self.one_time_costs_['Down payment'] = self.mortgage_.loan_down_payment_

    def add_one_time_costs(self, one_time_costs):
        self.one_time_costs_.update(one_time_costs)

    def add_monthly_income(self, monthly_income):
        self.monthly_income_.update(monthly_income)

    def add_annual_expenses(self, annual_expenses):
        self.annual_expenses_.update(annual_expenses)

    def add_monthly_expenses(self, monthly_expenses):
        self.monthly_expenses_.update(monthly_expenses)
        
    def add_expenses_proportional_to_rent(self, proportional_expenses):
        self.expenses_proportional_to_rent_.update(proportional_expenses)

    def add_capital_expenditures(self, capital_expenditures):
        self.capital_expenditures_.update(capital_expenditures)

    def get_cash_flow(self):
        income_names, income_values = self.calculate_total_income()
        expense_names, expense_values = self.calculate_total_expenses()
        return np.sum(income_values) - np.sum(expense_values)

    def get_total_one_time_costs(self):
        return np.sum([self.one_time_costs_[c] for c in self.one_time_costs_])

    def set_mortgage(self, mortgage):
        """
        Sets the mortgage for the balance sheet, including monthly expenses and
        one time costs.
        Args:
          * mortgage: the mortgage for the balance sheet.
        """
        self.mortgage_ = mortgage
        self.monthly_expenses['Mortgage'] = self.mortgage_.get_monthly_payment()
        self.one_time_costs_['Down payment'] = self.mortgage_.loan_down_payment_

    def _sort(self, names, values):
        """
        Sorts two lists of names and values by value.
        Args:
          * names: the names of items
          * values: the values of the items
        Returns:
          * sorted names.
          * sorted values.
        """
        vals = [list(x) for x in
                zip(*sorted(zip(values, names), key=lambda pair: pair[0]))]
        return vals[1], vals[0]

    def calculate_monthly_capital_expenditures(self):
        """
        Calculates the monthly capital expenditures, sorted by amount.
        Returns:
          * total_cap_ex_names: the name of each capital expenditure.
          * total_cap_ex_values: the $ amount of each capital expenditure.
        """
        total_cap_ex_names = []
        total_cap_ex_values = []
        for name in self.capital_expenditures_:
            period_years = self.capital_expenditures_[name][0]
            amount = self.capital_expenditures_[name][1] 
            if amount == 0: continue
            total_cap_ex_names.append(name)
            total_cap_ex_values.append(amount / (12.0 * float(period_years)))
        # Return the sorted cap ex names and values.
        return self._sort(total_cap_ex_names, total_cap_ex_values)

    def calculate_total_income(self):
        """
        Creates a sorted list of monthly income sources.
        Returns:
          * names of monthly income streams.
          * values of monthly income streams.
        """
        total_income_names = []
        total_income_values = []        
        for i in self.monthly_income_:
            if self.monthly_income_[i] == 0: continue
            total_income_names.append(i)
            total_income_values.append(self.monthly_income_[i])
        return self._sort(total_income_names, total_income_values)

    def calculate_total_expenses(self):
        """
        Creates a sorted list of monthly expenses.
        Returns:
          * names of monthly expenses.
          * values of monthly expenses.
        """
        total_expense_names = []
        total_expense_values = []
        for e in self.annual_expenses_:
            if self.annual_expenses_[e] == 0: continue
            total_expense_names.append(e)
            total_expense_values.append(self.annual_expenses_[e] / 12.0)
        for e in self.monthly_expenses_:
            if self.monthly_expenses_[e] == 0: continue
            total_expense_names.append(e)
            total_expense_values.append(self.monthly_expenses_[e])
        income_names, income_values = self.calculate_total_income()
        total_income = np.sum(income_values)
        for e in self.expenses_proportional_to_rent_:
            if self.expenses_proportional_to_rent_[e] == 0: continue
            total_expense_names.append(e)
            total_expense_values.append(
                self.expenses_proportional_to_rent_[e] * total_income)
        
        _, total_cap_ex_values = self.calculate_monthly_capital_expenditures()
        summed_cap_ex = np.sum(total_cap_ex_values)
        if summed_cap_ex > 0:
            total_expense_names.append('Capital expenditures')
            total_expense_values.append(summed_cap_ex)
        return self._sort(total_expense_names, total_expense_values)

    def plot_expenses(self):
        """
        Plots a pie chart of expenses.
        """
        names, values = self.calculate_total_expenses()
        print('\nMonthly expenses: $%2.2f' % np.sum(values))
        du.plot_pie(names, values)

    def plot_capital_expenditures(self):
        """
        Plots a pie chart of capital expenditures.
        """
        names, values = self.calculate_monthly_capital_expenditures()
        print('\nCapital expenditures: $%2.2f' % np.sum(values))
        du.plot_pie(names, values)

    def print_statement(self):
        """
        Print income, expenses, cash flow, RoI.
        """
        print('\n----- Income -----')
        income_names, income_values = self.calculate_total_income()
        for i in range(len(income_names)):
            print('\t', income_names[i], str('\t$%2.2f' % income_values[i]))
        print('\tTotal: \t $%2.2f' % np.sum(income_values))

        print('\n----- Expenses -----')
        expense_names, expense_values = self.calculate_total_expenses()
        for i in range(len(expense_names)):
            print('\t', expense_names[i], str('\t$%2.2f' % expense_values[i]))
        print('\tTotal: \t $%2.2f' % np.sum(expense_values))

        print('\n----- Capital expenditures -----')
        cap_ex_names, cap_ex_values = (
            self.calculate_monthly_capital_expenditures())
        for i in range(len(cap_ex_names)):
            print('\t', cap_ex_names[i], str('\t$%2.2f' % cap_ex_values[i]))
        print('\tTotal: \t $%2.2f' % np.sum(cap_ex_values))

        # 3. Cash Flow
        print('\n----- Cash Flow -----')
        monthly_cash_flow = np.sum(income_values) - np.sum(expense_values)
        annual_cash_flow = (12.0 * monthly_cash_flow)
        print('\tMonthly total cashflow = $%2.2f' % monthly_cash_flow)
        print('\tAnnual total cashflow = $%2.2f' % annual_cash_flow)

        # 4. Cash on Cash RoI
        print('\n----- Return on Investment -----')
        total_investment = np.sum(
            [self.one_time_costs_[e] for e in self.one_time_costs_])
        print('\tTotal investment = $%2.2f' % total_investment)
        annual_roi = annual_cash_flow / total_investment
        print('\tAnnual RoI = %2.2f%%' % (100.0 * annual_roi))
