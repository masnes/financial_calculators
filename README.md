### Interest Calculator

This program is an interest calculator / retirement calculator

To run it:

```bash
$ python interest.py
```

Optional arguments:
```
    -h show this help
    -s starting contribution (defaults to 0)
    -i (float >= 1.00) inflation rate (defaults to 1.03)
    -o (float >= 1.00) interest rate (defaults to 1.10)
    -c yearly contribution (defaults to 10,000)
    -n years of contribution (defaults to 40)
    -r years till retirement (defaults to 40)
    -m show how much your investments multiply over each of
       [num] periods of time over your investment (off by default)
```


#### Examples:

##### Run the calculator with defaults:
```bash
$ python interest.py
```

###### Output:
```
Assuming:
    A starting contribution of $0
    An inflation rate of 1.03
    An interest rate of 1.07
    A yearly contribution of $10,000
    40 years of contribution
    and 40 years till retirement

    You'll have a net interest rate of 1.04


You will retire with the equivalent of $950,255.16 in today's currency
```

##### Run the calculator with some options:

* A starting contribution of $50,000
* The default inflation rate of 1.03
* An interest rate of 1.08
* A yearly contribution of $10,000 (same as the default, but specified in the arguments)
* 15 years of contribution
* and 30 years till retirement

While showing how much your money multiplies by if you invest it
at (4) different periods in time over your 15 years of contribution.

```bash
$ python interest.py -s 50000 -o 1.08 -c 10000 -n 15 -r 30 -m 4
```
###### Output:
```
Assuming:
    A starting contribution of $50,000
    An inflation rate of 1.03
    An interest rate of 1.08
    A yearly contribution of $10,000
    15 years of contribution
    and 30 years till retirement

    You'll have a net interest rate of 1.05

Your money will multiply by:
     4.32 times if you invest it  0 years after the start of your retirement savings
     3.39 times if you invest it  5 years after the start of your retirement savings
     2.65 times if you invest it 10 years after the start of your retirement savings
     2.08 times if you invest it 15 years after the start of your retirement savings

You will retire with the equivalent of $664,699.96 in today's currency
```

##### Disclaimers
This program is not well hardened against improper input.

It has also not been well tested. Use for estimation purposes only.
