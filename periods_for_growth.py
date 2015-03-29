'''
Calculate number of periods required to grow a certain amount at a certain rate
By: Michael Asnes
'''
import sys
import math

def usage():
    print(
        '''Usage:
\t-h show this help
\t<Beginning Value>, <Ending Value>, <Rate of Change>'''
    )

def process_opts():
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            sys.exit(usage())
    try:
        beginning_value = sys.argv[1]
        ending_value = sys.argv[2]
        if '%' in sys.argv[3]:
            rate_of_change = float(sys.argv[3].replace('%', '')) / 100 + 1
        else:
            rate_of_change = sys.argv[3]
    except IndexError:
        sys.exit(usage())
    return beginning_value, ending_value, rate_of_change

class PeriodsForGrowthCalc(object):
    def __init__(self, beginning_value, ending_value, rate_of_change):
        self.beginning_value = float(beginning_value)
        self.ending_value = float(ending_value)
        self.rate_of_change = float(rate_of_change)

    def get_parameters(self):
        return self.beginning_value, self.ending_value, self.rate_of_change

    # rate of change = (ending value / beginning value) ^ (1 / periods)
    # 1 / periods = log(rate of change) / log(ending_value / beginning_value)
    # 1 = log(rate of change) / log(ending value / beginning value) * periods
    # log(ending value / beginning value) / log(rate of change) = periods
    # periods = log(ending value / beginning value) / log(rate of change)
    def periods(self):
        self._failsafes()
        print("beginning: {}, ending: {}, rate of change: {}".format(self.beginning_value, self.ending_value, self.rate_of_change))
        return math.log(self.ending_value / self.beginning_value) / math.log(self.rate_of_change)

    def _failsafes(self):
        if self.rate_of_change == 0 and self.beginning_value != self.ending_value:
            sys.exit("Infinite periods are required with a zero rate of change")

# source:
# http://stackoverflow.com/questions/4028889/floating-point-equality-in-python
def approx_equal(a, b, tol=0.000001):
        return abs(a-b) <= max(abs(a), abs(b)) * tol


def main():
    periods_for_growth_calc = PeriodsForGrowthCalc(*process_opts())
    periods = periods_for_growth_calc.periods()
    print(("You've given a beginning value of {1}, an ending value of {2}, "
           "and a rate of change of {3}.\nIt took {0:.2f} periods to grow "
           "your investment this much").format(periods, *periods_for_growth_calc.get_parameters()))

if __name__ == '__main__':
    main()
