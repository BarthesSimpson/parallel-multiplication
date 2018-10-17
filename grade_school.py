"""
This module implements integer multiplication
using only the primitive of addition. The 
algorithm has O(n^2) time complexity and 
O(n) space complexity.
"""

from util import carry_left, match_padding, pad, pad_if_needed, strip_leading_zeros
from big_numbers import big_number, big_number_as_array


def multiply_simple(x, y):
    """
    Multiplies two numbers represented as arrays
    using the grade school algorithm of cross-multiplying
    each pair of digits and "carrying" to the left when
    a pairwise multiplication results in a number larger
    than 9.

    :param x: []int
    :param y: []int
    :rtype []int
    """
    # Pad the shorter number with leading zeros
    x, y = match_padding(x, y)

    # Create a new list for the result
    res = [0] * len(x)

    # iterate from right to left, "multiplying"
    # the digit from x and the digit from y
    # by adding them and putting them into the
    # correct slot, carrying whenever the value
    # for that slot exceeds 9
    for i in range(len(x)):
        for j in range(len(y)):
            # figure out which slot we should be
            # adding our numbers to
            cardinality = i + j
            # get our pair for pairwise multiplication
            a = x[len(x) - (i + 1)]
            b = y[len(y) - (j + 1)]
            # if either of the numbers to be pairwise multiplied is zero,
            # we can just skip ahead; otherwise, "multiply" the pair
            if a > 0 and b > 0:
                for _ in range(a):
                    # first, need to make sure there is a slot to the left;
                    # if not, create it by adding more left padding
                    res = pad_if_needed(res, cardinality)
                    res[len(res) - (cardinality + 1)] += b
                # if the number overflowed, carry to the left recursively
                res = carry_left(res, cardinality)

    return strip_leading_zeros(res)


if __name__ == '__main__':

    print('testing multiply_simple')
    assert multiply_simple([0], [0]) == [0]
    assert multiply_simple([1], [0]) == [0]
    assert multiply_simple([1], [1]) == [1]
    assert multiply_simple([2], [3]) == [6]
    assert multiply_simple([2, 0], [3, 0]) == [6, 0, 0]
    assert multiply_simple([2, 4], [3, 5]) == [8, 4, 0]
    assert multiply_simple([2, 4, 5], [6, 7]) == [1, 6, 4, 1, 5]

    import time
    start = time.time()
    multiply_simple(big_number_as_array, big_number_as_array)
    end = time.time()
    print('naive', (end - start) * 1000, 'milliseconds')
    start = time.time()
    big_number * big_number
    end = time.time()
    print('native', (end - start) * 1000, 'milliseconds')
