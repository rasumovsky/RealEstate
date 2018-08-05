################################################################################
#
# The mortgage class contains methods for accessing mortgage payments and debts.
# Public methods:
#  * init(principal_loan_amount, annual_interest_rate, mortgage_term_in_years)
#  * get_annual_payment()
#  * get_monthly_payment()
#  * calculate_debt_at_year(year, additional_annual_payment)
#  * calculate_debt_at_month(month, additional_monthly_payment)
#
# The property class contains methods for assessing property value and equity.
# Public methods:
#  * init(mortgage, initial_property_value, annual_appreciation_rate)
#  * get_property_value_at_year(year)
#  * get_property_value_at_month(month)
#  * calculate_equity_at_year(year, additional_annual_payment)
#  * calculate_equity_at_month(month, additional_monthly_payment)
#  * calculate_all(additional_monthly_payment)
#
################################################################################

class mortgage:
    """
    A class for computing mortgage-related parameters.
    """
    def __init__(self, principal_loan_amount, annual_interest_rate,
                 mortgage_term_years):
        """
        Initializes the mortgage class.
        Args:
          * principal: the principal amount of the loan.
          * interest_rate: the annual interest rate on the loan.
          * term_in_years: the number of years until the loan is paid.
        """
        self.principal_loan_amount_ = principal_loan_amount
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


class investment_property:
    """
    A class for computing investment property-related parameters.
    """
    def __init__(self, mortgage, initial_property_value,
                 annual_appreciation_rate):
        """
        Initializes the property class.
        Args:
          * mortgage: the mortgage for the property.
          * initial_property_value: the initial value of the property.
          * annual_appreciation_rate: the annual rate of appreciation.
        """
        self.mortgage_ = mortgage
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