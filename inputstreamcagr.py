'''
Compound Annual Growth Rate (CAGR) Calculator with contributions per period
By: Michael Asnes
'''
import sys

def usage():
    print(
        '''Usage:
\t-h show this help
\t<Beginning Value>, <Ending Value>, <Contribution per period>,
\t<Number of Periods>'''
    )

def process_opts():
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            sys.exit(usage())
    try:
        begginning_value = sys.argv[1]
        ending_value = sys.argv[2]
        contribution_per_period = sys.argv[3]
        num_periods = sys.argv[4]
    except IndexError:
        sys.exit(usage())
    return begginning_value, ending_value, contribution_per_period, num_periods

class InputStreamCagr(object):
    """ Cagr is easy. But what if you've been investing a constant stream
    of money over x periods?

    To derive this, you need to solve the following equation for r:
        r = compounding rate (ex: 1.07 for a 7% / period return)
        s = starting value
        e = ending value
        c = yearly contribution value
        n = number of periods
        e = sum_{i=0}^{n-1}(c * r^i) + (s * r^n)

        Explained:
            The starting value compounds n times, giving us (s * r^n)
            The first periodic contribution will compound n-1 times (all times
            except the first period), the second will compound n-2 times,
            ... until the last one which doesn't compound.

    This is beyond my current mathematical knowledge. However,
    I can use a variant on binary search to approximate r.
    """

    def __init__(self, begginning_value, ending_value,
                 contribution_per_period, num_periods):
        self.begginning_value = float(begginning_value)
        self.ending_value = float(ending_value)
        self.contribution_per_period = float(contribution_per_period)
        self.num_periods = int(num_periods)

    def money_contributed(self):
        yearly_contribution_net = self.contribution_per_period * (self.num_periods - 1)
        return yearly_contribution_net + self.begginning_value

    def approximate_growth_rate(self, allowable_error):
        min_rate, max_rate = self._get_bounds_on_growth_rate(allowable_error)
        assert isinstance(min_rate, float) and isinstance(max_rate, float)

        mid_rate = (max_rate - min_rate) / 2 + min_rate
        return_at_mid_rate = self._calculate_return_at_rate(mid_rate)
        while abs(return_at_mid_rate - self.ending_value) > allowable_error:
            if return_at_mid_rate > self.ending_value:
                max_rate = mid_rate
            else:
                min_rate = mid_rate
            mid_rate = (max_rate - min_rate) / 2 + min_rate
            return_at_mid_rate = self._calculate_return_at_rate(mid_rate)
        approximate_growth_rate = mid_rate
        return approximate_growth_rate


    def _get_bounds_on_growth_rate(self, allowable_error):
        """ Returns: (min_rate, max_rate) """
        min_rate = None
        max_rate = None

        if self.ending_value < self.money_contributed():
            print("Warning, money shrank. The program cannot handle this")
            return None, 1.00

        guess_rate = 1.05
        return_at_rate = self._calculate_return_at_rate(guess_rate)
        if abs(return_at_rate - self.ending_value) <= allowable_error:
            min_rate = max_rate = guess_rate
            return min_rate, max_rate
        elif return_at_rate > self.ending_value:
            max_rate = guess_rate
            min_rate = 1.00
            return min_rate, max_rate
        else:   # return_at_rate < self.ending_value
            while return_at_rate <= self.ending_value:
                min_rate = guess_rate
                guess_rate = double_rate(guess_rate)
                return_at_rate = self._calculate_return_at_rate(guess_rate)
            max_rate = guess_rate
            return min_rate, max_rate

    def _calculate_return_at_rate(self, rate):
        compounded_beg_val = self.begginning_value * (rate ** self.num_periods)

        contribution_accumulator = self.contribution_per_period
        for _ in range(self.num_periods - 1):
            contribution_accumulator *= rate
            contribution_accumulator += self.contribution_per_period
        return contribution_accumulator + compounded_beg_val


def double_rate(rate):
    return ((rate - 1.0) * 2) + 1

def float_to_percent(double):
    return (double - 1.00) * 100

def main():
    inflation_rate = 1.03
    inflation_rate_percent = float_to_percent(inflation_rate)
    isc = InputStreamCagr(*process_opts())
    acceptable_error = abs(isc.ending_value / 1000)
    approximate_growth_rate = isc.approximate_growth_rate(acceptable_error)
    approximate_growth_rate_percent = float_to_percent(approximate_growth_rate)
    print("Money grew at an approximate growth rate of: {:.2f}%"\
          .format(approximate_growth_rate_percent))
    print("Assuming an inflation rate of {:.2f}%, this would cut real growth down "
          "to {:.2f}%, or require a real growth rate of {:.2f}% to maintain "
          "this value after inflation".format(inflation_rate_percent,
                                              approximate_growth_rate_percent -
                                              inflation_rate_percent,
                                              approximate_growth_rate_percent +
                                              inflation_rate_percent))

if __name__ == "__main__":
    main()
