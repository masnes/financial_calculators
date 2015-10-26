#!/usr/bin/env python3
'''
Retirement calculator
By: Michael Asnes
'''
import getopt
import sys

DEFAULT_INFLATION_RATE = 1.03
DEFAULT_COMPOUNDING_RATE = 1.095
DEFAULT_RETIRENMENT_COMPOUNDING_RATE = 1.08
DEFAULT_STARTING_CONTRIBUTION = 0
DEFAULT_YEARLY_CONTRIBUTION = 10000
DEFAULT_YEARS_OF_CONTRIBUTION = 40
DEFAULT_YEARS_TILL_RETIREMENT = 40
DEFAULT_YEARS_OF_RETIREMENT = 30
DEFAULT_SHOW_MULTIPLIERS = False
DEFAULT_NUM_MULTIPLIERS = 3
DEFAULT_WITHDRAW_RATE = 0.04
SAFE_WITHDRAW_RATE = 0.04


def usage():
    ''' print usage info '''
    print(''' Usage:
          -h show this help
          -s starting contribution (defaults to {:,})
          -i inflation rate (defaults to {}) (float >= 1.00 or 'x%')
          -o compounding rate (defaults to {}) (float >= 1.00 or 'x%')
          -c yearly contribution (defaults to {:,})
          -n years of contribution (defaults to {})
          -t years till retirement (defaults to {})
          -r years of retirement (defaults to {})
          -m show how much your investments multiply over each of
             [num] periods of time over your investment (off by default)
          '''.format(DEFAULT_STARTING_CONTRIBUTION, DEFAULT_INFLATION_RATE,
                     DEFAULT_COMPOUNDING_RATE, DEFAULT_YEARLY_CONTRIBUTION,
                     DEFAULT_YEARS_OF_CONTRIBUTION,
                     DEFAULT_YEARS_TILL_RETIREMENT,
                     DEFAULT_YEARS_OF_RETIREMENT))


def process_opts():
    def treat_potential_percent(arg, set_to_one=True):
        if '%' in arg:
            arg = arg.replace('%', '')
            if set_to_one:
                return float(arg) / 100 + 1
            else:
                return float(arg) / 100
        else:
            return float(arg)

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "s:i:c:w:n:t:r:m:ho:v", ["help"])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    inflation_rate = DEFAULT_INFLATION_RATE
    compounding_rate = DEFAULT_COMPOUNDING_RATE
    starting_contribution = DEFAULT_STARTING_CONTRIBUTION
    yearly_contribution = DEFAULT_YEARLY_CONTRIBUTION
    years_of_contribution = DEFAULT_YEARS_OF_CONTRIBUTION
    years_till_retirement = DEFAULT_YEARS_TILL_RETIREMENT
    years_of_retirement = DEFAULT_YEARS_OF_RETIREMENT
    show_multipliers = DEFAULT_SHOW_MULTIPLIERS
    num_multipliers = 0
    withdraw_rate = DEFAULT_WITHDRAW_RATE
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-s":
            starting_contribution = int(a)
        elif o == "-o":
            compounding_rate = treat_potential_percent(a)
        elif o == "-i":
            inflation_rate = treat_potential_percent(a)
        elif o == "-c":
            yearly_contribution = int(a)
        elif o == "-n":
            years_of_contribution = int(a)
        elif o == "-r":
            years_of_retirement = int(a)
        elif o == "-t":
            years_till_retirement = int(a)
        elif o == "-m":
            show_multipliers = True
            num_multipliers = int(a)
        else:
            assert False, "unhandled option"

    return (starting_contribution, inflation_rate, compounding_rate,
            yearly_contribution, years_of_contribution, years_till_retirement,
            years_of_retirement, show_multipliers, num_multipliers,
            withdraw_rate)

class DataHolder(object):
    def __init__(self):
        (self.starting_contribution,
         self.inflation_rate,
         self.compounding_rate,
         self.yearly_contribution,
         self.years_of_contribution,
         self.years_till_retirement,
         self.years_of_retirement,
         self.show_multipliers,
         self.num_multipliers,
         self.withdraw_rate) = process_opts()

        self.net_compounding_rate = self.compounding_rate - self.inflation_rate + 1

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[attr] = value


class CompoundingCalculator(object):
    def __init__(self, dataHolder):
        self.dataHolder = dataHolder
        self.retirement_funds = None
        self.multipliers_list = []

    def get_retirement_funds(self):
        if self.retirement_funds is None:
            compound = self.dataHolder.starting_contribution
            for i in range(0, self.dataHolder.years_till_retirement):
                compound *= self.dataHolder.net_compounding_rate
                if i < self.dataHolder.years_of_contribution:
                    compound += self.dataHolder.yearly_contribution

            self.retirement_funds = compound

        return self.retirement_funds

    def get_multipliers(self, num_multipliers):
        period_length = self.dataHolder.years_of_contribution // (num_multipliers-1)
        if len(self.multipliers_list) == 0:
            for n in range(0, num_multipliers):
                years_used = n * period_length
                multiplier = compound(1, self.dataHolder.net_compounding_rate, self.dataHolder.years_till_retirement - years_used)
                muliplier_package = (multiplier, years_used)
                self.multipliers_list.append(muliplier_package)
        return self.multipliers_list

    def money_contributed(self):
        return (self.dataHolder.yearly_contribution * self.dataHolder.years_of_contribution) + self.dataHolder.starting_contribution

