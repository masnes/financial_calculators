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
        beginning_value = sys.argv[1]
        ending_value = sys.argv[2]
        num_periods = sys.argv[3]
    except IndexError:
        sys.exit(usage())
    return beginning_value, ending_value, num_periods

class CagrCalc(object):
    def __init__(self, beginning_value, ending_value, num_periods):
        self.beginning_value = float(beginning_value)
        self.ending_value = float(ending_value)
        self.num_periods = float(num_periods)

    def get_parameters(self):
        return self.beginning_value, self.ending_value, self.num_periods

    def cagr(self):
        self._cagr_failsafes()
        return math.pow((self.ending_value / self.beginning_value), (1 / self.num_periods)) - 1

    def _cagr_failsafes(self):
        if self.ending_value == 0 and self.beginning_value == 0:
            sys.exit("Investment went from $0 to $0! "
                     "You made no money, from no money.")
        elif self.beginning_value == 0:
            sys.exit("Your returns were infinite")
        elif self.num_periods == 0:
            sys.exit("Growth doesn't make sense over 0 periods")

def main():
    cagr_calc = CagrCalc(*process_opts())
    cagr = cagr_calc.cagr()
    print(("You've given a beginning value of {1}, an ending value of {2}, "
           "and {3} periods\nYour investment has grown at a "
           "rate of {0:.2%} per period").format(cagr, *cagr_calc.get_parameters()))

if __name__ == '__main__':
    main()
