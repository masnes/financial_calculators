'''
Calcate net increase
By: Michael Asnes
'''
import math
import sys

def usage():
    sys.exit("""Usage:
\tpython net_increase.py <Rate of Increase> <Periods>""")

def main():
    try:
        if '%' in sys.argv[1]:
            rate = float(sys.argv[1].replace('%', '')) / 100 + 1
        else:
            rate = float(sys.argv[1])
        periods = float(sys.argv[2])
    except IndexError:
        usage()
    print("Increased {:.3f} times".format(math.pow(rate, periods)))

if __name__ == '__main__':
    main()
