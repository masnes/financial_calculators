'''
interest calculator
'''
import sys, getopt

DEFAULT_INTEREST_RATE = 1.03
DEFAULT_COMPOUND_RATE = 1.07
DEFAULT_STARTING_CONTRIBUTION = 0
DEFAULT_YEARLY_CONTRIBUTION = 10000
DEFAULT_YEARS_OF_CONTRIBUTION = 40
DEFAULT_YEARS_TILL_RETIREMENT = 40
DEFAULT_SHOW_MULTIPLIERS = False
DEFAULT_NUM_MULTIPLIERS = 3

def usage():
    ''' print usage info '''
    print(''' Usage:
          -s starting contribution (defaults to {:,})
          -i (float >= 1.00) interest rate (defaults to {})
          -o (float >= 1.00) compound rate (defaults to {})
          -c yearly contribution (defaults to {:,})
          -n years of contribution (defaults to {})
          -r years till retirement (defaults to {})
          -m [num] show multipliers (how much your investments multiply over
             each of [num] periods of your investment) (off by default)
          '''.format(DEFAULT_STARTING_CONTRIBUTION, DEFAULT_INTEREST_RATE,
                     DEFAULT_COMPOUND_RATE, DEFAULT_YEARLY_CONTRIBUTION,
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
    interest_rate = DEFAULT_INTEREST_RATE
    compound_rate = DEFAULT_COMPOUND_RATE
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
            compound_rate = float(a)
        elif o == "-i":
            interest_rate = float(a)
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

    return (starting_contribution, interest_rate, compound_rate,
            yearly_contribution, years_of_contribution, years_till_retirement,
            show_multipliers, num_multipliers)


def compound(start, compound_rate, years_to_compound):
    for _ in range(years_to_compound):
        start *= compound_rate
    return start

def get_multipliers(num_multipliers, net_interest_rate, years_of_contribution,
                    years_till_retirement):
    period_length = years_of_contribution // (num_multipliers-1)

    multipliers_list = []

    for n in range(0, num_multipliers):
        years_used = n * period_length
        multiplier = compound(1, net_interest_rate,
                              years_till_retirement - years_used)
        muliplier_package = (multiplier, years_used)
        multipliers_list.append(muliplier_package)

    return multipliers_list

def get_retirement_funds(starting_contribution, net_interest_rate,
                         yearly_contribution, years_of_contribution,
                         years_till_retirement):
    compound = starting_contribution
    for i in range(0, years_till_retirement):
        compound *= net_interest_rate
        if i < years_of_contribution:
            compound += yearly_contribution
    return compound

def main():
    (starting_contribution, interest_rate, compound_rate,
     yearly_contribution, years_of_contribution, years_till_retirement,
     show_multipliers, num_multipliers) = process_opts()

    net_interest_rate = compound_rate - interest_rate + 1

    retirement_fund = get_retirement_funds(starting_contribution,
                                           net_interest_rate,
                                           yearly_contribution,
                                           years_of_contribution,
                                           years_till_retirement)
    print("""Assuming
    A starting contribution of ${:,}
    An interest rate of {}
    A compound rate of {}
    A yearly contribution of ${:,}
    {} years of contribution
    and {} years till retirement
          """.format(starting_contribution, interest_rate, compound_rate,
                     yearly_contribution, years_of_contribution,
                     years_till_retirement))

    print("    You'll have a net interest rate of {}\n".format(net_interest_rate))

    if show_multipliers:
        multipliers_list = get_multipliers(num_multipliers, net_interest_rate,
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
