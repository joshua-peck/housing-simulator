#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas
from random import random
from random import uniform
import argparse
import getopt
import sys
from matplotlib import pyplot
import json

PROMPT = '>> '

parser = \
    argparse.ArgumentParser(description='Simulate performance of investment'
                            )
parser.add_argument(
    '--years',
    metavar='Y',
    type=int,
    nargs='?',
    default=5,
    help='number of years to simulate',
    )
parser.add_argument(
    '--file',
    metavar='F',
    type=str,
    nargs='?',
    default='SPCS10RSA.csv',
    help='filename containing housing data',
    )
parser.add_argument(
    '--count',
    metavar='C',
    type=int,
    nargs='?',
    default=5,
    help='number of simulations to run',
    )
parser.add_argument(
    '--value',
    metavar='V',
    type=int,
    nargs='?',
    default=150000,
    help='initial value of the property',
    )
args = parser.parse_args()

print "Reading historical data from '%s' and calculating metrics" \
    % args.file
histdata = pandas.read_csv(args.file)
histdata['DELTA'] = histdata.VALUE.astype(float) / 100.0

# XXX convert to module or object

histdata_stats = {
    'num_obs': float(len(histdata.index)),
    'num_gain': histdata.DELTA[histdata.DELTA > 0].count(),
    'num_loss': histdata.DELTA[histdata.DELTA < 0].count(),
    'p_gain': None,
    'p_loss': None,
    }

histdata_stats['p_gain'] = histdata_stats['num_gain'] \
    / histdata_stats['num_obs']
histdata_stats['p_loss'] = histdata_stats['num_loss'] \
    / histdata_stats['num_obs']
histdata_stats['mean_gain_size'] = histdata.DELTA[histdata.DELTA
        > 0].sum() / histdata_stats['num_gain']
histdata_stats['mean_loss_size'] = histdata.DELTA[histdata.DELTA
        < 0].sum() / histdata_stats['num_loss']

print 'Running simulations with the following options: '
print json.dumps(histdata_stats, sort_keys=True, indent=4,
                 separators=(',', ': '))
print "Running %d simulations of %d months" % (args.count, args.years * 12)
sim_results = list()
for n in range(args.count): # simulation number n
    month_sim = pandas.DataFrame(columns=('MONTH', 'OUTCOME', 'VALUE'))
    random_walk = list()
    for m in range(args.years * 12): # months to simulate
        sim = pandas.DataFrame()
        outcome = "DOWN"
        value = 0.0
        if (random() < histdata_stats['p_gain']):
            outcome = "UP"
        if ('DOWN' == outcome):
            value = uniform(histdata_stats['mean_loss_size'], 0)
        else:
            value = uniform(0, histdata_stats['mean_gain_size'])
        month_sim.loc[m] = (m, outcome, value)
        if (m > 0):
            random_walk.append(random_walk[m-1] + value)
        else:
            random_walk.append(value)
    # pyplot.plot(random_walk)
    # pyplot.show()
    annualized_return = month_sim.VALUE.sum() / args.years
    sim_results.append(annualized_return)

yields = pandas.Series(sim_results)
print yields
print yields.mean()
print yields.max()
print yields.min()
print yields.median()
print yields.mad()
yields.hist()
pyplot.show()
