'''
Compound Annual Growth Rate (CAGR) Calculator
By: Michael Asnes
'''
import sys
import math

def usage():
    print(
        '''Usage:
\t-h show this help
\t<Beginning Value>, <Ending Value>, <Number of Periods>'''
    )

def process_opts():
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            sys.exit(usage())
    try:
        begginning_value = sys.argv[1]
        ending_value = sys.argv[2]
        num_periods = sys.argv[3]
    except IndexError:
        sys.exit(usage())
    return begginning_value, ending_value, num_periods

class CagrCalc(object):
    def __init__(self, begginning_value, ending_value, num_periods):
        self.begginning_value = float(begginning_value)
        self.ending_value = float(ending_value)
        self.num_periods = float(num_periods)

    def get_parameters(self):
        return self.begginning_value, self.ending_value, self.num_periods

    def cagr(self):
        self._cagr_failsafes()
        return math.pow((self.ending_value / self.begginning_value), (1 / self.num_periods)) - 1

    def _cagr_failsafes(self):
        if self.ending_value == 0 and self.begginning_value == 0:
            sys.exit("Investment went from $0 to $0! "
                     "You made no money, from no money.")
        elif self.begginning_value == 0:
            sys.exit("Your returns were infinite")

def main():
    cagr_calc = CagrCalc(*process_opts())
    cagr = cagr_calc.cagr()
    print(("You've given a beginning value of {1}, an ending value of {2}, "
           "and {3} periods\nYour investment has grown at a "
           "rate of {0:.2%} per period").format(cagr, *cagr_calc.get_parameters()))

if __name__ == '__main__':
    main()
