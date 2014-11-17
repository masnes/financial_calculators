### Interest Calculator

This program is an interest calculator / retirement calculator

To run it:

```bash
$ python interest.py
```

Optional arguments:
    -h show this help
    -s starting contribution (defaults to 0)
    -i (float >= 1.00) interest rate (defaults to 1.03)
    -o (float >= 1.00) compound rate (defaults to 1.07)
    -c yearly contribution (defaults to 10,000)
    -n years of contribution (defaults to 40)
    -r years till retirement (defaults to 40)
    -m show how much your investments multiply over each of
       [num] periods of time over your investment (off by default)


#### Examples:

Run the calculator with defaults:
```bash
python interest.py
```

Run the calculator with:
    A starting contribution of 50000
    The default interest rate
    A compound rate of 1.07
    A yearly contribution of 10000
    Contributing for 10 years
    Retiring in 30 years
    Asking for 4 multipliers over your investment period

```bash
python interest.py -s 50000 -o 1.07 -c 10000 -n 15 -r 30 -m 4 
```
