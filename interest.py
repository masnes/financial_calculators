'''
compounding calculator
By: Michael Asnes
'''
import sys, getopt

DEFAULT_INFLATION_RATE = 1.03
DEFAULT_COMPOUNDING_RATE = 1.07
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
          -i (float >= 1.00) inflation rate (defaults to {})
          -o (float >= 1.00) compounding rate (defaults to {})
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
            compounding_rate = float(a)
        elif o == "-i":
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


def compound(start, compounding_rate, years_to_compound):
    for _ in range(years_to_compound):
        start *= compounding_rate
    return start


def get_multipliers(num_multipliers, net_compounding_rate, years_of_contribution,
                    years_till_retirement):
    period_length = years_of_contribution // (num_multipliers-1)

    multipliers_list = []

    for n in range(0, num_multipliers):
        years_used = n * period_length
        multiplier = compound(1, net_compounding_rate,
                              years_till_retirement - years_used)
        muliplier_package = (multiplier, years_used)
        multipliers_list.append(muliplier_package)

    return multipliers_list


def get_retirement_funds(starting_contribution, net_compounding_rate,
                         yearly_contribution, years_of_contribution,
                         years_till_retirement):
    compound = starting_contribution
    for i in range(0, years_till_retirement):
        compound *= net_compounding_rate
        if i < years_of_contribution:
            compound += yearly_contribution
    return compound


def main():
    (starting_contribution, inflation_rate, compounding_rate,
     yearly_contribution, years_of_contribution, years_till_retirement,
     show_multipliers, num_multipliers) = process_opts()

    net_compounding_rate = compounding_rate - inflation_rate + 1

    retirement_fund = get_retirement_funds(starting_contribution,
                                           net_compounding_rate,
                                           yearly_contribution,
                                           years_of_contribution,
                                           years_till_retirement)
    money_contributed = (yearly_contribution * years_of_contribution) + starting_contribution

    print("""Assuming:
    A starting contribution of ${:,}
    An inflation rate of {}
    An compounding rate of {}
    A yearly contribution of ${:,}
    {} years of contribution
    and {} years till retirement
          """.format(starting_contribution, inflation_rate, compounding_rate,
                     yearly_contribution, years_of_contribution,
                     years_till_retirement))

    print("    You'll have a net compounding rate of {}\n".format(net_compounding_rate))

    if show_multipliers:
        multipliers_list = get_multipliers(num_multipliers, net_compounding_rate,
                                           years_of_contribution,
                                           years_till_retirement)
        print("Your money will multiply by:")
        for multiplier_package in multipliers_list:
            multiple = multiplier_package[0]
            years = multiplier_package[1]
            print("    {:5.2f} times if you invest it".format(multiple),
                  "{:2} years after the start of your retirement savings".format(years))

    print("")
    print("You will retire with the equivalent of",
          "${:,.2f} in today's currency".format(retirement_fund))
    print("")


if __name__ == '__main__':
    main()
