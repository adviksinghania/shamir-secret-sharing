#!/usr/bin/env python3
# main.py
# Author: Advik Singhania
"""Visualising the difference of using Finite Field Arithmetic for Shamir Secret Sharing algorithm."""

import sys
import argparse
import matplotlib.pyplot as plt
import seaborn
import shamir_secret_galois
import shamir_secret

_NAME = sys.argv[0]


def set_arguments(p):
    # Setting options for command line arguments
    p.add_argument('-S', '--secret', dest='secret', type=int, help='Provide the original secret to be shared.')
    p.add_argument('-s', '--shares', dest='shares', type=int, help='Provide the number of shares to generate for sharing the secret.')
    p.add_argument('-t', '--threshold', dest='threshold', type=int, help='Provide the minimum number of shares required to reconstruct the secret.')


def get_arguments(p):
    # Parsing the command line arguments and returning the arguments
    arguments = p.parse_args()
    if arguments.secret is None:
        p.error(f'Please specify the secret. Type {_NAME} -h for more info.')
    elif arguments.shares is None:
        p.error(f'Please specify the number of shares. Type {_NAME} -h for more info.')
    elif arguments.threshold is None:
        p.error(f'Please specify the threshold for the secret. Type {_NAME} -h for more info.')
    else:
        return arguments


def main():
    # ArgumentParser() class to parse the command line arguments
    parser = argparse.ArgumentParser(description='Arguments to create an object for ShamirSecret class.', epilog=f'Example: python3 {_NAME} --secret 1234 --shares 4 --threshold 2')
    set_arguments(parser)
    # Getting the command line arguments
    args = get_arguments(parser)

    """Uncomment/comment one of the following at a time when running the script."""

    # *********************** Creating an object of ShamirSecret without Galois Field ************************
    s = shamir_secret.ShamirSecret(secret=args.secret, shares=args.shares, threshold=args.threshold)
    print(s)
    s.generate_shares()
    print('\nShares:', *s.get_shares(), sep='\n')
    x = list(map(lambda p: p[0], s.get_shares()))
    y = list(map(lambda p: p[1], s.get_shares()))

    seaborn.set_style('whitegrid')
    plt.scatter(x, y)
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    seaborn.despine()
    plt.show()

    print('\nReconstructed Secret:', s.reconstruct(s.random_shares()))
    # *********************************************************************************************************

    # ************************ Creating an object of ShamirSecret with Galois Field *************************
    s = shamir_secret_galois.ShamirSecret(secret=args.secret, shares=args.shares, threshold=args.threshold)
    print(s)
    s.generate_shares()
    print('\nShares:', *s.get_shares(), sep='\n')
    x = list(map(lambda p: p[0], s.get_shares()))
    y = list(map(lambda p: p[1], s.get_shares()))

    seaborn.set_style('whitegrid')
    plt.scatter(x, y)
    plt.xlabel('x - axis')
    plt.ylabel('y - axis')
    seaborn.despine()
    plt.show()

    print('\nReconstructed Secret:', s.reconstruct(s.random_shares(), s.prime))
    # *******************************************************************************************************


if __name__ == '__main__':
    main()
