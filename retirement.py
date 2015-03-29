'''
Retirement calculator
By: Michael Asnes
'''
import getopt, sys

DEFAULT_INFLATION_RATE = 1.03
DEFAULT_COMPOUNDING_RATE = 1.10
DEFAULT_STARTING_CONTRIBUTION = 0
DEFAULT_YEARLY_CONTRIBUTION = 10000
DEFAULT_YEARS_OF_CONTRIBUTION = 40
DEFAULT_YEARS_TILL_RETIREMENT = 40
DEFAULT_SHOW_MULTIPLIERS = False
DEFAULT_NUM_MULTIPLIERS = 3


def usage():
    ''' print usage info '''
    print(''' Usage:
          -h show this help
          -s starting contribution (defaults to {:,})
          -i inflation rate (defaults to {}) (float >= 1.00 or 'x%')
          -o compounding rate (defaults to {}) (float >= 1.00 or 'x%')
          -c yearly contribution (defaults to {:,})
          -n years of contribution (defaults to {})
          -r years till retirement (defaults to {})
          -m show how much your investments multiply over each of
             [num] periods of time over your investment (off by default)
          '''.format(DEFAULT_STARTING_CONTRIBUTION, DEFAULT_INFLATION_RATE,
                     DEFAULT_COMPOUNDING_RATE, DEFAULT_YEARLY_CONTRIBUTION,
                     DEFAULT_YEARS_OF_CONTRIBUTION,
                     DEFAULT_YEARS_TILL_RETIREMENT))


def process_opts():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "s:i:c:n:r:m:ho:v", ["help"])
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
    show_multipliers = DEFAULT_SHOW_MULTIPLIERS
    num_multipliers = 0
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o == "-s":
            starting_contribution = int(a)
        elif o == "-o":
            if '%' in a:
                a = a.replace('%', '')
                compounding_rate = float(a) / 100 + 1
            else:
                compounding_rate = float(a)
        elif o == "-i":
            if '%' in a:
                a = a.replace('%', '')
                inflation_rate = float(a) / 100 + 1
            else:
                inflation_rate = float(a)
        elif o == "-c":
            yearly_contribution = int(a)
        elif o == "-n":
            years_of_contribution = int(a)
        elif o == "-r":
            years_till_retirement = int(a)
        elif o == "-m":
            show_multipliers = True
            num_multipliers = int(a)
        else:
            assert False, "unhandled option"

    return (starting_contribution, inflation_rate, compounding_rate,
            yearly_contribution, years_of_contribution, years_till_retirement,
            show_multipliers, num_multipliers)


class CompoundingCalculator(object):
    def __init__(self):
        (
            self.starting_contribution,
            self.inflation_rate,
            self.compounding_rate,
            self.yearly_contribution,
            self.years_of_contribution,
            self.years_till_retirement,
            self.show_multipliers,
            self.num_multipliers
        ) = process_opts()
        self.net_compounding_rate = self.compounding_rate - self.inflation_rate + 1

    def get_retirement_funds(self):
        compound = self.starting_contribution
        for i in range(0, self.years_till_retirement):
            compound *= self.net_compounding_rate
            if i < self.years_of_contribution:
                compound += self.yearly_contribution
        return compound

    def get_multipliers(self):
        period_length = self.years_of_contribution // (self.num_multipliers-1)
        multipliers_list = []
        for n in range(0, self.num_multipliers):
            years_used = n * period_length
            multiplier = compound(1, self.net_compounding_rate, self.years_till_retirement - years_used)
            muliplier_package = (multiplier, years_used)
            multipliers_list.append(muliplier_package)
        return multipliers_list

    def money_contributed(self):
        return (self.yearly_contribution * self.years_of_contribution) + self.starting_contribution

    def print_starting_info(self):
        print("""Assuming:
        A starting contribution of ${:,}
        An inflation rate of {} ({})
        A compounding rate of {} ({})
        A yearly contribution of ${:,}
        {} years of contribution
        and {} years till retirement
            """.format(self.starting_contribution,
                       self.inflation_rate, to_percent_str(self.inflation_rate),
                       self.compounding_rate, to_percent_str(self.compounding_rate),
                       self.yearly_contribution,
                       self.years_of_contribution,
                       self.years_till_retirement))
        print("    You'll have a net compounding rate of {} ({})\n".format(
            self.net_compounding_rate,
            to_percent_str(self.net_compounding_rate)
        ))

    def print_money_contributed(self):
        print("")
        print("You will put in a total of ${:,.2f}".format(self.money_contributed()))

    def print_retirement_amount(self):
        print("You will retire with the equivalent of",
              "${:,.2f} in today's currency".format(self.get_retirement_funds()))
        print("")

    def print_multipliers(self):
        multipliers_list = self.get_multipliers()
        print("Your money will multiply by:")
        for multiplier_package in multipliers_list:
            multiple = multiplier_package[0]
            years = multiplier_package[1]
            print("    {:5.2f} times if you invest it".format(multiple),
                  "{:2} years after the start of your retirement savings".format(years))

def to_percent_str(num):
    percent_val = (num - 1.00) * 100
    return '{:.2f}%'.format(percent_val)

def compound(start, compounding_rate, years_to_compound):
    for _ in range(years_to_compound):
        start *= compounding_rate
    return start

def main():
    cc = CompoundingCalculator()
    cc.print_starting_info()
    cc.print_money_contributed()
    cc.print_retirement_amount()

    if cc.show_multipliers:
        cc.print_multipliers()


if __name__ == '__main__':
    main()
