# OVERVIEW

This simulation and model is devised as an attempt to discover actual returns an
investor should expect from residential real estate, assuming that future markets will
behave similarly to past markets.

I don't assume that future markets will __perform__ similarly to past markets,
but rather that they will be __behaviorally__ similar to past markets.

# USAGE
        usage: simulate.py [-h] [--years [Y]] [--file [F]] [--count [C]]

        Simulate performance of investment

        optional arguments:
          -h, --help   show this help message and exit
          --years [Y]  number of years to simulate
          --file [F]   filename containing housing data
          --count [C]  number of simulations to run

# DATA
All data provided by the St. Louis Federal Reserve (FRED).

S&P/Case-Shiller Home Price Indices (Percent Change)
https://fred.stlouisfed.org/series/SPCS10RSA/downloaddata

# NOTES:
If you download the `SPCS10RSA.csv` datafile again, make sure to set the first
row value for VALUE to `0.0`, otherwise it will interpret the entire column in the
.csv as `str()`

# AUTHOR
Josh Peck - jmp@joshpeck.org
