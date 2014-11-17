### Interest Calculator

This program is an interest calculator / retirement calculator

To run it:

```bash
$ python interest.py
```

Optional arguments:
    -h show this help
    -s starting contribution (defaults to 0)
    -i (float >= 1.00) inflation rate (defaults to 1.03)
    -o (float >= 1.00) interest rate (defaults to 1.07)
    -c yearly contribution (defaults to 10,000)
    -n years of contribution (defaults to 40)
    -r years till retirement (defaults to 40)
    -m show how much your investments multiply over each of
       [num] periods of time over your investment (off by default)


#### Examples:

###### Run the calculator with defaults:
```bash
$ python interest.py
```

###### Run the calculator with some options:

* A starting contribution of $50,000
* An inflation rate of 1.03
* An interest rate of 1.07
* A yearly contribution of $10,000
* 15 years of contribution
* and 30 years till retirement

While showing how much your money multiplies by if you invest it 
at (4) different periods in time over your 15 years of contribution.

```bash
$ python interest.py -s 50000 -o 1.07 -c 10000 -n 15 -r 30 -m 4 
```

##### Disclaimers
This program is not well hardened against improper input. 

It has also not been well tested. Use for estimation purposes only.