class CalcPrinter(object):
    def __init__(self, compoundingCalculator, dataHolder):
        self.compounding_calc = compoundingCalculator
        self.dataHolder = dataHolder

    def print_starting_info(self):
        cc = self.compounding_calc
        print("""Assuming:
        A starting contribution of ${:,}
        An inflation rate of {} ({})
        A compounding rate of {} ({})
        A yearly contribution of ${:,}
        {} years of contribution
        {} years till retirement
        and {} years of retirement
            """.format(self.dataHolder.starting_contribution,
                       self.dataHolder.inflation_rate, self.to_percent_str(self.dataHolder.inflation_rate),
                       self.dataHolder.compounding_rate, self.to_percent_str(self.dataHolder.compounding_rate),
                       self.dataHolder.yearly_contribution,
                       self.dataHolder.years_of_contribution,
                       self.dataHolder.years_till_retirement,
                       self.dataHolder.years_of_retirement))
        print("    You'll have a net compounding rate of {} ({})\n".format(
            self.dataHolder.net_compounding_rate,
            self.to_percent_str(self.dataHolder.net_compounding_rate)
        ))

    def print_money_contributed(self):
        print("")
        print("You will put in a total of ${:,.2f}".format(self.compounding_calc.money_contributed()))

    def print_retirement_amount(self):
        print("You will retire with the equivalent of",
              "${:,.2f} in today's currency".format(self.compounding_calc.get_retirement_funds()))
        print("")

        self.print_withdraw_rate()

    def _get_safe_withdraw_rate(self):
        # See http://www.retireearlyhomepage.com/restud1.html
        # (Or Google the numbers: 8.47% 4.78% 3.81% 3.54% 3.35% 3.24%)
        years_to_safe_withdraw_rates = {
            10: .0847,
            20: .0478,
            30: .0381,
            40: .0354,
            50: .0335,
            60: .0324,
        }

        withdrawal_rate_keys = sorted(years_to_safe_withdraw_rates.keys())

        years_of_retirement = self.dataHolder.years_of_retirement
        # Best to round up eagerly. Rounding down can give an unsafe impression.
        approximate_years_of_retirement = (round(years_of_retirement)
                                           if years_of_retirement <= 3
                                           else round_up_to_nearest_ten(years_of_retirement))

        if approximate_years_of_retirement < withdrawal_rate_keys[0]:
            approximate_years_of_retirement = withdrawal_rate_keys[0]
        elif approximate_years_of_retirement > withdrawal_rate_keys[-1]:
            approximate_years_of_retirement = withdrawal_rate_keys[-1]
        return years_to_safe_withdraw_rates[approximate_years_of_retirement]


    def print_withdraw_rate(self):
        safe_withdraw_rate = self._get_safe_withdraw_rate()
        withdraw_per_year = self.compounding_calc.get_retirement_funds() * safe_withdraw_rate
        print("If you expect to be retired for {} years, then the approximate rate which you\n"
              "can safely withdraw funds each year is {:1.3%}. At this rate, you can withdraw \n"
              "\n"
              "\t${:,.2f} per year (today's currency)\n"
              "\n"
              "Historically, this rate has been >99% safe for the given duration. \n"
              #TODO
              #"To get the 100%% safe rate, use the "--safe" option\n"
              "\n"
              "There is a significant, but non guaranteed, chance of ending up with \n"
              "significantly more money at the end of the period. In the worst historical case,\n"
              "funds are completely depleted at the end of the period.\n"
              "\n"
              "These calculations do not factor in taxes, pensions, or social security."
              "".format(self.dataHolder.years_of_retirement,
                        safe_withdraw_rate, withdraw_per_year))



    def print_multipliers(self):
        multipliers_list = self.compounding_calc.get_multipliers(self.dataHolder.num_multipliers)
        print("Your money will multiply by:")
        for multiplier_package in multipliers_list:
            multiple = multiplier_package[0]
            years = multiplier_package[1]
            print("    {:5.2f} times if you invest it".format(multiple),
                  "{:2} years after the start of your retirement savings".format(years))

    def to_percent_str(self, num, set_to_one=True):
        if num <= 0.00:
            return "-infinity%"
        if set_to_one:
            percent_val = (num - 1.00) * 100
        else:
            percent_val = num * 100
        return '{:.2f}%'.format(percent_val)

def round_up_to_nearest_ten(num):
    if num % 10 == 0:
        return num
    return (int(num / 10) + 1) * 10

def compound(start, compounding_rate, years_to_compound):
    for _ in range(years_to_compound):
        start *= compounding_rate
    return start

# source:
# http://stackoverflow.com/questions/4028889/floating-point-equality-in-python
def approx_equal(a, b, tol=0.000010):
        return abs(a-b) <= max(abs(a), abs(b)) * tol

def main():
    dataHolder = DataHolder()
    calc = CompoundingCalculator(dataHolder)
    printer = CalcPrinter(calc, dataHolder)

    printer.print_starting_info()
    printer.print_money_contributed()
    printer.print_retirement_amount()

    if dataHolder.show_multipliers:
        printer.print_multipliers()


if __name__ == '__main__':
    main()
