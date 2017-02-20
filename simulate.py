#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas
import argparse
import json
from random import random
from random import uniform
from matplotlib import pyplot
from math import sqrt

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
args = parser.parse_args()


def get_historical_params(df):
    stats = {
        'num_obs': float(df.DELTA.count()),
        'num_gain': df.DELTA[df.DELTA > 0].count(),
        'num_loss': df.DELTA[df.DELTA < 0].count(),
        'p_gain': None,
        'p_loss': None,
        }
    stats['p_gain'] = stats['num_gain'] / stats['num_obs']
    stats['p_loss'] = stats['num_loss'] / stats['num_obs']
    stats['mean_gain_size'] = df.DELTA[df.DELTA > 0].sum() \
        / stats['num_gain']
    stats['mean_loss_size'] = df.DELTA[df.DELTA < 0].sum() \
        / stats['num_loss']
    return stats


def simulate_month(stats):
    outcome = 'DOWN'
    value = 0.0
    if random() < stats['p_gain']:
        outcome = 'UP'
    if 'DOWN' == outcome:
        value = uniform(stats['mean_loss_size'], 0)
    else:
        value = uniform(0, stats['mean_gain_size'])
    return (outcome, value)


def plot_random_walk(rw, n):
    random_walk = pandas.Series(rw)
    pyplot.title('Random Walk (n=%d, %d months, simulation #%d)'
                 % (args.count, args.years * 12, n + 1))
    pyplot.ylabel('Growth (decimal)')
    pyplot.xlabel('Month')
    lines = pyplot.plot(random_walk * 100.0)
    pyplot.grid(True)
    pyplot.setp(lines, color='b', alpha=0.75, linewidth=3.0)
    pyplot.savefig('figures/randomwalk-n%d-m%d-%d.png' % (args.count,
                   args.years * 12, n + 1))
    pyplot.close()


def yields_summary_stats(yields):
    return """Summary Statistics:
    Mean: %0.04f\tMedian:   %0.04f
    Max:  %0.04f\tMin:      %0.04f
    MAD:  %0.04f\tKurtosis: %0.04f
    """ \
        % (
        yields.mean(),
        yields.median(),
        yields.max(),
        yields.min(),
        yields.mad(),
        yields.kurt(),
        )


def plot_yields(yields):
    ax = (yields * 100.0).hist(
        bins=int(sqrt(args.count)),
        color='g',
        alpha=1,
        linewidth=2,
        ylabelsize=16,
        xlabelsize=16,
        histtype='bar',
        )
    pyplot.title('Housing Annual Returns (n=%d, %d months)'
                 % (args.count, args.years * 12))
    pyplot.ylabel('# of Occurences')
    pyplot.xlabel('Return in %')
    fig = ax.get_figure()
    fig.savefig('figures/hist-n%d-m%d.png' % (args.count, args.years
                * 12))
    pyplot.close()


if __name__ == '__main__':
    print "*** Reading historical data from '%s' and calculating metrics" \
        % args.file
    hist_data = pandas.read_csv(args.file)
    hist_data['DELTA'] = hist_data.VALUE.astype(float) / 100.0
    hist_params = get_historical_params(hist_data)
    print '*** Running simulations with the following parameters (derived from the datafile): '
    print json.dumps(hist_params, sort_keys=True, indent=4,
                     separators=(',', ': '))
    print '*** Running %d simulations of %d months each' % (args.count,
            args.years * 12)
    yields = pandas.Series()
    for n in range(args.count):  # simulation number n
        month_sim = pandas.DataFrame(columns=('MONTH', 'OUTCOME',
                'VALUE'))
        random_walk = list()
        for m in range(args.years * 12):  # months to simulate
            sim = pandas.DataFrame()
            (outcome, value) = simulate_month(hist_params)
            month_sim.loc[m] = (m, outcome, value)
            if m > 0:
                random_walk.append(random_walk[m - 1] + value)
            else:
                random_walk.append(value)
        annualized_return = month_sim.VALUE.sum() / args.years
        yields = yields.set_value(n, annualized_return)
        plot_random_walk(random_walk, n)
    plot_yields(yields)
    print 'The complete list of yields for each run:\n', yields
    print yields_summary_stats(yields)
