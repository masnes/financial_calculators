'''
Calcate net increase
By: Michael Asnes
'''
import sys

def usage():
    sys.exit("""Usage:
\tpython net_increase.py <Rate of Increase> <Periods>""")

def main():
    try:
        rate = float(sys.argv[1])
        periods = int(sys.argv[2])
    except IndexError:
        usage()
    acc = 1
    for _ in range(periods):
        acc *= rate
    print("Increased {:.3f} times".format(acc))

if __name__ == '__main__':
    main()
