#!/usr/bin/env python3
# shamir_secret_galois.py
# Author: Advik Singhania
"""Implementing Shamir's Secret Sharing algorithm in Python3 with Galois Field."""

import random


class ShamirSecret:
    """
    Encode and share a secret based on Shamir's Secret Sharing algorithm.

    Attributes
    ----------
    secret: int
        Stores the original secret
    shares: int
        Number of shares to be generated
    threshold: int
        Minimum number of shares required to reconstruct the secret
    prime: int
        The prime number used for Galois Field operations
    generated_shares: list
        Contains pairwise tuples of shares generated from the secret

    """

    def __init__(self, **kwargs) -> None:
        """
        Construct a ShamirSecret object.

        Parameters
        ----------
        kwargs: dict
            Contains the mandatory keyword arguments:
            secret: int
                The secret to be shared
            shares: int
                Number of shares to be generated
            threshold: int
                Minimum number of shares required to reconstruct the secret

        Example
        -------
        >>> s = ShamirSecret(secret=1234, shares=4, threshold=2)

        """
        self.secret = kwargs.get('secret')
        self.shares = kwargs.get('shares')
        self.threshold = kwargs.get('threshold')
        self.prime = self.next_prime()
        self.generated_shares = list()

    def __str__(self) -> str:
        return f'ShamirSecret(secret={self.secret}, shares={self.shares}, threshold={self.threshold})'

    def next_prime(self):
        """
        Generate the smallest next prime number greater than num.

        Returns
        -------
        num: int
            The prime number

        """

        def isPrime(n: int) -> bool:
            # Checks if a number is prime or not
            if n <= 1:
                return False
            elif n <= 3:
                return True
            elif n % 2 == 0 or n % 3 == 0:
                return False

            for i in range(5, int(n ** 0.5 + 1), 6):
                if n % i == 0 or n % (i + 2) == 0:
                    return False

            return True

        num = self.secret
        if num <= 1:
            return 2

        num += 1
        while not isPrime(num):
            num += 1

        return num

    def generate_shares(self):
        """
        Generate the specified number of shares for the secret.

        Example
        -------
        >>> s.generate_shares()
        >>> print(*s.get_shares(), sep='\\n')
        (1, 890)
        (2, 546)
        (3, 202)
        (4, 1095)
        ...

        """
        # random coefficients of the polynomial
        coefficients = tuple(random.randrange(1, self.prime) for _ in range(self.threshold - 1))

        def construct_poly(s, k, a, x, p):
            # f(x) = a0 + a1 * x + a2 * (x ^ 2) + .... + a(k-1) * (x ^ k-1)
            # constructing the polynomial for each value of x,
            # with s as a0 and other coefficients in tuple a
            f = s
            for i, pw in zip(a, tuple(range(1, k))):
                f += i * x ** pw

            return f % p

        for x in range(1, self.shares + 1):
            fx = construct_poly(self.secret, self.threshold, coefficients, x, self.prime)
            self.generated_shares.append((x, fx))

    def get_shares(self):
        """Returns the generated shares."""
        return self.generated_shares

    def random_shares(self):
        """
        Select random threshold number of shares from the list of generated_shares.

        Returns
        -------
        : tuple
            Contains the pairwise tuples of shares.

        Example
        -------
        >>> s.random_shares()
        ((4, 1095), (1, 890))

        """
        return tuple(random.sample(self.generated_shares, k=self.threshold))

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm."""
        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y

        return last_x, last_y

    def galois_div(self, num, den, p):
        """
        Division in integers modulus p means finding the inverse of the
        denominator modulo p and then multiplying the numerator by this
        inverse.

        Inverse of an integer can be found using the Extended Euclidean Algorithm.
        (Note: inverse of A is B such that A*B % p == 1)

        Compute num / den modulo prime p

        To explain what this means, the return value will be such that the
        following is true: den * galois_div(num, den, p) % p == num

        Parameters
        ----------
        num: int
            Numerator
        den: int
            Denominator
        p: int
            Prime Number

        """
        inv, _ = self.extended_gcd(den, p)
        return num * inv

    def reconstruct(self, rand_shares, prime) -> int:
        """
        Reconstruct the secret with random shares and a prime.

        Parameters
        ----------
        rand_shares: tuple
            Containing pairwise tuples of random shares.
        prime: int
            The prime number for the galois field.

        Returns
        -------
        sigma: int
            The reconstructed secret

        Example
        -------
        >>> s.reconstruct(s.random_shares(), s.prime)
        1234

        """
        l = len(rand_shares)  # length: number of random shares
        x_s = tuple(map(lambda x: x[0], rand_shares))  # x values of shares
        y_s = tuple(map(lambda x: x[1], rand_shares))  # y values of shares

        def PI(vars):  # product of inputs (PI)
            acc = 1
            for v in vars:
                acc *= v

            return acc

        nume = tuple()
        deno = tuple()
        for j in range(l):
            nume += (PI(x_s[m] for m in range(l) if m != j), )
            deno += (PI(x_s[m] - x_s[j] for m in range(l) if m != j), )

        den = PI(deno)
        num = sum(self.galois_div(nume[i] * den * y_s[i] % prime, deno[i], prime) for i in range(l))
        sigma = (self.galois_div(num, den, prime) + prime) % prime

        return sigma


if __name__ == '__main__':
    s = ShamirSecret(secret=1234, shares=4, threshold=2)
    print(s)
    s.generate_shares()
    print('\nShares:', *s.get_shares(), sep='\n')
    print('\nReconstructed Secret:', s.reconstruct(s.random_shares(), s.prime))
